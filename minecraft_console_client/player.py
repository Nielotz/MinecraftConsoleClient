import logging

logger = logging.getLogger('mainLogger')

import sys
import queue
import threading
import time

from connection import Connection
from version import Version, VersionNamedTuple
import action
import utils

from packet import Creator


class Player:
    """
    Manages player behavior. Highest API level
    Imitate last stage e.g. "game" in system->client->GAME
    """
    version: VersionNamedTuple = None
    action_list: dict = None

    received_queue: queue.Queue = queue.Queue()
    to_send_queue: queue.Queue = queue.Queue()

    listener: threading.Thread = None
    sender: threading.Thread = None

    _conn: Connection = None
    _host: (str, int) = None
    _data: dict = {"username": "Anyone"}
    _ready = threading.Event()

    def __init__(self, host: (str, int), version: Version, username: str):
        """
        :param host: host data (address, port) to which client connects to
        :param version: VersionNamedTuple object from VERSION,
                        tells which version of protocol to use
        :param username: username
        """

        logger.info("Creating player".center(60, "-"))

        self._data["username"] = username
        logger.info("|" +
                    f"Username: '{self._data['username']}'".center(58, " ") +
                    "|")

        self.version = version.value
        logger.info("|" +
                    f"Client version: '{self.version.release_name}'"
                    .center(58, " ") + "|")

        self._host = host
        logger.info("|" + f"Server address: '{self._host[0]}: {self._host[1]}'"
                    .center(58, " ") + "|")

        logger.info("".center(60, "-"))

        self._conn = Connection()

        self.action_list = action.get_action_list(self.version)

        self.listener = threading.Thread(target=self.__start_listening,
                                         args=(self.received_queue, self._ready),
                                         daemon=True
                                         )

        self.sender = threading.Thread(target=self.__start_sending,
                                       args=(self.to_send_queue, self._ready),
                                       daemon=True
                                       )

    def __del__(self):
        self.stop("Shutting down player")  # Temporally

    def start(self):
        """ Starts as bot. """

        logger.info(f"Starting bot: '{self._data['username']}'")

        # If possible change to decorators
        if not self.connect_to_server():
            logger.critical("Can't connect to the server")
            self.stop("Can't connect to the server")
            return False

    def start_listening(self):
        """
        Similar to start_sending.
        Starts new thread-daemon that listens packets incoming from server.
        When received packet (if need) - decompresses,
        then inserts it into self.received_queue.
        Thread ends when received packet longer or shorted than declared,
        len(packet) or declared length equals zero.
        When connection has been interrupted puts b'' into queue.
        """
        if self.listener.is_alive():
            logger.error("Listener already started")
            return False
        try:
            self.listener.start()
            self._ready.wait(15)
        except Exception:
            return False
        return True

    def start_sending(self):
        """
        Similar to start_listening.
        Starts new thread-daemon which waits for packets to appear in
        self.to_send_queue then sends it to server.
        """
        if self.sender.is_alive():
            logger.error("Sender already started")
            return False
        try:
            self.sender.start()
            self._ready.wait(15)
        except Exception:
            return False
        return True

    def stop(self, reason="not defined"):
        logger.info(f"Stopping program. Reason: {reason}")
        self._conn.close()

    def connect_to_server(self, timeout=5):
        """
        Connects to the server.
        Allows to start sending playing packets.
        Starts sender and receiver.

        :returns: success
        :rtype: bool

        """
        # TODO: add retry, timeout, etc...
        if not self._connect(timeout=timeout):
            return False

        if not self.start_listening():
            self.stop("Cannot start listener")
            return False
        logger.debug("Successfully started listening thread")

        if not self.start_sending():
            self.stop("Cannot start listener")
            return False
        logger.debug("Successfully started sending thread")

        if not self._login():
            return False
        return True

    def _login(self):
        """
        # TODO: Make this comment readable
        Sends login packets to offline (non-premium) server e.g. without encryption.

        :return success
        :rtype bool
        """
        logger.info("Trying to log in in offline mode")

        packet = Creator.Login.handshake(self._host, self.version)
        self.to_send_queue.put(packet)

        packet = Creator.Login.login_start(self._data["username"])
        self.to_send_queue.put(packet)

        # self._conn.close()

        for i in range(10):  # Try for 10 packets
            data = self.received_queue.get(timeout=10)
            if len(data) == 0:
                logger.error("Received 0 bytes")
                return False
            packet_id, data = utils.unpack_varint(data)

            if self.interpret_login_packet(packet_id, data):
                return True
        return False

    def interpret_packet(self, packet_id: int, payload: bytes):
        logger.debug(f"[1/2] Interpreting packet with id: {packet_id}")

        if packet_id in self.action_list:
            self.action_list[packet_id](self, payload)
        else:
            logger.debug("[2/2] Not implemented yet")

    def interpret_login_packet(self, packet_id: int, payload: bytes):
        logger.debug(f"[1/2] Interpreting packet with id: {packet_id}")

        if packet_id in self.action_list:
            self.action_list[packet_id](self, payload)
            if packet_id == 2:
                return True
        else:
            logger.debug("[2/2] Not implemented yet")
        return False

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
            size, packet = self._conn.receive_packet()

            # buffer.put() blocks if necessary until a free slot is available.

            logger.debug(f'[RECEIVED] size: {size}')

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
            logger.debug(f'[SEND] size: {len(packet)}')
            try:
                self._conn.sendall(packet)
            except ConnectionAbortedError:
                """ Client closed connection """
                logger.info("Connection has been shut down by client. ")
                break

        logger.info("Exiting sending thread")

    def _connect(self, timeout=5):
        """
        Connects to server.
        Not raises exceptions.

        :param timeout: connection timeout
        :returns success
        :rtype bool
        """

        try:
            self._conn.connect(self._host, timeout)
        except OSError as e:
            logger.critical(f"Can't connect to: "
                            f"'{self._host[0]}:"
                            f"{self._host[1]}'"
                            f", reason: {e}")
            return False

        logger.info("Established connection with: "
                    f"'{self._host[0]}:"
                    f"{self._host[1]}'")
        return True
