"""Provides functions which generate given packet."""
from data_structures.entity import Look
from data_structures.position import Position
from misc import converters
from versions.v1_12_2.packet.serverbound.create.packet_id import PLAY as PLAY_PACKETS_IDS


def teleport_confirm(teleport_id: bytes) -> bytes:
    """Return packet with confirmation for Player Position And Look."""

    return b''.join((PLAY_PACKETS_IDS.TELEPORT_CONFIRM, teleport_id))


def tabcomplete() -> bytes:
    packed_packet = b''
    return packed_packet


def chat_message() -> bytes:
    packed_packet = b''
    return packed_packet


def client_status(action_id: int) -> bytes:
    """Possible action_id: 0 (perform respawn), 1 (request stats)."""
    # action_id being converted to VarInt
    return b''.join((PLAY_PACKETS_IDS.CLIENT_STATUS, [b'\x00', b'\x01'][action_id]))


def client_settings() -> bytes:
    packed_packet = b''
    return packed_packet


def confirm_transaction() -> bytes:
    packed_packet = b''
    return packed_packet


def enchant_item() -> bytes:
    packed_packet = b''
    return packed_packet


def click_window() -> bytes:
    packed_packet = b''
    return packed_packet


def close_window() -> bytes:
    packed_packet = b''
    return packed_packet


def plugin_message() -> bytes:
    packed_packet = b''
    return packed_packet


def use_entity() -> bytes:
    packed_packet = b''
    return packed_packet


def keep_alive(keep_alive_id: bytes) -> bytes:
    return b''.join((PLAY_PACKETS_IDS.KEEP_ALIVE, keep_alive_id))


def player() -> bytes:
    packed_packet = b''
    return packed_packet


def player_position(position: Position, on_ground: bool) -> bytes:
    """
    :param position: (x, y, z) of destination
    :param on_ground: determines whether is player on ground
    """
    return b''.join((
        PLAY_PACKETS_IDS.PLAYER_POSITION,
        converters.pack_double(position.x),
        converters.pack_double(position.y),
        converters.pack_double(position.z),
        converters.pack_bool(on_ground)
    ))


def player_position_and_look_confirm(data: bytes, on_ground: bool = False):
    """
    Confirm for player_position_and_look sent by server.

    :param data: received data from server.
    :param on_ground: determines whether is player on ground
    """
    return b''.join((PLAY_PACKETS_IDS.PLAYER_POSITION_AND_LOOK,
                     data[:32],  # 2 floats, 3 doubles => 32 bytes
                     converters.pack_bool(on_ground)))


def player_position_and_look(position: Position,
                             look: Look,
                             on_ground: bool) -> bytes:
    """
    :param position: (x, y, z) of destination
    :param look: (yaw, pitch) how to set head
    :param on_ground: determines whether is player on ground
    """
    return b''.join((PLAY_PACKETS_IDS.PLAYER_POSITION_AND_LOOK,
                     converters.pack_double(position.x),
                     converters.pack_double(position.y),
                     converters.pack_double(position.z),
                     converters.pack_float(look.yaw),
                     converters.pack_float(look.pitch),
                     converters.pack_bool(on_ground))
                    )


def player_look(look: Look, on_ground: bool) -> bytes:
    return b''.join((PLAY_PACKETS_IDS.PLAYER_LOOK,
                     converters.pack_float(look.yaw),
                     converters.pack_float(look.pitch),
                     converters.pack_bool(on_ground))
                    )


def vehicle_move() -> bytes:
    packed_packet = b''
    return packed_packet


def steer_boat() -> bytes:
    packed_packet = b''
    return packed_packet


def craft_recipe_request() -> bytes:
    packed_packet = b''
    return packed_packet


def player_abilities() -> bytes:
    packed_packet = b''
    return packed_packet


def player_digging() -> bytes:
    packed_packet = b''
    return packed_packet


def entity_action() -> bytes:
    packed_packet = b''
    return packed_packet


def steer_vehicle() -> bytes:
    packed_packet = b''
    return packed_packet


def crafting_book_data() -> bytes:
    packed_packet = b''
    return packed_packet


def resource_pack_status() -> bytes:
    packed_packet = b''
    return packed_packet


def advancement_tab() -> bytes:
    packed_packet = b''
    return packed_packet


def held_item_change() -> bytes:
    packed_packet = b''
    return packed_packet


def creative_inventory_action() -> bytes:
    packed_packet = b''
    return packed_packet


def update_sign() -> bytes:
    packed_packet = b''
    return packed_packet


def animation() -> bytes:
    packed_packet = b''
    return packed_packet


def spectate() -> bytes:
    packed_packet = b''
    return packed_packet


def player_block_placement() -> bytes:
    packed_packet = b''
    return packed_packet


def use_item() -> bytes:
    packed_packet = b''
    return packed_packet
