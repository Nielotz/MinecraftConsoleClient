from typing import Union

import logging

logger = logging.getLogger('mainLogger')

from exceptions import DisconnectedError
from version import VersionNamedTuple, Version
import utils
from packet import Creator

""" Actions possible to happen, e.g. packets available to be received/sent. """


class Server:
    """
    Namespace for server-side events.
    Method names taken from minecraft protocol page.

    :params player: Player on which process packet.
    :params bytes: Data received from server, uncompressed, without packet id.
    """

    @staticmethod
    def set_compression(player, data: bytes):
        threshold, _ = utils.unpack_varint(data)
        player._conn.set_compression(threshold)

        if threshold < 0:
            logger.info(f"Compression is disabled")
        else:
            logger.info(f"Compression set to {threshold} bytes")

    @staticmethod
    def login_success(player, data: bytes):
        player.uuid = utils.extract_string_from_data(data)[0].decode('utf-8')
        logger.info(f"Successfully logged to the server, UUID: {player.uuid}")
        return True

    @staticmethod
    def disconnect(player, data: bytes):
        reason = utils.extract_json_from_chat(data)
        # reason should be dict Chat type.
        logger.error(f"{player.username} has been "
                     f"disconnected by server. Reason: '{reason['text']}'")
        raise DisconnectedError("Disconnected by server.")

    @staticmethod
    def server_difficulty(player, data: bytes):
        player.game_data.difficulty, data = \
            utils.extract_unsigned_byte(data)
        logger.info(f"Server difficulty: {player.game_data.difficulty}")

    @staticmethod
    def join_game(player, data: bytes):
        player.entity_id, data = utils.extract_int(data)

        gamemode, data = utils.extract_unsigned_byte(data)
        player.gamemode = gamemode & 0b00000111
        player.is_hardcore = bool(gamemode & 0b00001000)

        player.dimension, data = utils.extract_int(data)

        player.game_data.difficulty, data = \
            utils.extract_unsigned_byte(data)

        """ 
        Was once used by the client to draw the player list, but now is ignored.
        player._server_data["max_players"], data = \
            utils.extract_unsigned_byte(data)
         """
        data = data[1::]

        # default, flat, largeBiomes, amplified, default_1_1
        player.game_data.level_type, data = \
            utils.extract_string_from_data(data)

        # Reduced Debug Info
        # player._server_data["RDI"], data = utils.extract_boolean(data)
        logger.info(f"Join game read: "
                    f"player_id: {player.entity_id}, "
                    f"gamemode: {player.gamemode}, "
                    f"hardcore: {player.is_hardcore}, "
                    f"dimension: {player.dimension}, "
                    f"difficulty: {player.game_data.difficulty}, "
                    f"level_type: {player.game_data.level_type}, "
                    )

    @staticmethod
    def player_abilities(player, data: bytes):

        flags, data = utils.extract_byte(data)
        player.is_invulnerable = bool(flags & 0x01)
        player.is_flying = bool(flags & 0x02)
        player.is_allow_flying = bool(flags & 0x04)
        player.is_creative_mode = bool(flags & 0x08)

        player.flying_speed, data = utils.extract_float(data)

        player.fov_modifier, data = utils.extract_float(data)

        logger.info("Player abilities changed: "
                    f"invulnerable: {player.is_invulnerable}, "
                    f"flying: {player.is_flying}, "
                    f"allow_flying: {player.is_allow_flying}, "
                    f"creative_mode: {player.is_creative_mode}")

    @staticmethod
    def held_item_change(player, data: bytes):
        player.active_slot = utils.extract_byte(data)[0]
        logger.debug(f"Held slot changed to {player.active_slot}")

    @staticmethod
    def entity_status(player, data: bytes):
        entity_id, byte = utils.extract_int(data)
        entity_status = utils.extract_byte(data)[0]
        logger.debug(f"Entity with id: {entity_id} "
                     f"status changed to: {entity_status}")

    @staticmethod
    def player_position_and_look(player, data: bytes):
        x, data = utils.extract_double(data)
        y, data = utils.extract_double(data)
        z, data = utils.extract_double(data)
        yaw, data = utils.extract_float(data)
        pitch, data = utils.extract_float(data)
        flags, data = utils.extract_byte(data)
        teleport_id = data

        if flags & 0x01:
            player.pos_x += x
        else:
            player.pos_x = x

        if flags & 0x02:
            player.pos_y += y
        else:
            player.pos_y = y

        if flags & 0x04:
            player.pos_z += z
        else:
            player.pos_z = z

        if flags & 0x08:
            player.yaw += yaw
        else:
            player.yaw = yaw

        if flags & 0x10:
            player.pitch += pitch
        else:
            player.pitch = pitch

        logger.info(f"Player pos: "
                    f"x: {player.pos_x}, "
                    f"y: {player.pos_y}, "
                    f"z: {player.pos_z}, "
                    f"yaw: {player.yaw}, "
                    f"pitch: {player.pitch}")

        player.to_send_queue.put(Creator.Play.teleport_confirm(teleport_id))

    # @staticmethod
    # def something(player, data: bytes):
    #     logger.debug(f"Held slot changed to {slot}")


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
            # 0x00: Server.spawn_object
            0x0D: Server.server_difficulty,
            # 0x18: Server.plugin_message,
            0x1A: Server.disconnect,
            0x1B: Server.entity_status,  # TODO: Add entity statuses
            0x2C: Server.player_abilities,
            0x23: Server.join_game,
            0x2F: Server.player_position_and_look,
            0x3A: Server.held_item_change,


        }
    }
}


def get_action_list(player_version: VersionNamedTuple,
                    actions_type: str = "login") -> dict:
    """
    Returns dictionary that pairs packet_id to the action based on game version.
    When not found returns None.
    Not raises exception.

    Function login_success should return True when successfully logged in.

    :param actions_type: "login", "play"
    :param player_version: VersionNamedTuple from Version
    :returns dict(int, method) or None
    :rtype Union(dict, None)
    """

    try:
        actions_list = clientbound_action_list[player_version.release_name][actions_type]
    except Exception:
        actions_list = None

    return actions_list
