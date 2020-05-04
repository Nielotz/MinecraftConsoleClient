import logging

from connection import Connection
from player import Player
from server import Server

from version import Version, VersionNamedTuple
from packet import PacketID, PacketIDNamedTuple
from state import State

import utils


def create_client(host: Server):
    # TODO:
    """
    Create object Client and load its settings from filename

    :return: Client
    """

    return Client(host, Version.V1_12_2)


class Client:
    """
    Main client action manager.
    Provides methods to control:
        client,
        client.player: Player.
    """

    player: Player = None
    _server: Server = None
    _connection: Connection = None
    _version: VersionNamedTuple = None

    def __init__(self, host: Server, version: Version):
        """
        :param host: Server object to which client connects to
        :param version: VersionNamedTuple object from VERSION,
                        tells which version of protocol to use
        """

        logging.info(f"Server address: '{host.socket_data[0]}:"
                     f"{host.socket_data[1]}'")

        self._server = host
        self._version = version.value
        self._connection = Connection()

    def login(self, player: Player):
        """
        Login to offline (non-premium) server e.g. without encryption, as player.

        :param player: Player
        :return True when logged in otherwise False
        :rtype bool
        """
        logging.info("Trying to log in in offline mode")

        if not self.__connect():
            return False
        self.player = player

        logging.info("Established connection with: "
                     f"'{self._server.socket_data[0]}:"
                     f"{self._server.socket_data[1]}'")

        self.__handshake()
        self.__send_login_start()
        is_logged = self.__handle_login_packets()
        return is_logged

    def __connect(self, timeout=5):
        """
        Connects to server.
        Not raise exceptions.

        :param timeout: connection timeout
        :returns True when connected, otherwise False
        :rtype bool
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

    def __handshake(self):
        """ Send handshake packet """
        data = [
            Version.V1_12_2.value.version_number_bytes,  # Protocol Version
            self._server.socket_data[0],  # Server Address
            self._server.socket_data[1],  # Server Port
            State.LOGIN.value  # Next State (login)
            ]
        self._connection.send(PacketID.HANDSHAKE, data)

    def __send_login_start(self):
        """ Send "login start" packet """
        data = [self.player.data["username"]]
        self._connection.send(PacketID.LOGIN_START, data)

    # TODO: Packets...
    def __handle_login_packets(self) -> bool:
        """
        Handle packets send by server during login process e.g.
        "Set Compression (optional)" and "Login Success"

        :returns True when successfully logged in, otherwise False
        :rtype bool
        """

        packet_length, data = self._connection.receive()

        # Protection from crash when server is starting
        if len(data) == 0:
            return False

        packet_id, data = utils.unpack_varint(data)

        logging.debug(f"[RECEIVED] ID: {packet_id}, payload: {bytes(data)}")

        if packet_id == PacketID.SET_COMPRESSION.value.int:
            threshold, _ = utils.unpack_varint(data)
            self._connection.set_compression(threshold)

            # Next packet have to be login success
            packet_length, data = self._connection.receive()
            packet_id, data = utils.extract_data(data,
                    compression=not (self._connection._compression_threshold < 0)
                                                 )

        logging.debug(f"[RECEIVED] ID: {packet_id}, payload: {bytes(data)}")

        if packet_id == 2:  # PacketID.LOGIN_SUCCESS.value:
            uuid, data = utils.extract_string_from_data(data)
            uuid = bytes(uuid).decode('utf-8')
            self.player.data["uuid"] = uuid
            logging.info(f"Player UUID: {uuid}")
            return True

        return False



