from typing import Union, NoReturn

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

    :params bot: Bot on which process packet.
    :params bytes: Data received from server, uncompressed, without packet id.
    """

    @staticmethod
    def set_compression(bot, data: bytes):
        threshold, _ = utils.unpack_varint(data)
        bot._conn.set_compression(threshold)

        if threshold < 0:
            logger.info(f"Compression is disabled")
        else:
            logger.info(f"Compression set to {threshold} bytes")

    @staticmethod
    def login_success(bot, data: bytes) -> True:
        bot._player.uuid = utils.extract_string_from_data(data)[0].decode('utf-8')
        logger.info(f"Successfully logged to the server, UUID: {bot._player.uuid}")
        return True

    @staticmethod
    def disconnect(bot, data: bytes) -> NoReturn:
        reason = utils.extract_json_from_chat(data)
        # reason should be dict Chat type.
        logger.error(f"{bot._player.username} has been "
                     f"disconnected by server. Reason: '{reason['text']}'")
        raise DisconnectedError("Disconnected by server.")

    @staticmethod
    def server_difficulty(bot, data: bytes):
        bot._game_data.difficulty, data = \
            utils.extract_unsigned_byte(data)
        logger.info(f"Server difficulty: {bot._game_data.difficulty}")

    @staticmethod
    def join_game(bot, data: bytes):
        bot._player.entity_id, data = utils.extract_int(data)

        gamemode, data = utils.extract_unsigned_byte(data)
        bot._player.gamemode = gamemode & 0b00000111
        bot._player.is_hardcore = bool(gamemode & 0b00001000)

        bot._player.dimension, data = utils.extract_int(data)

        bot._game_data.difficulty, data = \
            utils.extract_unsigned_byte(data)

        """ 
        Was once used by the client to draw the player list, but now is ignored.
        bot.player._server_data["max_players"], data = \
            utils.extract_unsigned_byte(data)
         """
        data = data[1::]

        # default, flat, largeBiomes, amplified, default_1_1
        bot._game_data.level_type, data = \
            utils.extract_string_from_data(data)

        # Reduced Debug Info
        # bot.player._server_data["RDI"], data = utils.extract_boolean(data)
        logger.info(f"Join game read: "
                    f"player_id: {bot._player.entity_id}, "
                    f"gamemode: {bot._player.gamemode}, "
                    f"hardcore: {bot._player.is_hardcore}, "
                    f"dimension: {bot._player.dimension}, "
                    f"difficulty: {bot._game_data.difficulty}, "
                    f"level_type: {bot._game_data.level_type}, "
                    )

    @staticmethod
    def player_abilities(bot, data: bytes):

        flags, data = utils.extract_byte(data)
        bot._player.is_invulnerable = bool(flags & 0x01)
        bot._player.is_flying = bool(flags & 0x02)
        bot._player.is_allow_flying = bool(flags & 0x04)
        bot._player.is_creative_mode = bool(flags & 0x08)

        bot._player.flying_speed, data = utils.extract_float(data)

        bot._player.fov_modifier, data = utils.extract_float(data)

        logger.info("Player abilities changed: "
                    f"invulnerable: {bot._player.is_invulnerable}, "
                    f"flying: {bot._player.is_flying}, "
                    f"allow_flying: {bot._player.is_allow_flying}, "
                    f"creative_mode: {bot._player.is_creative_mode}")

    @staticmethod
    def held_item_change(bot, data: bytes):
        bot._player.active_slot = utils.extract_byte(data)[0]
        logger.debug(f"Held slot changed to {bot._player.active_slot}")

    @staticmethod
    def entity_status(bot, data: bytes):
        entity_id, byte = utils.extract_int(data)
        entity_status = utils.extract_byte(data)[0]
        logger.debug(f"Entity with id: {entity_id} "
                     f"status changed to: {entity_status}")

    @staticmethod
    def player_position_and_look(bot, data: bytes):
        x, data = utils.extract_double(data)
        y, data = utils.extract_double(data)
        z, data = utils.extract_double(data)
        yaw, data = utils.extract_float(data)
        pitch, data = utils.extract_float(data)
        flags, data = utils.extract_byte(data)
        teleport_id = data

        if flags & 0x01:
            bot._player.pos_x += x
        else:
            bot._player.pos_x = x

        if flags & 0x02:
            bot._player.pos_y += y
        else:
            bot._player.pos_y = y

        if flags & 0x04:
            bot._player.pos_z += z
        else:
            bot._player.pos_z = z

        if flags & 0x08:
            bot._player.yaw += yaw
        else:
            bot._player.yaw = yaw

        if flags & 0x10:
            bot._player.pitch += pitch
        else:
            bot._player.pitch = pitch

        logger.info(f"Player pos: "
                    f"x: {bot._player.pos_x}, "
                    f"y: {bot._player.pos_y}, "
                    f"z: {bot._player.pos_z}, "
                    f"yaw: {bot._player.yaw}, "
                    f"pitch: {bot._player.pitch}")

        bot.to_send_queue.put(Creator.Play.teleport_confirm(teleport_id))

    @staticmethod
    def chunk_data(bot, data: bytes):
        pass
        # logger.debug(f"")

    # @staticmethod
    # def spawn_position(bot, data: bytes):
    #     logger.debug(f"Held slot changed to {slot}")

    # @staticmethod
    # def something(bot, data: bytes):
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
            0x20: Server.chunk_data,
            0x2C: Server.player_abilities,
            0x23: Server.join_game,
            0x2F: Server.player_position_and_look,
            0x3A: Server.held_item_change,


        }
    }
}


def get_action_list(bot_version: VersionNamedTuple,
                    actions_type: str = "login") -> dict:
    """
    Returns dictionary that pairs packet_id to the action based on game version.
    When not found returns None.
    Not raises exception.

    Function login_success should return True when successfully logged in.

    :param actions_type: "login", "play"
    :param bot_version: VersionNamedTuple from Version
    :returns dict(int, method) or None
    :rtype Union(dict, None)
    """

    try:
        actions_list = clientbound_action_list[bot_version.release_name][actions_type]
    except Exception:
        actions_list = None

    return actions_list
