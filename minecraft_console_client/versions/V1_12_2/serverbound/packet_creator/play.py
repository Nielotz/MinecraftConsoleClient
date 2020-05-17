import misc.utils as utils
from versions.V1_12_2.serverbound.packet_id import play
from data_structures.position import Position


def teleport_confirm(teleport_id: bytes) -> bytes:
    """ Return packet with confirmation for Player Position And Look. """
    return utils.pack_data(play.TELEPORT_CONFIRM, [teleport_id])


def tabcomplete() -> bytes:
    packed_packet = b''
    return packed_packet


def chat_message() -> bytes:
    packed_packet = b''
    return packed_packet


def client_status(action_id: int) -> bytes:
    try:
        ac_id = [b'\x00', b'\x01'][action_id]
    except IndexError:
        ac_id = utils.convert_to_varint(action_id)
    return utils.pack_data(play.CLIENT_STATUS, [ac_id])


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
    return utils.pack_data(play.TELEPORT_CONFIRM, keep_alive_id)


def player() -> bytes:
    packed_packet = b''
    return packed_packet


def player_position(position: Position, on_ground: bool) -> bytes:
    return b''.join((play.PLAYER_POSITION,
                     utils.pack_double(position.x),
                     utils.pack_double(position.y),
                     utils.pack_double(position.z),
                     utils.pack_bool(on_ground))
                    )


def player_position_and_look(position: Position, on_ground: bool) -> bytes:
    return b''.join((play.PLAYER_POSITION_AND_LOOK,
                     utils.pack_double(position.x),
                     utils.pack_double(position.y),
                     utils.pack_double(position.z),
                     utils.pack_float(position.yaw),
                     utils.pack_float(position.pitch),
                     utils.pack_bool(on_ground))
                    )


def player_look(position: Position, on_ground: bool) -> bytes:
    return b''.join((play.PLAYER_LOOK,
                     utils.pack_float(position.yaw),
                     utils.pack_float(position.pitch),
                     utils.pack_bool(on_ground))
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
