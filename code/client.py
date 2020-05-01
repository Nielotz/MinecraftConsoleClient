import logging

from connection import Connection
from player import Player
from hash_tables import PacketIDToBytes, PacketIDToInt, State
from server import Server
import utils


class Client:
    """Main connection manager between mc server and this client."""
    _server = None
    _connection: Connection = None
    _player: Player = None

    def __init__(self, host: Server):
        """host: Server obj to connect to."""

        logging.info(f"Server address: '{host.socket_data[0]}:"
                     f"{host.socket_data[1]}'")

        self._server = host
        self._connection = Connection()

    def login(self, player: Player):
        """Login to offline(non-premium) server e.g. without encryption,
        using player data.
        :raises

        :param player: Player
        :return: True when logged in otherwise False
        :rtype: bool
        """
        logging.info("Trying to log in in offline mode")

        if not self._connect():
            return False
        self._player = player

        logging.info("Established connection with: "
                     f"'{self._server.socket_data[0]}:"
                     f"{self._server.socket_data[1]}'")

        self.__handshake()
        self.__send_login_start()
        is_logged = self.__handle_login_packets()
        return is_logged

    def _connect(self, timeout=5):
        """Connect to server.
        Not raise exceptions.

        :returns: True when connected, otherwise False.
        :type: bool
        """
        try:
            self._connection.connect(self._server.socket_data, timeout)
        except OSError as e:
            logging.critical(f"Can't connect to: "
                             f"'{self._server.socket_data[0]}:"
                             f"{self._server.socket_data[1]}'"
                             f", reason: {e}")
            return False
        return True

    def __handle_login_packets(self):
        """Handle packets send by server during login process e.g.
        "Set Compression (optional)" and "Login Success"

        :returns: True when successfully logged in, otherwise False.
        :type: bool
        """
        packet_length, data = self._connection.receive()
        # Protection from crash when server is starting
        if len(data) == 0:
            return False
        packet_id, data = utils.unpack_varint(data)

        logging.debug(f"[RECEIVED] ID: {packet_id}, payload: {bytes(data)}")

        if packet_id == PacketIDToInt.SET_COMPRESSION.value:
            threshold, _ = utils.unpack_varint(data)
            self._connection.set_compression(threshold)

            # Next packet have to be login success
            packet_length, data = self._connection.receive()
            packet_id, data = utils.extract_data(data,
                    compression=not (self._connection.compression_threshold < 0)
                                                 )

        logging.debug(f"[RECEIVED] ID: {packet_id}, payload: {bytes(data)}")

        if packet_id == 2:  # PacketID.LOGIN_SUCCESS.value:
            uuid, data = utils.extract_string_from_data(data)
            uuid = bytes(uuid).decode('utf-8')
            self._player.data["uuid"] = uuid
            logging.info(f"Player UUID: {uuid}")
            return True

        return False

    def __handshake(self):
        """Send handshake packet"""
        data = [
            utils.convert_to_varint(340),  # Protocol Version
            self._server.socket_data[0],  # Server Address
            self._server.socket_data[1],  # Server Port
            State.LOGIN.value  # Next State (login)
            ]
        self._connection.send(PacketIDToBytes.HANDSHAKE, data)

    def __send_login_start(self):
        """Send "login start" packet"""
        data = [self._player.data["username"]]
        self._connection.send(PacketIDToBytes.LOGIN_START, data)




