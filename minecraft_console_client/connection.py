import logging
import socket
import zlib
import threading
import queue
import time

logger = logging.getLogger('mainLogger')

from misc.consts import MAX_INT
from misc import utils


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

    __listener: threading.Thread = None
    __sender: threading.Thread = None

    __ready = threading.Event()

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

    def start_listener(self, received_queue: queue.Queue) -> bool:
        """
        Similar to start_sending.
        Starts new thread-daemon that listens packets incoming from server.
        When received packet (if need) - decompresses,
        then inserts it into self.received_queue.
        Thread ends when received packet longer or shorted than declared,
        len(packet) or declared length equals zero.
        When connection has been interrupted puts b'' into queue.

        :param received_queue: where to put received packets
        :returns started successfully
        :rtype bool
        """

        if self.__listener is not None and self.__listener.is_alive():
            logger.error("Listener already started")
            return False

        self.__listener = threading.Thread(target=self.__start_listening,
                                           args=(received_queue,
                                                 self.__ready,
                                                 0.001),
                                           daemon=True
                                           )
        try:
            self.__listener.start()
            self.__ready.wait(15)
        except Exception:
            return False
        return True

    def start_sender(self, to_send_queue: queue.Queue) -> bool:
        """
        Similar to start_listening.
        Starts new thread-daemon which waits for packets to appear in
        self.to_send_queue then sends it to server.

        :param to_send_queue: from where send packets
        :returns started successfully
        :rtype bool
        """
        if self.__sender is not None and self.__sender.is_alive():
            logger.error("Sender already started")
            return False

        self.__sender = threading.Thread(target=self.__start_sending,
                                         args=(to_send_queue, self.__ready),
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

        # Closing connection makes listener exit.
        if self.__listener.is_alive():
            logger.debug("Waiting for listener to end")
            try:
                self.__listener.join(timeout=10)
            except TimeoutError:
                logger.error("Cannot stop listener.")
        else:
            logger.debug("Listener is already closed")

        # When listener exits, sends packet that exits sender.
        if self.__sender.is_alive():
            logger.debug("Waiting for sender to end")
            try:
                self.__sender.join(timeout=10)
            except TimeoutError:
                logger.error("Cannot stop sender.")
        else:
            logger.debug("Sender is already closed")

        logger.info("Closed connection")

    def __start_listening(self, buffer: queue.Queue, ready: threading.Event,
                          check_delay=0.050):
        """
        Similar to start_sending.
        Starts listening packets incoming from server.
        When received packet (if need) - decompresses,
        then inserts it into buffer.
        It is blocking function, so has to be run in a new thread as daemon.
        Closes when receive packet longer or shorted than declared,
        len(packet) or declared length equals zero.
        When connection has been interrupted puts b'' into queue.

        Job:
            Receives packets waiting to be received,
            appends them to buffer specified in constructor,
            sleeps for check_delay [seconds].
            Repeat.

        :param buffer: queue.Queue (FIFO) where read packets append to
        :param ready: threading.Event object sets when thread started
        :param check_delay: delay in seconds that
                            specifies how long sleep between receiving packets
        """

        if not threading.current_thread().daemon:
            raise RuntimeError(
                "Thread running start_listening() has to start as daemon!")

        ready.set()

        while True:
            size, packet = self.receive_packet()

            # buffer.put() blocks if necessary until a free slot is available.

            if size != len(packet):
                logger.error(f"Packet length: {len(packet)} "
                             f"not equal to declared size: {size}")

            elif len(packet) == 0:
                logger.error(
                    f"Packet length: equals zero. Declared size: {size}")

            elif size == 0:
                logger.error(f"Declared packet length equals zero")

            else:  # Everything is everything
                buffer.put(packet)
                time.sleep(check_delay)
                continue

            buffer.put(b'')
            break

        logger.info("Exiting listening thread")

    def __start_sending(self, buffer: queue.Queue, ready: threading.Event):
        """
        Similar to start_listen.
        Starts waiting for packets to appear in buffer then sends it to server.
        It is blocking function, so has to be run in a new thread as daemon.

        Job:
            Freeze until packet appear in buffer,
            send it the connection.
            Repeat.

        :param ready: threading.Event object sets when thread started
        :param buffer: queue.Queue (FIFO) from where packets are reads
        """

        if not threading.current_thread().daemon:
            raise RuntimeError(
                "Thread running start_sending() has to be a daemon!")

        ready.set()

        while True:
            packet = buffer.get(block=True)
            # logger.debug(f'[SEND] size: {len(packet)}')
            try:
                self.sendall(packet)
            except ConnectionAbortedError:
                """ Client closed connection """
                logger.info("Connection has been shut down by client. ")
                break

        logger.info("Exiting sending thread")


