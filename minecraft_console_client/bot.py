import logging
from typing import Any
import queue

logger = logging.getLogger('mainLogger')

from versions.version import Version
from connection import Connection
from misc import utils
from data_structures.game_data import GameData
from data_structures.player import Player
from data_structures.position import Position
from action.move_manager import MoveManager
from action.target import Target

import versions.defaults


class Bot:
    """
    Manages bot behavior. Highest API level
    Imitate last stage e.g. "game" in `os->client->GAME`
    """

    version_data: Version = None
    login_packet_creator = None  # Module
    play_packet_creator = None  # Module
    clientbound_action_list: dict = None

    received_queue: queue.Queue = None
    send_queue: queue.Queue = None
    move_manager: MoveManager = None

    _game_data: GameData = None
    _conn: Connection = None

    __host: (str, int) = None

    def __init__(self, host: (str, int), version: Version, username: str):
        """
        :param host: host data (address, port) to which client connects to
        :param version: Version, tells which version of protocol to use
        :param username: username
        """

        self._game_data = GameData()
        self._game_data.player = Player()

        logger.info("Creating bot".center(60, "-"))

        self._game_data.player.username = username
        logger.info("|" +
                    f"Username: '{username}'".center(58, " ") +
                    "|")

        self.version_data: versions.defaults.VersionData = version.value

        self.play_packet_creator = self.version_data.packet_creator.play
        self.login_packet_creator = self.version_data.packet_creator.login

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

        self.send_queue: queue.Queue = queue.Queue()
        self.received_queue: queue.Queue = queue.Queue()

        self.move_manager = MoveManager(self.send_queue,
                                        self.play_packet_creator,
                                        self._game_data.player)

        self.move_manager.start()

    def __del__(self):
        logger.info("Deleting bot")
        self.exit("Shutting down bot")  # Temporally

    def start(self) -> str:
        """
        Starts playing.
        Returns error message, or - when everything worked as expected - "".

        :return error message
        :rtype str
        """

        logger.info(f"Starting bot: '{self._game_data.player.username}'")

        if not self.connect_to_server():
            return "Can't connect to the server"
        logger.info("Successfully connected to server.")

        if not self.start_listening():
            return "Cannot start listener"
        logger.debug("Successfully started listening thread")

        if not self.start_sending():
            return "Cannot start sender"
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

    def start_sending(self) -> bool:
        """ See Connection.start_sender() """
        return self._conn.start_sender(self.send_queue)

    def start_listening(self):
        """ See Connection.start_listener() """
        return self._conn.start_listener(self.received_queue)

    def exit(self, reason="not defined"):
        """ Shutdowns and closes connection then threads get auto-closed """
        logger.info(f"Stopping bot '{self._game_data.player.username}'. "
                    f""f"Reason: {reason}")

        self._conn.close()

        logger.debug("Stopped".center(60, '-'))

    def login_non_premium(self) -> bool:
        """
        # TODO: Make this comment readable
        Sends login packets to offline (non-premium) server e.g. without encryption.

        :return success
        :rtype bool
        """
        logger.info("Trying to log in in offline mode (non-premium)")

        self.send_queue.put(
            self.login_packet_creator.handshake(self.__host))

        self.send_queue.put(
            self.login_packet_creator.login_start(
                self._game_data.player.username))

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
        self.send_queue.put(self.play_packet_creator.client_status(0))

    def goto(self, x: float, y: float, z: float):
        self.move_manager.add_target(Target(x, y, z))


        




