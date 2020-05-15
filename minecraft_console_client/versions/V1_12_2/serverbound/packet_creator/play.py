import misc.utils as utils
from versions.V1_12_2.serverbound.packet_id import play


def teleport_confirm(teleport_id: bytes) -> bytes:
    """ Return packet with confirmation for Player Position And Look. """
    return utils.pack_payload(play.TELEPORT_CONFIRM, [teleport_id])


def tabcomplete() -> bytes:
    packed_packet = b''
    return packed_packet


def chat_message() -> bytes:
    packed_packet = b''
    return packed_packet


def client_status() -> bytes:
    packed_packet = b''
    return packed_packet


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
    return utils.pack_payload(play.TELEPORT_CONFIRM, keep_alive_id)


def player() -> bytes:
    packed_packet = b''
    return packed_packet


def player_position() -> bytes:
    packed_packet = b''
    return packed_packet


def player_position_and_look() -> bytes:
    packed_packet = b''
    return packed_packet


def player_look() -> bytes:
    packed_packet = b''
    return packed_packet


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
