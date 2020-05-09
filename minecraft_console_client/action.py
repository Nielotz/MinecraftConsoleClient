import logging

logger = logging.getLogger('mainLogger')

from exceptions import DisconnectedError
from version import VersionNamedTuple, Version
from enum import Enum
import utils

""" Actions possible to happen, e.g. packets available to be received/sent. """


class Server:
    """
    Namespace for server-side events.
    Method names taken from minecraft protocol page.

    :params player: Player on which process packet.
    :params bytes: Data received from server, uncompressed, without packet id.
    """

    @staticmethod
    def server_difficulty(player, data: bytes):
        player._server_data["difficulty"], data = \
            utils.extract_unsigned_byte(data)
        logger.debug("[2/2] Changed difficulty")

    @staticmethod
    def not_implemented(*args):
        logger.debug("[2/2] Not implemented yet")

    @staticmethod
    def disconnect(player, data: bytes):
        reason = utils.extract_json_from_chat(data)
        # reason should be dict Chat type.
        logger.error(f"[2/2] {player._data['username']} has been "
                     f"disconnected by server. Reason: '{reason['text']}'")
        raise DisconnectedError("Disconnected by server.")

    @staticmethod
    def login_success(player, data: bytes):
        uuid, data = utils.extract_string_from_data(data)
        uuid = uuid.decode('utf-8')
        player._data["uuid"] = uuid
        logger.debug("[2/2] Successfully logged to the server")
        return True

    @staticmethod
    def set_compression(player, data: bytes):
        threshold, _ = utils.unpack_varint(data)
        player._conn.set_compression(threshold)

        if threshold < 0:
            logger.debug(f"[2/2] Compression is disabled")
        else:
            logger.debug(f"[2/2] Compression set to {threshold} bytes")

    @staticmethod
    def join_game(player, data: bytes):
        player._data["entity_id"], data = utils.extract_int(data)

        gamemode, data = utils.extract_unsigned_byte(data)
        player._data["gamemode"] = gamemode & 0b00000111
        player._data["hardcore"] = (gamemode & 0b00001000) and True

        player._data["dimension"], data = utils.extract_int(data)

        player._server_data["difficulty"], data = \
            utils.extract_unsigned_byte(data)

        """ 
        Was once used by the client to draw the player list, but now is ignored.
        
        player._server_data["max_players"], data = \
            utils.extract_unsigned_byte(data)
         """
        data = data[1::]

        # default, flat, largeBiomes, amplified, default_1_1
        player._server_data["level_type"], data = \
            utils.extract_string_from_data(data)

        # Reduced Debug Info
        # player._server_data["RDI"], data = utils.extract_boolean(data)

        logger.debug("[2/2] Join game read")

    @staticmethod
    def player_abilities(player, data: bytes):

        flags, data = utils.extract_byte(data)
        player._data["invulnerable"] = (flags & 0x01) and True
        player._data["flying"] = (flags & 0x02) and True
        player._data["allow_flying"] = (flags & 0x04) and True
        player._data["creative_mode"] = (flags & 0x08) and True

        player._data["flying_speed"], data = utils.extract_float(data)
        player._data["fov_modifier"], data = utils.extract_float(data)

        logger.debug("[2/2] Player abilities changed.")

    # @staticmethod
    # def held_item_change(player, data: bytes):
    #     utils.extract_slot(data)



"""
Schema:
    clientbound_action_list = {
        "1.12.2": {
            "login": {
                packet_id: Server.method,
            },
            "play": {
                packet_id: Server.method,
            }
        }
    }
"""

clientbound_action_list = {
    "1.12.2": {
        "login": {
            0: Server.disconnect,
            # 1: Sever._encryption_request,
            2: Server.login_success,
            3: Server.set_compression,
        },
        "play": {

            0x0E: Server.server_difficulty,
            0x1A: Server.disconnect,

            0x2C: Server.player_abilities,
            0x23: Server.join_game,
            #0x3A: Server.held_item_change,

        }
    }
}


def get_action_list(player_version: VersionNamedTuple,
                    actions_type: str = "login") -> dict:
    """
    Returns dictionary that pairs packet_id to the action based on game version.

    Function login_success should return True when successfully logged in.

    :param actions_type: "login", "play"
    :param player_version: VersionNamedTuple from Version
    :returns dict(int, method)
    :rtype dict
    """

    try:
        actions_list = clientbound_action_list[player_version.release_name][actions_type]
    except Exception:
        actions_list = None

    return actions_list
