import json
import time
import struct
import utils
from typing import Optional, Union

import logging


from connection import Connection
from player import Player
from hash_tables import PacketIDToBytes, PacketIDToInt


def get_status(address, port):
    """
    Create socket, connect to server, request for information.
    On success return json, on error False
    Should not raise exception

    :returns: False or server information
    :rtype: json
    """
    # Todo: add to json / log version in str sample: 1.12.2

    logging.info(f"Gathering data from: '{address}:{port}'")
    connection = Connection()

    logging.info(f"Connecting to: '{address}:{port}'")
    try:
        connection.connect((address, port), 5)  # Status request.
    except OSError as e:
        logging.error(f"Can't connect to: '{address}:{port}', reason: {e}")
        return False
    else:
        logging.info(f"Connected")

    data = [
        b"\x00",  # Protocol Version
        address,  # Server Address
        port,  # Server Port
        b"\x01"  # Next State (status)
        ]
    connection.send(PacketIDToBytes.HANDSHAKE, data)
    connection.send(PacketIDToBytes.HANDSHAKE, [])

    _, data = connection.read()

    # Send and read unix time
    connection.send(PacketIDToBytes.PING, [time.time() * 1000])
    _, unix = connection.read()

    # TODO: Fix JSONDecodeError("Expecting value", s, err.value) from None
    #   raised when server is starting

    # Load json and return
    response = json.loads(data.decode('utf8'))
    response['ping'] = int(time.time() * 1000) - struct.unpack('Q', unix)[0]

    try:
        logging.info(f"Server info: version: {response['version']} \n"
                     f"    ping:  {response['ping']}ms")  # \n for long name

    except:  # Issue with logging, e.g. some of response fields not exist
        pass

    return response


class Server:
    socket_data = None
    connection: Connection = None
    player: Player = None

    def __init__(self, host, port):
        # TODO change params to class IP with ip parser, etc.

        logging.info(f"Server address: '{host}:{port}'")

        self.socket_data = (host, port)
        self.connection = Connection()

    def _connect(self, timeout=5):
        try:
            self.connection.connect(self.socket_data, timeout)  # Status request.
        except OSError as e:
            logging.error(f"Can't connect to: "
                          f"'{self.socket_data[0]}:{self.socket_data[1]}'"
                          f", reason: {e}")
            return False
        return True

    def login(self, player: Player):
        if not self._connect():
            return False
        self.player = player
        logging.info("Established connection with: "
                     f"'{self.socket_data[0]}:{self.socket_data[1]}'")
        logging.info("Logging in offline mode: ")

        # 1. C→S: Handshake with Next State set to 2 (login)
        self.__handshake()
        # 2. C→S: Login Start
        self.__send_login_start(self.player.data["username"])

        self.__handle_login_packets()

    def __handle_login_packets(self):
        packet_length, data = self.connection.read()
        packet_id, data = utils.unpack_varint_new(data)
        logging.debug(f"[RECEIVED] ID: {packet_id}, payload: {bytes(data)}")

        if packet_id == PacketIDToInt.SET_COMPRESSION.value:
            threshold, _ = utils.unpack_varint_new(data)
            self.connection.set_compression(threshold)

            # Next packet have to be login success
            packet_length, data = self.connection.read()

        packet_id, data = utils.extract_data(data,
                    compression=not (self.connection.compression_threshold < 0)
                                             )

        logging.debug(f"[RECEIVED] ID: {packet_id}, payload: {bytes(data)}")

        if packet_id == 2:  # PacketID.LOGIN_SUCCESS.value:
            uuid, data = utils.extract_string_from_data(data)
            uuid = bytes(uuid).decode('utf-8')
            self.player.data["uuid"] = uuid
            logging.info(f"Player UUID: {uuid}")
            return True

        return False


    def __handle_packet(self, packet_id: PacketIDToBytes, data: bytes):
        pass

    def __handshake(self):
        data = [
            utils.convert_to_varint(340),  # Protocol Version
            self.socket_data[0],  # Server Address
            self.socket_data[1],  # Server Port
            b"\x02"  # Next State (login)
            ]
        self.connection.send(PacketIDToBytes.HANDSHAKE, data)

    def __send_login_start(self, username):
        data = [username]
        self.connection.send(PacketIDToBytes.LOGIN_START, data)




