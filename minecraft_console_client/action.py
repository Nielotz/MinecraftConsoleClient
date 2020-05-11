from typing import Union, NoReturn

import logging

logger = logging.getLogger('mainLogger')

from exceptions import DisconnectedError
from version import VersionNamedTuple, Version
import utils
from packet import Creator
from position import Position

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
        bot._player.uuid = utils.extract_string(data)[0].decode('utf-8')
        logger.info(f"Successfully logged to the server, "
                    f"UUID: {bot._player.uuid}")
        return True

    @staticmethod
    def disconnect(bot, data: bytes) -> NoReturn:
        reason = utils.extract_json_from_chat(data)
        # reason should be dict Chat type.
        logger.error(f"{bot._player.username} has been "
                     f"disconnected by server. Reason: '{reason['text']}'")
        raise DisconnectedError("Disconnected by server.")

    @staticmethod
    def spawn_object(bot, data: bytes):
        pass

    @staticmethod
    def spawn_experience_orb(bot, data: bytes):
        pass

    @staticmethod
    def spawn_global_entity(bot, data: bytes):
        pass

    @staticmethod
    def spawn_mob(bot, data: bytes):
        pass

    @staticmethod
    def spawn_painting(bot, data: bytes):
        pass

    @staticmethod
    def spawn_player(bot, data: bytes):
        pass

    @staticmethod
    def animation(bot, data: bytes):
        pass

    @staticmethod
    def statistics(bot, data: bytes):
        pass

    @staticmethod
    def block_break_animation(bot, data: bytes):
        pass

    @staticmethod
    def update_block_entity(bot, data: bytes):
        pass

    @staticmethod
    def block_action(bot, data: bytes):
        pass

    @staticmethod
    def block_change(bot, data: bytes):
        pass

    @staticmethod
    def boss_bar(bot, data: bytes):
        pass

    @staticmethod
    def server_difficulty(bot, data: bytes):
        bot._game_data.difficulty, data = \
            utils.extract_unsigned_byte(data)
        logger.info(f"Server difficulty: {bot._game_data.difficulty}")

    @staticmethod
    def tab_complete(bot, data: bytes):
        pass

    @staticmethod
    def chat_message(bot, data: bytes):
        pass

    @staticmethod
    def multi_block_change(bot, data: bytes):
        pass

    @staticmethod
    def confirm_transaction(bot, data: bytes):
        pass

    @staticmethod
    def close_window(bot, data: bytes):
        pass

    @staticmethod
    def open_window(bot, data: bytes):
        pass

    @staticmethod
    def window_items(bot, data: bytes):
        pass

    @staticmethod
    def window_property(bot, data: bytes):
        pass

    @staticmethod
    def set_slot(bot, data: bytes):
        pass

    @staticmethod
    def set_cooldown(bot, data: bytes):
        pass

    @staticmethod
    def plugin_message(bot, data: bytes):
        pass

    @staticmethod
    def named_sound_effect(bot, data: bytes):
        pass

    @staticmethod
    def disconnect(bot, data: bytes):
        pass

    @staticmethod
    def entity_status(bot, data: bytes):
        entity_id, byte = utils.extract_int(data)
        entity_status = utils.extract_byte(data)[0]
        logger.debug(f"Entity with id: {entity_id} "
                     f"status changed to: {entity_status}")

    @staticmethod
    def explosion(bot, data: bytes):
        pass

    @staticmethod
    def unload_chunk(bot, data: bytes):
        pass

    @staticmethod
    def change_game_state(bot, data: bytes):
        pass

    @staticmethod
    def keep_alive(bot, data: bytes):
        pass

    @staticmethod
    def chunk_data(bot, data: bytes):
        pass

    @staticmethod
    def effect(bot, data: bytes):
        pass

    @staticmethod
    def particle(bot, data: bytes):
        pass

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
            utils.extract_string(data)

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
    def map(bot, data: bytes):
        pass

    @staticmethod
    def entity(bot, data: bytes):
        pass

    @staticmethod
    def entity_relative_move(bot, data: bytes):
        pass

    @staticmethod
    def entity_look_and_relative_move(bot, data: bytes):
        pass

    @staticmethod
    def entity_look(bot, data: bytes):
        pass

    @staticmethod
    def vehicle_move(bot, data: bytes):
        pass

    @staticmethod
    def open_sign_editor(bot, data: bytes):
        pass

    @staticmethod
    def craft_recipe_response(bot, data: bytes):
        pass

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
    def combat_event(bot, data: bytes):
        pass

    @staticmethod
    def player_list_item(bot, data: bytes):
        pass

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

        logger.debug(f"Player pos: "
                     f"x: {bot._player.pos_x}, "
                     f"y: {bot._player.pos_y}, "
                     f"z: {bot._player.pos_z}, "
                     f"yaw: {bot._player.yaw}, "
                     f"pitch: {bot._player.pitch}")

        bot.to_send_queue.put(Creator.Play.teleport_confirm(teleport_id))

    @staticmethod
    def use_bed(bot, data: bytes):
        pass

    @staticmethod
    def unlock_recipes(bot, data: bytes):
        pass

    @staticmethod
    def destroy_entities(bot, data: bytes):
        pass

    @staticmethod
    def remove_entity_effect(bot, data: bytes):
        pass

    @staticmethod
    def resource_pack_send(bot, data: bytes):
        pass

    @staticmethod
    def respawn(bot, data: bytes):
        pass

    @staticmethod
    def entity_head_look(bot, data: bytes):
        pass

    @staticmethod
    def select_advancement_tab(bot, data: bytes):
        pass

    @staticmethod
    def world_border(bot, data: bytes):
        pass

    @staticmethod
    def camera(bot, data: bytes):
        pass

    @staticmethod
    def held_item_change(bot, data: bytes):
        bot._player.active_slot = utils.extract_byte(data)[0]
        logger.debug(f"Held slot changed to {bot._player.active_slot}")

    @staticmethod
    def display_scoreboard(bot, data: bytes):
        pass

    @staticmethod
    def entity_metadata(bot, data: bytes):
        pass

    @staticmethod
    def attach_entity(bot, data: bytes):
        pass

    @staticmethod
    def entity_velocity(bot, data: bytes):
        pass

    @staticmethod
    def entity_equipment(bot, data: bytes):
        pass

    @staticmethod
    def set_experience(bot, data: bytes):
        pass

    @staticmethod
    def update_health(bot, data: bytes):
        pass

    @staticmethod
    def scoreboard_objective(bot, data: bytes):
        pass

    @staticmethod
    def set_passengers(bot, data: bytes):
        pass

    @staticmethod
    def teams(bot, data: bytes):
        pass

    @staticmethod
    def update_score(bot, data: bytes):
        pass

    @staticmethod
    def spawn_position(bot, data: bytes):
        bot._player.position, data = utils.extract_position(data)
        logger.info(f"Changed player spawn position to {bot._player.position}")

    @staticmethod
    def time_update(bot, data: bytes):
        pass

    @staticmethod
    def title(bot, data: bytes):
        pass

    @staticmethod
    def sound_effect(bot, data: bytes):
        pass

    @staticmethod
    def player_list_header_and_footer(bot, data: bytes):
        pass

    @staticmethod
    def collect_item(bot, data: bytes):
        pass

    @staticmethod
    def entity_teleport(bot, data: bytes):
        pass

    @staticmethod
    def advancements(bot, data: bytes):
        pass

    @staticmethod
    def entity_properties(bot, data: bytes):
        pass

    @staticmethod
    def entity_effect(bot, data: bytes):
        pass


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
            # 0x00: Server.spawn_object,
            # 0x01: Server.spawn_experience_orb,
            # 0x02: Server.spawn_global_entity,
            # 0x03: Server.spawn_mob,
            # 0x04: Server.spawn_painting,
            # 0x05: Server.spawn_player,
            # 0x06: Server.animation,
            # 0x07: Server.statistics,
            # 0x08: Server.block_break_animation,
            # 0x09: Server.update_block_entity,
            # 0x0A: Server.block_action,
            # 0x0B: Server.block_change,
            # 0x0C: Server.boss_bar,
            0x0D: Server.server_difficulty,
            # 0x0E: Server.tab_complete,
            # 0x0F: Server.chat_message,
            # 0x10: Server.multi_block_change,
            # 0x11: Server.confirm_transaction,
            # 0x12: Server.close_window,
            # 0x13: Server.open_window,
            # 0x14: Server.window_items,
            # 0x15: Server.window_property,
            # 0x16: Server.set_slot,
            # 0x17: Server.set_cooldown,
            # 0x18: Server.plugin_message,
            # 0x19: Server.named_sound_effect,
            0x1A: Server.disconnect,
            0x1B: Server.entity_status,
            # 0x1C: Server.explosion,
            # 0x1D: Server.unload_chunk,
            # 0x1E: Server.change_game_state,
            # 0x1F: Server.keep_alive,
            0x20: Server.chunk_data,
            # 0x21: Server.effect,
            # 0x22: Server.particle,
            0x23: Server.join_game,
            # 0x24: Server.map,
            # 0x25: Server.entity,
            # 0x26: Server.entity_relative_move,
            # 0x27: Server.entity_look_and_relative_move,
            # 0x28: Server.entity_look,
            # 0x29: Server.vehicle_move,
            # 0x2A: Server.open_sign_editor,
            # 0x2B: Server.craft_recipe_response,
            0x2C: Server.player_abilities,
            # 0x2D: Server.combat_event,
            # 0x2E: Server.player_list_item,
            0x2F: Server.player_position_and_look,
            # 0x30: Server.use_bed,
            # 0x31: Server.unlock_recipes,
            # 0x32: Server.destroy_entities,
            # 0x33: Server.remove_entity_effect,
            # 0x34: Server.resource_pack_send,
            # 0x35: Server.respawn,
            # 0x36: Server.entity_head_look,
            # 0x37: Server.select_advancement_tab,
            # 0x38: Server.world_border,
            # 0x39: Server.camera,
            0x3A: Server.held_item_change,
            # 0x3B: Server.display_scoreboard,
            # 0x3C: Server.entity_metadata,
            # 0x3D: Server.attach_entity,
            # 0x3E: Server.entity_velocity,
            # 0x3F: Server.entity_equipment,
            # 0x40: Server.set_experience,
            # 0x41: Server.update_health,
            # 0x42: Server.scoreboard_objective,
            # 0x43: Server.set_passengers,
            # 0x44: Server.teams,
            # 0x45: Server.update_score,
            0x46: Server.spawn_position,
            # 0x47: Server.time_update,
            # 0x48: Server.title,
            # 0x49: Server.sound_effect,
            # 0x4A: Server.player_list_header_and_footer,
            # 0x4B: Server.collect_item,
            # 0x4C: Server.entity_teleport,
            # 0x4D: Server.advancements,
            # 0x4E: Server.entity_properties,
            # 0x4F: Server.entity_effect,
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
