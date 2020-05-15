import logging

logger = logging.getLogger("mainLogger")

import versions.defaults.creator

from versions.V1_12_2.packet import Packet
from misc import utils


class Creator(versions.defaults.creator.Creator):
    """
    Namespace for serverbound packets (created and sent by client).
    Method names same as on minecraft protocol page.

    """

    class Login(versions.defaults.creator.Creator.Login):
        """ Namespace for packets used to login """

        @staticmethod
        def handshake(host: (str, int)) -> bytes:
            """ Returns handshake packet ready to send """
            login = b'\x02'
            data = [
                # Protocol Version
                versions.V1_12_2.VersionData.protocol_version_varint,
                host[0],  # Server Address
                host[1],  # Server Port
                login  # Next State (login)
            ]
            return utils.pack_payload(Packet.Login.HANDSHAKE, data)

        @staticmethod
        def login_start(username) -> bytes:
            """ Returns "login start" packet """
            return utils.pack_payload(Packet.Login.LOGIN_START,
                                      [username])

    class Status(versions.defaults.creator.Creator.Status):
        """ Namespace for packets used to receive status """

        # TODO

        @staticmethod
        def request() -> bytes:
            """ Returns request packet """
            return utils.pack_payload(Packet.Status.REQUEST, [])

        @staticmethod
        def ping(actual_time: float) -> bytes:
            """ Returns ping packet """
            packed_packet = utils.pack_payload(Packet.Status.PING,
                                               [actual_time])
            return packed_packet

        @staticmethod
        def handshake(host: (str, int)) -> bytes:
            """ Returns handshake packet """
            status = b'\x01'
            data = [
                # Protocol Version
                versions.V1_12_2.VersionData.protocol_version_varint,
                host[0],  # Server Address
                host[1],  # Server Port
                status  # Next State (login)
            ]

            return utils.pack_payload(Packet.Status.HANDSHAKE, data)

    class Play(versions.defaults.creator.Creator.Play):
        """ Namespace for packets used in play """

        @staticmethod
        def teleport_confirm(teleport_id: bytes) -> bytes:
            """ Return packet with confirmation for Player Position And Look. """
            return utils.pack_payload(Packet.Play.TELEPORT_CONFIRM,
                                      [teleport_id])

        @staticmethod
        def tabcomplete() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def chat_message() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def client_status() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def client_settings() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def confirm_transaction() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def enchant_item() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def click_window() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def close_window() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def plugin_message() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def use_entity() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def keep_alive(keep_alive_id: bytes) -> bytes:
            return utils.pack_payload(Packet.Play.TELEPORT_CONFIRM,
                                      keep_alive_id)

        @staticmethod
        def player() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def player_position() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def player_position_and_look() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def player_look() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def vehicle_move() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def steer_boat() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def craft_recipe_request() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def player_abilities() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def player_digging() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def entity_action() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def steer_vehicle() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def crafting_book_data() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def resource_pack_status() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def advancement_tab() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def held_item_change() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def creative_inventory_action() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def update_sign() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def animation() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def spectate() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def player_block_placement() -> bytes:
            packed_packet = b''
            return packed_packet

        @staticmethod
        def use_item() -> bytes:
            packed_packet = b''
            return packed_packet
