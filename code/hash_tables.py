from enum import Enum, IntEnum


class PacketIDToBytes(Enum):
    """Packet name => packet id: <binary hex byte value in two's complement>"""
    REQUEST = b'\x00'
    HANDSHAKE = b'\x00'
    LOGIN_START = b'\x00'
    TELEPORT_CONFIRM = b'\x00'
    DISCONNECT_LOGIN = b'\x00'
    PING = b'\x01'
    LOGIN_SUCCESS = b'\x02'
    CHAT_MESSAGE_SERVERBOUND = b'\x02'
    CLIENT_STATUS = b'\x03'
    SET_COMPRESSION = b'\x03'
    CLIENT_SETTINGS = b'\x04'
    PLUGIN_MESSAGE_SERVERBOUND = b'\x09'
    KEEP_ALIVE_SERVERBOUND = b'\x0b'
    CHAT_MESSAGE_CLIENTBOUND = b'\x0F'
    OPEN_WINDOW = b'\x13'
    PLUGIN_MESSAGE_CLIENTBOUND = b'\x18'
    DISCONNECT_PLAY = b'\x1A'
    CHANGE_GAME_STATE = b'\x1E'
    KEEP_ALIVE_CLIENTBOUND = b'\x1F'
    JOIN_GAME = b'\x23'
    PLAYER_POSITION_AND_LOOK = b'\x2F'
    RESPAWN = b'\x35'
    PLAYER_LIST_HEADER_AND_FOOTER = b'\x4A'


class PacketIDToInt(IntEnum):
    HANDSHAKE = 0
    LOGIN_START = 0
    TELEPORT_CONFIRM = 0
    DISCONNECT_LOGIN = 0
    PING = 1
    CHAT_MESSAGE_SERVERBOUND = 2
    LOGIN_SUCCESS = 2
    SET_COMPRESSION = 3
    CLIENT_STATUS = 3
    CLIENT_SETTINGS = 4
    PLUGIN_MESSAGE_SERVERBOUND = 9
    KEEP_ALIVE_SERVERBOUND = 11
    CHAT_MESSAGE_CLIENTBOUND = 15
    OPEN_WINDOW = 19
    PLUGIN_MESSAGE_CLIENTBOUND = 24
    DISCONNECT_PLAY = 26
    CHANGE_GAME_STATE = 30
    KEEP_ALIVE_CLIENTBOUND = 31
    JOIN_GAME = 35
    PLAYER_POSITION_AND_LOOK = 47
    RESPAWN = 53
    PLAYER_LIST_HEADER_AND_FOOTER = 74


class ProtocolVersion(IntEnum):
    ANY = 999
    V1_15_2 = 578
    V1_15_1 = 575
    V1_15 = 573
    V1_14_4 = 498
    V1_14_3 = 490
    V1_14_2 = 485
    V1_14_1 = 480
    V1_14 = 477
    V1_13_2 = 404
    V1_13_1 = 401
    V1_13 = 393
    V1_12_2 = 340
    V1_12_1 = 338
    V1_12 = 335
    V1_11_2 = 316
    V1_11_1 = 316
    V1_11 = 315
    V1_10_2 = 210
    V1_10_1 = 210
    V1_10 = 210
    V1_9_4 = 110
    V1_9_3 = 110
    V1_9_2 = 109
    V1_9_1 = 108
    V1_9 = 107
    V1_8_9 = 47
    V1_8_8 = 47
    V1_8_7 = 47
    V1_8_6 = 47
    V1_8_5 = 47
    V1_8_4 = 47
    V1_8_3 = 47
    V1_8_2 = 47
    V1_8_1 = 47
    V1_8 = 47
    V1_7_10 = 5
    V1_7_9 = 5
    V1_7_8 = 5
    V1_7_7 = 5
    V1_7_6 = 5
    V1_7_5 = 4
    V1_7_4 = 4
    # V1_7_3 NOT EXIST
    V1_7_2 = 4


class State(Enum):
    REQUEST = b'\x01'
    PING = b'\x01'
    LOGIN = b'\x02'
