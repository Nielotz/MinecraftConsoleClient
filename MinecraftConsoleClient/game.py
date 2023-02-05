"""
Container for game class.

Everything what is happening, happens here.
Everything what is controlled, is controlled here.
"""

import logging
import queue
from typing import Any, Union, TYPE_CHECKING

import action.move_manager
import connection
import data_structures.hero
import data_structures.host
import versions.base
import versions.version
from data_structures.game_data import GameData
from misc.exceptions import DisconnectedByServerException, InvalidUncompressedPacketError
from packet.packet_data_reader import PacketDataReader
from versions.v1_12_2.packet.clientbound.packet_specific import PacketSpecific

if TYPE_CHECKING:
    import versions.base.data_structures.world_data

logger = logging.getLogger("mainLogger")


class Game:
    """Ultimate class for Life, the Universe, and Everything."""

    def __init__(self, host: data_structures.host.Host,
                 hero: data_structures.hero.Hero):
        """
        Create game.

        :param host: where to connect to
        :param hero: to connect as who
        """
        self.data: GameData = GameData(host=host, hero=hero)

        self.to_send_packets: queue.Queue = queue.Queue()
        self.received_packets: queue.Queue = queue.Queue()

        # TODO: Move mover to Hero.
        self.play_packet_creator: versions.base.VersionData.packet_creator.play \
            = self.data.version_data.packet_creator.play
        self.login_packet_creator: versions.base.VersionData.packet_creator.login \
            = self.data.version_data.packet_creator.login

        self.move_manager = action.move_manager.MoveManager(self.to_send_packets,
                                                            self.play_packet_creator,
                                                            self.data.hero)

        self._connection: connection.Connection = connection.Connection()

    def start(self) -> Union[str, None]:
        """
        Start game.

        :return: error message, otherwise None
        """
        # TODO: Change to try except custom exceptions.
        if not self._connect_to_server():
            return self.stop("Cannot connect to the server.")
        logger.info("Successfully connected to the server.")

        if not self._connection.start_listener(self.received_packets):
            return self.stop("Cannot start listener")
        logger.debug("Successfully started listening thread")

        if not self._connection.start_sender(self.to_send_packets):
            return self.stop("Cannot start sender")
        logger.debug("Successfully started sending thread")

        if not self._log_in():
            return self.stop("Cannot log in.")
        logger.info("Successfully logged in to server.")

        if not self.move_manager.start():
            return self.stop("Can't start move manager.")

        play_packets_specifics = self.data.version_data.packets_specifics["play"]

        packet_data_reader = PacketDataReader()
        packet_data_reader.set_compression_threshold(self._connection.compression_threshold)

        get_received_packet = self.received_packets.get
        while True:
            try:
                data = get_received_packet(timeout=20)
            except TimeoutError:
                return self.stop("Server timeout error.")

            if not data:
                return self.stop("Received 0 bytes")

            try:
                packet_data_reader.load(packet_data=memoryview(data))
            except InvalidUncompressedPacketError:
                return self.stop("Received packet with invalid compression.")

            if self.interpret_packet(packet_data_reader=packet_data_reader,
                                     state_packets_specifics=play_packets_specifics) == 5555:
                break

        return None

    def _log_in(self) -> bool:
        """
        Log-in into server.

        SUPPORT ONLY NON-PREMIUM.

        Establish connection with the server, and perform log in.
        In this part connection threshold (not necessary) will be set.

        :return success
        :rtype bool
        """
        # TODO: Change to auto-detect.
        if not self._login_non_premium():
            return False
        return True

    def stop(self, error_message: Any = None) -> Union[str, None]:
        """
        Stop everything. Close files, connections, etc. Return message.

        :param error_message: error message, leave None when normal exit
        :return passed message, None or error message
        """

        logger.info("Stopping bot %s. Reason: %s.",
                    self.data.hero.username, error_message)

        self._connection.close()
        self._connection = None

        return error_message

    def __del__(self):
        if self._connection is not None:
            self.stop()
    def _login_non_premium(self) -> bool:
        """
        # TODO: when login_premium done, write what da fuk is dat.
        # TODO: improve and simplify

        :return success
        :rtype bool
        """
        logger.info("Trying to log in in offline mode (non-premium).")

        self.to_send_packets.put(
            self.login_packet_creator.handshake(
                self.data.host.get_host_data()))

        self.to_send_packets.put(
            self.login_packet_creator.login_start(
                self.data.hero.username))

        packet_data_reader = PacketDataReader()
        packet_data_reader.set_compression_threshold(self._connection.compression_threshold)

        login_packets_specifics = self.data.version_data.packets_specifics["login"]
        # Try to log in for 50 sec (10 sec x 5 packets)
        for _ in range(5):
            try:
                data = self.received_packets.get(timeout=20)
            except TimeoutError:
                logger.error("TimeoutError while waiting for nonpremium login responses.")
                return False

            if not data:
                logger.error("Received 0 bytes")
                return False

            try:
                packet_data_reader.load(packet_data=memoryview(data))
            except InvalidUncompressedPacketError:
                logger.error("InvalidUncompressedPacketError while parsing nonpremium login responses.")
                return False

            try:
                result = self.interpret_packet(packet_data_reader=packet_data_reader,
                                               state_packets_specifics=login_packets_specifics)
            except DisconnectedByServerException:
                self.to_send_packets.put(b'')
                logger.error("DisconnectedByServerException")
                return False
            except Exception as err:
                logger.critical("<bot#1>Uncaught exception [%s] occurred: %s ",
                                err.__class__.__name__, err)
                # print("FOUND UNEXPECTED EXCEPTION\n" * 20)
                self.to_send_packets.put(b'')
                return False

            if result is True:
                return True
            if isinstance(result, int):
                self.data.world_data.compression_threshold = self._connection.compression_threshold = result
                packet_data_reader.set_compression_threshold(result)

        return False

    def _connect_to_server(self, timeout=5) -> bool:
        """
        Establish connection with the server.

        Not raises exceptions.

        :param timeout: connection timeout
        :returns: success
        :rtype: bool
        """
        try:
            self._connection.connect(self.data.host.get_host_data(), timeout)
        except OSError as err:
            logger.critical("Can't connect to: %s, reason: %s",
                            self.data.host.socket_data, err)
            return False

        logger.debug("Established connection with: %s", self.data.host.socket_data)
        return True

    def interpret_packet(self, packet_data_reader: PacketDataReader, state_packets_specifics: dict) -> Any:
        """
        Interpret packet data using list of actions.

        :param packet_data_reader: blob of uncompressed bytes
        :param state_packets_specifics: actions specific to state (play, login, status) and to packets
        """
        packet_id = packet_data_reader.extract_packet_id()
        if packet_id in state_packets_specifics:
            packet_specific: PacketSpecific = state_packets_specifics[packet_id]

            packet_specific.read_data(packet_data_reader.get_not_parsed_data())
            packet_specific.pre_handler(game_=self)
            default_handler_return = packet_specific.default_handler(game_=self)
            packet_specific.post_handler(game_=self)

            return default_handler_return

        return None

    # TODO: Move into reaction_list. Now only for testing.
    def on_death(self):
        """Define what to do when hero died."""
        logger.info("Player has dead. Respawning.")
        self.to_send_packets.put(self.play_packet_creator.client_status(0))
