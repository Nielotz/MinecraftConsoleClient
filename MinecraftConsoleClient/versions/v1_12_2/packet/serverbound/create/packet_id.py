from typing import NamedTuple

"""Contain packet name translated to its id."""


class STATUS(NamedTuple):
    pass


class LOGIN(NamedTuple):
    HANDSHAKE: bytes = b'\x00'
    LOGIN_START: bytes = b'\x00'


class PLAY(NamedTuple):
    TELEPORT_CONFIRM: bytes = b'\x00'
    # TABCOMPLETE: bytes = b'\x01'
    # CHAT_MESSAGE: bytes = b'\x02'
    CLIENT_STATUS: bytes = b'\x03'
    # CLIENT_SETTINGS: bytes = b'\x04'
    # CONFIRM_TRANSACTION: bytes = b'\x05'
    # ENCHANT_ITEM: bytes = b'\x06'
    # CLICK_WINDOW: bytes = b'\x07'
    # CLOSE_WINDOW: bytes = b'\x08'
    # PLUGIN_MESSAGE: bytes = b'\x09'
    # USE_ENTITY: bytes = b'\x0A'
    KEEP_ALIVE: bytes = b'\x0B'
    # PLAYER: bytes = b'\x0C'
    PLAYER_POSITION: bytes = b'\x0D'
    PLAYER_POSITION_AND_LOOK: bytes = b'\x0E'
    PLAYER_LOOK: bytes = b'\x0F'
    # VEHICLE_MOVE: bytes = b'\x10'
    # STEER_BOAT: bytes = b'\x11'
    # CRAFT_RECIPE_REQUEST: bytes = b'\x12'
    # PLAYER_ABILITIES: bytes = b'\x13'
    # PLAYER_DIGGING: bytes = b'\x14'
    # ENTITY_ACTION: bytes = b'\x15'
    # STEER_VEHICLE: bytes = b'\x16'
    # CRAFTING_BOOK_DATA: bytes = b'\x17'
    # RESOURCE_PACK_STATUS: bytes = b'\x18'
    # ADVANCEMENT_TAB: bytes = b'\x19'
    # HELD_ITEM_CHANGE: bytes = b'\x1A'
    # CREATIVE_INVENTORY_ACTION: bytes = b'\x1B'
    # UPDATE_SIGN: bytes = b'\x1C'
    # ANIMATION: bytes = b'\x1d'
    # SPECTATE: bytes = b'\x1e'
    # PLAYER_BLOCK_PLACEMENT: bytes = b'\x1f'
    # USE_ITEM: bytes = b'\x20'
