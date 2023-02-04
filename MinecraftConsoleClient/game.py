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
from data_structures.packet_data_reader import PacketDataReader, TypeToExtract
from misc.exceptions import DisconnectedByServerException, InvalidUncompressedPacketError

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

        action_list_play = self.data.version_data.action_list["play"]
        while True:
            try:
                data = self.received_packets.get(timeout=20)
            except TimeoutError:
                return self.stop("Server timeout error.")

            if not data:
                return self.stop("Received 0 bytes")

            packet_data_reader = PacketDataReader(data)

            if not self._connection.compression_threshold < 0:
                try:
                    packet_data_reader.decompress()
                except InvalidUncompressedPacketError:
                    return self.stop("Received packet with invalid compression.")

            if self.interpret_packet(packet_data_reader=packet_data_reader, action_list=action_list_play) == 5555:
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
            self.login_packet_creator.handshake(self.data.host.get_host_data()))

        self.to_send_packets.put(
            self.login_packet_creator.login_start(
                self.data.hero.username))

        action_list_login = self.data.version_data.action_list["login"]
        # Try to log in for 50 sec (10 sec x 5 packets)
        for _ in range(5):
            data = self.received_packets.get(timeout=10)
            if not data:
                logger.error("Received 0 bytes")
                return False

            packet_data_reader = PacketDataReader(data)

            try:
                packet_data_reader.decompress()
            except InvalidUncompressedPacketError:
                return False

            try:
                result = self.interpret_packet(packet_data_reader=packet_data_reader, action_list=action_list_login)
            except DisconnectedByServerException:
                self.to_send_packets.put(b'')
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

    def interpret_packet(self, packet_data_reader: PacketDataReader, action_list: dict) -> Any:
        """
        Interpret packet data using list of actions.

        :param packet_data_reader: blob of uncompressed bytes
        :param action_list: list of actions used to parse given packet
        """
        packet_id = packet_data_reader.extract(TypeToExtract.PACKET_ID)
        if packet_id in action_list:
            return action_list[packet_id](self, packet_data_reader)
        return None

    # TODO: Move into reaction_list. Now only for testing.
    def on_death(self):
        """Define what to do when hero died."""
        logger.info("Player has dead. Respawning.")
        self.to_send_packets.put(self.play_packet_creator.client_status(0))
