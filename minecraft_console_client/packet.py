from collections import namedtuple
from enum import Enum
import logging
logger = logging.getLogger('mainLogger')

from version import VersionNamedTuple, Version
from state import State
import utils

PacketIDNamedTuple = namedtuple("PacketIDNamedTuple", "int bytes")


class PacketID(Enum):
    """
    Packet name => PacketIDNamedTuple(int, hex byte value in two's complement)
    """

    REQUEST = PacketIDNamedTuple(0, b'\x00')
    HANDSHAKE = PacketIDNamedTuple(0, b'\x00')
    LOGIN_START = PacketIDNamedTuple(0, b'\x00')
    TELEPORT_CONFIRM = PacketIDNamedTuple(0, b'\x00')
    DISCONNECT_LOGIN = PacketIDNamedTuple(0, b'\x00')
    PING = PacketIDNamedTuple(0, b'\x01')
    LOGIN_SUCCESS = PacketIDNamedTuple(2, b'\x02')
    CHAT_MESSAGE_SERVERBOUND = PacketIDNamedTuple(2, b'\x02')
    CLIENT_STATUS = PacketIDNamedTuple(3, b'\x03')
    SET_COMPRESSION = PacketIDNamedTuple(3, b'\x03')
    CLIENT_SETTINGS = PacketIDNamedTuple(4, b'\x04')
    PLUGIN_MESSAGE_SERVERBOUND = PacketIDNamedTuple(9, b'\x09')
    KEEP_ALIVE_SERVERBOUND = PacketIDNamedTuple(11, b'\x0b')
    CHAT_MESSAGE_CLIENTBOUND = PacketIDNamedTuple(15, b'\x0F')
    OPEN_WINDOW = PacketIDNamedTuple(19, b'\x13')
    PLUGIN_MESSAGE_CLIENTBOUND = PacketIDNamedTuple(15, b'\x18')
    DISCONNECT_PLAY = PacketIDNamedTuple(26, b'\x1A')
    CHANGE_GAME_STATE = PacketIDNamedTuple(30, b'\x1E')
    KEEP_ALIVE_CLIENTBOUND = PacketIDNamedTuple(31, b'\x1F')
    JOIN_GAME = PacketIDNamedTuple(35, b'\x23')
    PLAYER_POSITION_AND_LOOK = PacketIDNamedTuple(47, b'\x2F')
    RESPAWN = PacketIDNamedTuple(53, b'\x35')
    PLAYER_LIST_HEADER_AND_FOOTER = PacketIDNamedTuple(74, b'\x4A')


def _pack_payload(packet_id: PacketID, arr_with_payload):
    """
    Stolen from
    https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0
    """
    data = bytearray(packet_id.value.bytes)
    logger.debug(f"[SEND] {packet_id.name} {arr_with_payload}")

    for arg in arr_with_payload:
        data.extend(utils.pack_data(arg))

    # logger.debug(f"[PACKED] {data}")

    return data


class Creator:
    """ Namespace for creating packets """

    class Login:
        """ Namespace for packets used to login """

        @staticmethod
        def handshake(server_data: (str, int),
                      protocol_version: VersionNamedTuple) -> bytearray:
            """ Returns handshake packet ready to send """
            data = [
                protocol_version.version_number_bytes,  # Protocol Version
                server_data[0],  # Server Address
                server_data[1],  # Server Port
                State.LOGIN.value  # Next State (login)
                ]
            packed_packet = _pack_payload(PacketID.HANDSHAKE, data)

            return packed_packet

        @staticmethod
        def login_start(username):
            """ Returns "login start" packet """
            packed_packet = _pack_payload(PacketID.LOGIN_START, [username])
            return packed_packet

    class Status:
        """ Namespace for packets used to receive status """

        @staticmethod
        def request():
            """ Returns request packet """
            packed_packet = _pack_payload(PacketID.REQUEST, [])
            return packed_packet

        @staticmethod
        def ping(actual_time: float):
            """ Returns ping packet """
            packed_packet = _pack_payload(PacketID.PING, [actual_time])
            return packed_packet

        @staticmethod
        def handshake(server_data: (str, int),
                      protocol_version: Version) -> bytearray:
            """ Returns handshake packet """
            data = [
                protocol_version.value.version_number_bytes,  # Protocol Version
                server_data[0],  # Server Address
                server_data[1],  # Server Port
                State.STATUS.value  # Next State (login)
                ]
            packed_packet = _pack_payload(PacketID.HANDSHAKE, data)

            return packed_packet

