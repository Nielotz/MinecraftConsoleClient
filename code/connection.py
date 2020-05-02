import socket

import logging

from consts import MAX_INT
import utils
from packet import PacketID


class Connection:
    """
    Main class that create and handle tcp connection between server and
    client(localhost).
    Handle reading(sending) data from(to) server.

    Auto-close connection when instance being deleted.
    """
    # TODO: improve __del__ to make sure socket closed correctly e.g.
    #   exception catch only "Can't close not open socket"

    """
     Positive threshold means number of bytes before start compressing
     otherwise compression is disabled
    """
    _compression_threshold = -1
    __connection: socket.socket = None

    def __init__(self):
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        try:
            self.__connection.shutdown(socket.SHUT_RDWR)
            logging.info("Shutdown connection")
        except:
            pass
        try:
            self.__connection.close()
            logging.info("Closed socket")
        except:
            pass

    def set_compression(self, threshold: int):
        self._compression_threshold = threshold

        if threshold < 0:
            logging.info(f"Compression is disabled")
        else:
            logging.info(f"Compression is enabled, threshold: {threshold}")

    def connect(self, socket_data: (str, int), timeout: int = 5):
        """"
        Start connection using socket_data(ip or hostname, port).
        On error raises standard socket exceptions

        :param timeout: connection timeout
        :param socket_data: tuple(host, port)
        """

        self.__connection.settimeout(timeout)
        self.__connection.connect(socket_data)

    def receive(self) -> (int, memoryview):
        """
        Read whole packet from connection.
        https://stackoverflow.com/a/17668009

        :returns length of packet, memoryview of read bytes
        :rtype int, memoryview
        """
        packet_length = self.__read_packet_length()

        fragments = []
        read_bytes = 0
        while read_bytes < packet_length:
            packet = self.__connection.recv(packet_length - read_bytes)
            if not packet:
                return None
            fragments.append(packet)
            read_bytes += len(packet)

        return packet_length, b''.join(fragments)

    def __read_packet_length(self) -> int:
        """
        Read and unpack unknown length (up to 5 bytes) VarInt.
        If not found end of VarInt raise ValueError.
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

    def send(self, packet_id: PacketID, arr_with_payload):
        """
        Send the data on the connection.
        Stolen from
        https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0
        """
        data = packet_id.value.bytes
        logging.debug(f"[SEND] {packet_id.name} {arr_with_payload}")
        # data_log = [data, ]
        for arg in arr_with_payload:
            data += utils.pack_data(arg)
            # data_log.append(utils.pack_data(arg))

        self.__connection.send(utils.convert_to_varint(len(data)) + data)
