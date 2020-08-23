"""
Container for game class.

Everything what is happening, happens here.
Everything what is controlled, is controlled here.
"""

import logging
import queue
import zlib
from typing import Any, Union, TYPE_CHECKING

import action.move_manager
import connection
import data_structures.host
import data_structures.player
import misc.converters as converters
import versions.defaults
import versions.version
from misc.exceptions import DisconnectedError
from misc.exceptions import InvalidUncompressedPacketError

if TYPE_CHECKING:
    import versions.defaults.data_structures.game_data

logger = logging.getLogger("mainLogger")


class Game:
    """Ultimate class for Life, the Universe, and Everything."""

    host: data_structures.host.Host = None
    version_data: versions.defaults.VersionData = None
    player: data_structures.player.Player = None
    game_data: versions.defaults.data_structures.game_data.GameData = None

    # Serverbound
    _login_packet_creator: versions.defaults.VersionData.packet_creator.login \
        = None  # Module
    _play_packet_creator: versions.defaults.VersionData.packet_creator.play \
        = None  # Module

    # Clientbound
    # versions.defaults.VersionData.action_list[stage]
    # where stage in ("login", "play", "status")
    _action_list: dict = None

    received_packets: queue.Queue = None
    to_send_packets: queue.Queue = None

    _conn: connection.Connection = None

    def __init__(self,
                 host: data_structures.host.Host,
                 player: data_structures.player.Player,
                 game_version: versions.version.Version):
        """
        Create game.

        :param host: where to connect to
        :param player: to connect as who
        :param game_version: to connect in which game version
        """
        self.host = host
        # TODO: check is server responding / online
        self.player = player
        # TODO: check username
        self.version_data = game_version.value
        # TODO: check is game data valid, then remove other checks
        self.game_data = versions.defaults.data_structures.game_data.GameData()

        logger.info(
            """
%s
| %s |
| %s |
| %s |
%s
""",
            "Created bot".center(80, "-"),
            f"Username: '{player.data.username}'".center(78, " "),
            f"Client version: '{self.version_data.release_name}'".center(
                78, " "),
            f"Socket data: {self.host.socket_data}".center(78, " "),
            "".center(80, "-")
        )

        # Check does play exist in action_packet.
        if not self._switch_action_packets("play"):
            raise RuntimeError("Not found 'play' in action_packet. "
                               f"Game version: {self.version_data}")

        # Switch to login packet type.
        if not self._switch_action_packets("login"):
            raise RuntimeError("Not found 'login' in action_packet. "
                               f"Game version: {self.version_data}")

        self.play_packet_creator = self.version_data.packet_creator.play
        self.login_packet_creator = self.version_data.packet_creator.login

        self._conn = connection.Connection()

        self.to_send_packets = queue.Queue()
        self.received_packets = queue.Queue()

        self.move_manager = action.move_manager.MoveManager(
            self.to_send_packets,
            self.play_packet_creator,
            self.player.data)

    def start(self) -> Union[str, None]:
        """
        Start game.

        :return: error message, otherwise None
        """
        if not self._connect_to_server():
            return self.stop("Cannot connect to the server.")
        logger.info("Successfully connected to the server.")

        if not self._conn.start_listener(self.received_packets):
            return self.stop("Cannot start listener")
        logger.debug("Successfully started listening thread")

        if not self._conn.start_sender(self.to_send_packets):
            return self.stop("Cannot start sender")
        logger.debug("Successfully started sending thread")

        if not self._log_in():
            return self.stop("Cannot log in.")
        logger.info("Successfully logged in to server.")

        self._switch_action_packets("play")

        if not self.move_manager.start():
            return self.stop("Can't start move manager.")

        # TODO: Add reaction_list, user_action_list, or other shit.
        while True:
            try:
                data = self.received_packets.get(timeout=20)
            except TimeoutError:
                return self.stop("Server timeout error.")

            if not data:
                return self.stop("Received 0 bytes")

            if not self._conn.compression_threshold < 0:
                try:
                    data = self._decompress_packet(data)
                except InvalidUncompressedPacketError:
                    return self.stop(
                        "Received packet with invalid compression.")

            # Decompression needs to be done before this!
            packet_id, packet = converters.extract_varint(data)

            if self._interpret_packet(packet_id, packet) == 5555:
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
                    self.player.data.username, error_message)

        self._conn.close()
        self._conn: None = None

        return error_message

    def __del__(self):
        if self._conn is not None:
            self.stop()

    def _switch_action_packets(self, actions_type: str = "login") -> bool:
        """
        Switch between different action types.

        To see possible action types see:
            versions.<version>.clientbound.action_list.py

        Based on v1_12_2:
            Possible types: login, play, status.

        :return success
        :rtype bool
        """
        self._action_list = \
            self.version_data.action_list.get(actions_type)
        return self._action_list is not None

    def _login_non_premium(self) -> bool:
        """
        #TODO: when login_premium done, write what da fuk is dat.
        #TODO: improve and simplify

        :return success
        :rtype bool
        """
        logger.info("Trying to log in in offline mode (non-premium).")

        self.to_send_packets.put(
            self.login_packet_creator.handshake(self.host.get_host_data()))

        self.to_send_packets.put(
            self.login_packet_creator.login_start(
                self.player.data.username))

        # Try to log in for 50 sec (10 sec x 5 packets)
        for _ in range(5):
            data = self.received_packets.get(timeout=10)
            if not data:
                logger.error("Received 0 bytes")
                return False

            try:
                packet = self._decompress_packet(data)
            except InvalidUncompressedPacketError:
                return False

            packet_id, data = converters.extract_varint(packet)
            # print(packet_id, data)
            try:
                result = self._interpret_packet(packet_id, data)
            except DisconnectedError:
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
                self.game_data.compression_threshold = result
                self._conn.compression_threshold = result

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
            self._conn.connect(self.host.get_host_data(), timeout)
        except OSError as err:
            logger.critical("Can't connect to: %s, reason: %s",
                            self.host.socket_data, err)
            return False

        logger.debug("Established connection with: %s", self.host.socket_data)
        return True

    def _interpret_packet(self, packet_id: int, payload: bytes) -> Any:
        """
        Interpret given packet and call function assigned \
        to packet_id in action_list, then return function return.

        If compression threshold is not negative - uncompress.

        :param packet_id: int representing packet id e.g 0,1,2,3,4...
        :param payload: uncompressed data
        :return: whatever action_list[packet_id]() returns
        """

        if packet_id in self._action_list:
            return self._action_list[packet_id](self, payload)

        # logger.debug("Packet with id: %s is not implemented yet", packet_id)
        return None

    def _decompress_packet(self, packet: bytes) -> bytes:
        """Decompress packet, and return it."""
        threshold = self.game_data.compression_threshold

        # If compression is enabled.
        if threshold < 0:
            return packet

        data_length, packet = converters.extract_varint(packet)

        if data_length == 0:  # Packet is not compressed.
            return packet

        packet = zlib.decompress(packet)

        if len(packet) < threshold:
            logger.critical("Received invalid packet.")
            # TODO: to improve performance:
            #   change try except to if
            #   move extraction into _interpret_packet
            raise InvalidUncompressedPacketError("Received invalid packet.")

        return packet
        # End of decompression

    # TODO: Move into reaction_list. Now only for testing.
    def on_death(self):
        """Define what to do when player died."""
        logger.info("Player has dead. Respawning.")
        self.to_send_packets.put(self.play_packet_creator.client_status(0))
