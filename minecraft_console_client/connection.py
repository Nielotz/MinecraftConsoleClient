import logging
import queue
import socket
import threading
import zlib
from contextlib import suppress

logger = logging.getLogger('mainLogger')

from misc.consts import MAX_INT
from misc import utils


class Connection:
    """
    Main class that creates and handles TCP connection between server(host) and
    client.
    Handles reading(sending) data from(to) the server.

    Auto-closes connection when instance being deleted.

    """

    """ Positive threshold means number of bytes before start compressing
    otherwise compression is disabled."""
    _compression_threshold = -1
    __connection: socket.socket = None

    __listener: threading.Thread = None
    __sender: threading.Thread = None

    __ready = threading.Event()

    def __init__(self):
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        self.close()

    def setblocking(self, is_blocking: bool = True):
        """ Changes socket behavior. """
        self.__connection.setblocking(is_blocking)

    def set_compression(self, threshold: int):
        """
        Sets compression threshold.
        Negative threshold means no compression.
        """

        self._compression_threshold = threshold

        if threshold < 0:
            logger.info(f"Compression is disabled")
        else:
            logger.info(f"Compression is enabled, threshold: {threshold}")

    def connect(self, socket_data: (str, int), timeout: int = 5):
        """
        Starts connection using socket_data(ip / hostname, port).
        On error raises standard socket exceptions.

        :param timeout: connection timeout
        :param socket_data: tuple(host, port)
        """

        self.__connection.settimeout(timeout)
        self.__connection.connect(socket_data)

    def __receive_packet(self) -> (int, bytes):
        """
        Reads whole packet from connection.
        https://stackoverflow.com/a/17668009

        Returns 0, b'' when connection is broken or sth.

        :returns length of packet, read bytes
        :rtype int, bytes
        """

        # Broad try, because when sth went wrong here we are in danger.
        try:
            read_bytes = 0
            fragments = []

            packet_length = self.__read_packet_length()

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

        return packet_length, b''.join(fragments)

    def start_listener(self, received_queue: queue.Queue) -> bool:
        """
        Similar to start_sending.
        Starts new thread-daemon that listens packets incoming from the server.
        When received packet (if need) - decompresses,
        then inserts it into received_queue.
        Thread ends when length of a packet or declared length equals zero.
        When connection has been interrupted puts b'' into queue.

        :param received_queue: where to put received packets
        :returns started successfully
        :rtype bool
        """

        if self.__listener is not None and self.__listener.is_alive():
            logger.error("Listener already started")
            return False

        self.__ready = threading.Event()
        self.__listener = threading.Thread(target=self.__listen,
                                           args=(received_queue,),
                                           daemon=True)
        try:
            self.__listener.start()
            self.__ready.wait(15)
        except Exception:
            return False
        return True

    def start_sender(self, to_send: queue.Queue) -> bool:
        """
        Similar to start_listening.
        Starts new thread-daemon which waits for packets to appear in
        to_send then sends it to the server.

        :param to_send: queue from where get and send packets
        :returns started successfully
        :rtype bool
        """

        if self.__sender is not None and self.__sender.is_alive():
            logger.error("Sender already started")
            return False

        self.__ready = threading.Event()

        self.__sender = threading.Thread(target=self.__send,
                                         args=(to_send,),
                                         daemon=True
                                         )
        try:
            self.__sender.start()
            self.__ready.wait(15)
        except Exception:
            return False
        return True

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
        recv = self.__connection.recv
        for i in range(5):
            ordinal = recv(1)

            if len(ordinal) == 0:
                break
            byte = ord(ordinal)  # TODO: hashtable? 0 to 0xFF
            length |= (byte & 0x7F) << 7 * i

            if not byte & 0x80:
                break
        else:
            raise ValueError("VarInt is too big!")
        if length > MAX_INT:
            raise ValueError("VarInt is too big!")

        return length

    def close(self):
        """
        Tries to close connection, and stop threads in a nice way.
        Does not ensure that! But gives its full power.
        """
        with suppress(Exception):
            """ Shut down one or both halves of the connection. """
            self.__connection.shutdown(socket.SHUT_RDWR)
            logger.info("Shutdown connection")

        with suppress(Exception):
            """ Close a socket file descriptor. """
            self.__connection.close()
            logger.info("Closed socket")

        # Closing connection makes listener exit.
        logger.debug("Trying to stop listener...")
        with suppress(Exception):
            self.__listener.join(timeout=20)

        # When listener exits, sends packet that exits sender.
        logger.debug("Trying to stop sender...")
        with suppress(Exception):
            self.__sender.join(timeout=5)

        logger.info("Closed connection")

    def __listen(self, received: queue.Queue):
        """
        Similar to __sender.
        Starts listening packets incoming from server.
        When received packet inserts it into buffer queue (received).
        It is blocking function, so has to be run in a new thread as daemon.
        Closes when:
            receive packet longer or shorted than declared,
            len(packet) or declared length equals zero.
        When connection has been interrupted puts b'' into queue.

        Job:
            Receives packet awaiting to be received(if needed) - decompresses.
            Appends them to buffer queue (received).
            If delay_after_packet [seconds] is over 0.001 - sleeps.
            After every number_of_packets_before_delay packets received sleeps
            for delay_after_packets [seconds].
            After every packets_before_full_receive receives all awaiting packets.
            Repeat.

        :param received: queue.Queue (FIFO) where read packets append to
        """

        if not threading.current_thread().daemon:
            raise RuntimeError(
                "Thread running start_listening() has to start as daemon!")

        self.__ready.set()

        while True:
            size, packet = self.__receive_packet()

            if size == 0:
                logger.critical("Packet length equals zero.")
                received.put(b'')
                break

            # If compression is enabled.
            if not self._compression_threshold < 0:
                data_length, packet = utils.extract_varint(packet)

                if data_length != 0:
                    packet = zlib.decompress(packet)

                    if len(packet) < self._compression_threshold:
                        logger.critical(
                            "Packet length is shorter than compression threshold.")
                        received.put(b'')
                        break
            # End of decompression

            received.put(packet)

        logger.info("Exiting listening thread")

    def __send(self, to_send: queue.Queue):
        """
        Similar to __listen.
        Starts waiting for bytes to appear in to_send then sends it to server.
        It is blocking function, so has to be run in a new thread as a daemon.

        Job:
            Freezes until packet appear in buffer.
            If compression is enabled and packet exceeds compression_threshold
            compresses.
            Sends it to the host.
            Repeat.

        :param to_send: queue.Queue (FIFO) from where to read bytes to send
        """

        if not threading.current_thread().daemon:
            raise RuntimeError(
                "Thread running start_sending() has to be a daemon!")

        self.__ready.set()

        convert_to_varint = utils.convert_to_varint
        while True:
            # packet: b'VarInt(Packet ID)' + b'VarInt(Data)'
            payload = to_send.get(block=True)

            payload_len = len(payload)

            # Compression is disabled
            if self._compression_threshold < 0:
                packet = convert_to_varint(payload_len) + payload

            else:
                # TODO: Optimize by hard coding some values.

                # When compression disabled for this packet
                if payload_len < self._compression_threshold:
                    packet = convert_to_varint(payload_len + 1) + \
                             bytes(b'\x00') + payload

                else:  # Compression is enabled
                    compressed_payload = zlib.compress(payload)
                    payload = convert_to_varint(payload_len) + compressed_payload
                    packet = convert_to_varint(len(payload)) + payload
            # End of compression

            try:
                self.__connection.sendall(packet)
            except ConnectionAbortedError:
                """ Client closed connection """
                logger.warning("Connection has been shut down by client. ")
                break
            except Exception as e:
                logger.critical(f"Uncaught exception occurred: {e}")
                break

        logger.info("Exiting sending thread")
