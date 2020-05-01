from collections import namedtuple
from enum import Enum

PacketIDNamedTuple = namedtuple("PacketIDNamedTuple", "int bytes")


class PacketID(Enum):
    """Packet name => packet id: <binary hex byte value in two's complement>"""
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
