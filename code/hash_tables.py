from enum import Enum


class PacketName(Enum):
    """Packet name => packet id: <binary hex byte value in two's complement>"""

    HANDSHAKE = b'0x00'
    LOGIN_START = b'0x00'
    TELEPORT_CONFIRM = b'0x00'
    DISCONNECT_LOGIN = b'0x00'
    CHAT_MESSAGE_SERVERBOUND = b'0x02'
    LOGIN_SUCCESS = b'0x02'
    SET_COMPRESSION = b'0x03'
    CLIENT_STATUS = b'0x03'
    CLIENT_SETTINGS = b'0x04'
    PLUGIN_MESSAGE_SERVERBOUND = b'0x09'
    KEEP_ALIVE_SERVERBOUND = b'0x0B'
    CHAT_MESSAGE_CLIENTBOUND = b'0x0F'
    OPEN_WINDOW = b'0x13'
    PLUGIN_MESSAGE_CLIENTBOUND = b'0x18'
    DISCONNECT_PLAY = b'0x1A'
    CHANGE_GAME_STATE = b'0x1E'
    KEEP_ALIVE_CLIENTBOUND = b'0x1F'
    JOIN_GAME = b'0x23'
    PLAYER_POSITION_AND_LOOK = b'0x2F'
    RESPAWN = b'0x35'
    PLAYER_LIST_HEADER_AND_FOOTER = b'0x4A'

print(len(PacketName.RESPAWN.value))