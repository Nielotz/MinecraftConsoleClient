import versions.defaults.packet


class Packet(versions.defaults.packet.Packet):
    """ Translates packet name to packet_id (int varint) """

    class Login(versions.defaults.packet.Packet.Login):
        HANDSHAKE = LOGIN_START = b'\x00'

    class Status(versions.defaults.packet.Packet.Status):
        # TODO
        REQUEST = HANDSHAKE = TELEPORT_CONFIRM = b'\x00'

    class Play(versions.defaults.packet.Packet.Play):
        TELEPORT_CONFIRM = b'\x00'
        TABCOMPLETE = b'\x01'
        CHAT_MESSAGE = b'\x02'
        CLIENT_STATUS = b'\x03'
        CLIENT_SETTINGS = b'\x04'
        CONFIRM_TRANSACTION = b'\x05'
        ENCHANT_ITEM = b'\x06'
        CLICK_WINDOW = b'\x07'
        CLOSE_WINDOW = b'\x08'
        PLUGIN_MESSAGE = b'\x09'
        USE_ENTITY = b'\x0A'
        KEEP_ALIVE = b'\x0B'
        PLAYER = b'\x0C'
        PLAYER_POSITION = b'\x0D'
        PLAYER_POSITION_AND_LOOK = b'\x0E'
        PLAYER_LOOK = b'\x0F'
        VEHICLE_MOVE = b'\x10'
        STEER_BOAT = b'\x11'
        CRAFT_RECIPE_REQUEST = b'\x12'
        PLAYER_ABILITIES = b'\x13'
        PLAYER_DIGGING = b'\x14'
        ENTITY_ACTION = b'\x15'
        STEER_VEHICLE = b'\x16'
        CRAFTING_BOOK_DATA = b'\x17'
        RESOURCE_PACK_STATUS = b'\x18'
        ADVANCEMENT_TAB = b'\x19'
        HELD_ITEM_CHANGE = b'\x1A'
        CREATIVE_INVENTORY_ACTION = b'\x1B'
        UPDATE_SIGN = b'\x1C'
        ANIMATION = b'\x1d'
        SPECTATE = b'\x1e'
        PLAYER_BLOCK_PLACEMENT = b'\x1f'
        USE_ITEM = b'\20'
