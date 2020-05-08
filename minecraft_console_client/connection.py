import socket
import zlib
import select

import logging
logger = logging.getLogger('mainLogger')

from consts import MAX_INT
import utils


class Connection:
    """
    Main class that creates and handles tcp connection between server(host) and
    client(localhost).
    Handle reading(sending) data from(to) server.

    Auto-closes connection when instance being deleted.
    """
    # TODO: improve __del__ to make sure socket closed correctly e.g.
    #   exception catch only "Can't close not open socket"

    """
     Positive threshold means number of bytes before start compressing
     otherwise compression is disabled.
    """
    _compression_threshold = -1
    __connection: socket.socket = None

    def __init__(self):
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        self.close()

    def setblocking(self, is_blocking: bool = True):
        """ Change socket behavior """
        self.__connection.setblocking(is_blocking)

    def set_compression(self, threshold: int):
        self._compression_threshold = threshold

        if threshold < 0:
            logger.info(f"Compression is disabled")
        else:
            logger.info(f"Compression is enabled, threshold: {threshold}")

    def connect(self, socket_data: (str, int), timeout: int = 5):
        """"
        Starts connection using socket_data(ip or hostname, port).
        On error raises standard socket exceptions.

        :param timeout: connection timeout
        :param socket_data: tuple(host, port)
        """

        self.__connection.settimeout(timeout)
        self.__connection.connect(socket_data)

    def receive_packet(self) -> (int, bytes):
        """
        Reads whole packet from connection and auto-decompress.
        https://stackoverflow.com/a/17668009

        Returns 0, b'' when connection is broken or sth

        :returns length of packet, read bytes
        :rtype int, bytes
        """
        # Broad try, because when sth went wrong here we are in danger.
        try:
            packet_length = self.__read_packet_length()

            fragments = []
            read_bytes = 0
            while read_bytes < packet_length:
                packet_part = self.__connection.recv(packet_length - read_bytes)
                if not packet_part:
                    return 0, b''
                fragments.append(packet_part)
                read_bytes += len(packet_part)

        except BrokenPipeError:
            logger.critical("Connection has been broken.")
            return 0, b''
        except Exception as e:
            logger.critical(f"Uncaught exception occurred: {e}")
            return 0, b''

        packet = b''.join(fragments)

        if len(packet) == 0:
            logger.critical("Packet length equals zero.")
            return 0, b''

        # Decompression section didn't move to its own function to avoid
        # unnecessary copying of potentially huge amount of data

        # If compression is enabled
        if not self._compression_threshold < 0:
            data_length, packet = utils.unpack_varint(packet)
            if data_length != 0:
                packet = zlib.decompress(packet)
                packet_length = data_length
            else:
                # Exclude data_length(0) from packet_length
                packet_length -= 1

        # End of decompression

        return packet_length, packet

    def sendall(self, payload: bytes):
        """
        If compression_threshold is non-negative then auto-compresses data.
        Adds packet length and sends the packet to the host.

        :param payload: b'VarInt(Packet ID)' + b'VarInt(Data)'
        """

        payload_len = len(payload)

        # Compression is disabled
        if self._compression_threshold < 0:
            packet = utils.convert_to_varint(payload_len) + payload

        else:
            # Compression section didn't move to its own function to avoid
            # unnecessary copying of potentially huge amount of data

            # TODO: If works optimize by hard coding some values.
            # Compression disabled for this packet
            if payload_len < self._compression_threshold:
                payload_len = utils.convert_to_varint(0)
                payload = payload_len + payload
                packet_len = len(payload)

                packet = utils.convert_to_varint(packet_len) + payload

            # Compression is enabled
            else:
                compressed_payload = zlib.compress(payload)
                payload = utils.convert_to_varint(
                    payload_len) + compressed_payload
                packet_len = len(payload)
                packet = utils.convert_to_varint(packet_len) + payload
        # End of compression

        self.__connection.sendall(packet)

    def __read_packet_length(self) -> int:
        """
        Reads and unpacks unknown length (up to 5 bytes) VarInt.
        If not found end of VarInt raises ValueError.
        Stolen from
        https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0

        :returns VarInt: int
        :rtype int
        """

        length = 0
        for i in range(5):
            ordinal = self.__connection.recv(1)

            if len(ordinal) == 0:
                break

            byte = ord(ordinal)
            length |= (byte & 0x7F) << 7 * i

            if not byte & 0x80:
                break
        else:
            raise ValueError("VarInt is too big!")
        if length > MAX_INT:
            raise ValueError("VarInt is too big!")

        return length

    def close(self):
        try:
            """ Shut down one or both halves of the connection. """
            self.__connection.shutdown(socket.SHUT_RDWR)
            logger.debug("Shutdown connection")
        except:
            pass
        try:
            """ Close a socket file descriptor. """
            self.__connection.close()
            logger.debug("Closed socket")
        except:
            pass
        logger.info("Closed connection")
