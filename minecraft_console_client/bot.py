import logging
from typing import Any

logger = logging.getLogger('mainLogger')

import queue
import threading
import time

from versions.version import Version
from connection import Connection
from misc import utils
from data_structures.game_data import GameData
from data_structures.player import Player

import versions.defaults


class Bot:
    """
    Manages bot behavior. Highest API level
    Imitate last stage e.g. "game" in system->client->GAME
    """

    version_data: Version = None
    PacketCreator = None
    clientbound_action_list: dict = None

    received_queue: queue.Queue = queue.Queue()
    to_send_queue: queue.Queue = queue.Queue()

    _game_data: GameData = None
    _player: Player = None
    _conn: Connection = None

    __listener: threading.Thread = None
    __sender: threading.Thread = None

    __ready = threading.Event()
    __host: (str, int) = None

    def __init__(self, host: (str, int), version: Version, username: str):
        """
        :param host: host data (address, port) to which client connects to
        :param version: Version, tells which version of protocol to use
        :param username: username
        """

        self._game_data = GameData()
        self._player = Player()

        logger.info("Creating bot".center(60, "-"))

        self._player.username = username
        logger.info("|" +
                    f"Username: '{username}'".center(58, " ") +
                    "|")

        self.version_data: versions.defaults.VersionData = version.value
        self.PacketCreator = self.version_data.PacketCreator
        logger.info("|" +
                    f"Client version: '{self.version_data.release_name}'"
                    .center(58, " ") + "|")

        if not self.switch_action_packets("login"):
            raise RuntimeError("Not found 'login' in action_packet")

        self.__host = host

        logger.info("|" + f"Server address: '{self.__host[0]}: {self.__host[1]}'"
                    .center(58, " ") + "|")

        logger.info("".center(60, "-"))

        self._conn = Connection()

        self.__listener = threading.Thread(target=self.__start_listening,
                                           args=(self.received_queue,
                                                 self.__ready,
                                                 0.001),
                                           daemon=True
                                           )

        self.__sender = threading.Thread(target=self.__start_sending,
                                         args=(self.to_send_queue, self.__ready),
                                         daemon=True
                                         )

    def __del__(self):
        logger.info("Deleting bot")
        self.stop("Shutting down bot")  # Temporally

    def start(self) -> str:
        """
        Starts playing.
        Returns error message, or - when everything worked as expected - "".

        :return error message
        :rtype str
        """

        logger.info(f"Starting bot: '{self._player.username}'")

        if not self.connect_to_server():
            return "Can't connect to the server"
        logger.info("Successfully connected to server.")

        if not self.start_listening():
            return "Cannot start listener"
        logger.debug("Successfully started listening thread")

        if not self.start_sending():
            return "Cannot start listener"
        logger.debug("Successfully started sending thread")

        if not self.login_non_premium():
            return "Can't connect to the server"
        logger.info("Successfully logged in to server.")

        if not self.switch_action_packets("play"):
            return "Can't assign 'play' action packet."

        while True:
            data = self.received_queue.get(timeout=10)
            if len(data) == 0:
                return "Received 0 bytes"
            packet_id, data = utils.unpack_varint(data)

            self._interpret_packet(packet_id, data)

    def start_listening(self) -> bool:
        """
        Similar to start_sending.
        Starts new thread-daemon that listens packets incoming from server.
        When received packet (if need) - decompresses,
        then inserts it into self.received_queue.
        Thread ends when received packet longer or shorted than declared,
        len(packet) or declared length equals zero.
        When connection has been interrupted puts b'' into queue.

        :returns success
        :rtype bool
        """
        if self.__listener.is_alive():
            logger.error("Listener already started")
            return False
        try:
            self.__listener.start()
            self.__ready.wait(15)
        except Exception:
            return False
        return True

    def start_sending(self) -> bool:
        """
        Similar to start_listening.
        Starts new thread-daemon which waits for packets to appear in
        self.to_send_queue then sends it to server.

        :returns success
        :rtype bool
        """
        if self.__sender.is_alive():
            logger.error("Sender already started")
            return False
        try:
            self.__sender.start()
            self.__ready.wait(15)
        except Exception:
            return False
        return True

    def stop(self, reason="not defined"):
        """ Shutdowns and closes connection then threads get auto-closed """
        logger.info(
            f"Stopping bot '{self._player.username}'. Reason: {reason}")

        self._conn.close()

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
        logger.debug("Stopped".center(60, '-'))

    def login_non_premium(self) -> bool:
        """
        # TODO: Make this comment readable
        Sends login packets to offline (non-premium) server e.g. without encryption.

        :return success
        :rtype bool
        """
        logger.info("Trying to log in in offline mode (non-premium)")

        self.to_send_queue.put(
            self.version_data.PacketCreator.login.handshake(self.__host))

        self.to_send_queue.put(
            self.version_data.PacketCreator.login.login_start(
                self._player.username))

        # Try to log in for 50 sec (10 sec x 5 packets)
        for i in range(5):
            data = self.received_queue.get(timeout=10)
            if len(data) == 0:
                logger.error("Received 0 bytes")
                return False
            packet_id, data = utils.unpack_varint(data)

            if self._interpret_packet(packet_id, data):
                return True

        return False

    def connect_to_server(self, timeout=5) -> bool:
        """
        Establishes connection with to server.
        Not raises exceptions.

        :param timeout: connection timeout
        :returns: success
        :rtype: bool

        """

        # TODO: add retry, timeout, etc...
        try:
            self._conn.connect(self.__host, timeout)
        except OSError as e:
            logger.critical(f"Can't connect to: "
                            f"'{self.__host[0]}:"
                            f"{self.__host[1]}'"
                            f", reason: {e}")
            return False

        logger.info("Established connection with: "
                    f"'{self.__host[0]}:"
                    f"{self.__host[1]}'")
        return True

    def switch_action_packets(self, actions_type: str = "login") -> bool:
        """
        Switches between different action types.
        To see possible action types see: docs of action.get_action_list()

        Based on V1_12_2:
        packet id of disconnect in "login" equals 0 whereas in "play" equals 26.

        :return success
        :rtype bool
        """

        self.clientbound_action_list = \
            self.version_data.action_list.get(actions_type)
        return self.clientbound_action_list is not None

    def _interpret_packet(self, packet_id: int, payload: bytes) -> Any:
        """
        Interpret given packet and call function assigned to packet id in
        action_list.

        :param packet_id: int representing packet id e.g 0,1,2,3,4...
        :param payload: uncompressed data
        :return: whatever action_list[packet_id]() returns
        """

        if packet_id in self.clientbound_action_list:
            return self.clientbound_action_list[packet_id](self, payload)
        else:
            logger.debug(f"Packet with id: {packet_id} is not implemented yet")
            return None

    def on_death(self):
        logger.info("Player has dead. Respawning.")
        self.to_send_queue.put(self.PacketCreator.play.client_status(0))

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
                self._conn.sendall(packet)
            except ConnectionAbortedError:
                """ Client closed connection """
                logger.info("Connection has been shut down by client. ")
                break

        logger.info("Exiting sending thread")
