from collections import namedtuple

import versions.defaults.packet

PacketIDNamedTuple = namedtuple("PacketIDNamedTuple", "int bytes")


class Packet(versions.defaults.packet.Packet):
    """ Translates packet name to packet_id (int varint) """

    class Login(versions.defaults.packet.Packet.Login):
        HANDSHAKE = LOGIN_START = PacketIDNamedTuple(0, b'\x00')

    class Status(versions.defaults.packet.Packet.Status):
        # TODO
        REQUEST = HANDSHAKE = TELEPORT_CONFIRM \
            = PacketIDNamedTuple(0, b'\x00')

    class Play(versions.defaults.packet.Packet.Play):
        TELEPORT_CONFIRM = PacketIDNamedTuple(0, b'\x00')
        TABCOMPLETE = PacketIDNamedTuple(1, b'\x01')
        CHAT_MESSAGE = PacketIDNamedTuple(2, b'\x02')
        CLIENT_STATUS = PacketIDNamedTuple(3, b'\x03')
        CLIENT_SETTINGS = PacketIDNamedTuple(4, b'\x04')
        CONFIRM_TRANSACTION = PacketIDNamedTuple(5, b'\x05')
        ENCHANT_ITEM = PacketIDNamedTuple(6, b'\x06')
        CLICK_WINDOW = PacketIDNamedTuple(7, b'\x07')
        CLOSE_WINDOW = PacketIDNamedTuple(8, b'\x08')
        PLUGIN_MESSAGE = PacketIDNamedTuple(9, b'\x09')
        USE_ENTITY = PacketIDNamedTuple(10, b'\x0A')
        KEEP_ALIVE = PacketIDNamedTuple(11, b'\x0B')
        PLAYER = PacketIDNamedTuple(12, b'\x0C')
        PLAYER_POSITION = PacketIDNamedTuple(13, b'\x0D')
        PLAYER_POSITION_AND_LOOK = PacketIDNamedTuple(14, b'\x0E')
        PLAYER_LOOK = PacketIDNamedTuple(15, b'\x0F')
        VEHICLE_MOVE = PacketIDNamedTuple(16, b'\x10')
        STEER_BOAT = PacketIDNamedTuple(17, b'\x11')
        CRAFT_RECIPE_REQUEST = PacketIDNamedTuple(18, b'\x12')
        PLAYER_ABILITIES = PacketIDNamedTuple(19, b'\x13')
        PLAYER_DIGGING = PacketIDNamedTuple(20, b'\x14')
        ENTITY_ACTION = PacketIDNamedTuple(21, b'\x15')
        STEER_VEHICLE = PacketIDNamedTuple(22, b'\x16')
        CRAFTING_BOOK_DATA = PacketIDNamedTuple(23, b'\x17')
        RESOURCE_PACK_STATUS = PacketIDNamedTuple(24, b'\x18')
        ADVANCEMENT_TAB = PacketIDNamedTuple(25, b'\x19')
        HELD_ITEM_CHANGE = PacketIDNamedTuple(26, b'\x1A')
        CREATIVE_INVENTORY_ACTION = PacketIDNamedTuple(27, b'\x1B')
        UPDATE_SIGN = PacketIDNamedTuple(28, b'\x1C')
        ANIMATION = PacketIDNamedTuple(29, b'\x1d')
        SPECTATE = PacketIDNamedTuple(30, b'\x1e')
        PLAYER_BLOCK_PLACEMENT = PacketIDNamedTuple(31, b'\x1f')
        USE_ITEM = PacketIDNamedTuple(32, b'\20')
