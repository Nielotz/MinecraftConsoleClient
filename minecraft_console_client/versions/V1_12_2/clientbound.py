import logging
from typing import NoReturn

logger = logging.getLogger("mainLogger")

from misc import utils
from misc.exceptions import DisconnectedError
from versions.V1_12_2.creator import Creator
import versions.defaults.clientbound


from GUI.gui import GUI
gui = GUI()


class Clientbound(versions.defaults.clientbound.Clientbound):
    """
    Namespace for clientbound events (sent by server).
    Method names same as on minecraft protocol page.

    Inherits default methods from versions.default.Server.

    :params bot: Bot on which process packet.
    :params bytes: Data received from server, uncompressed, without packet id.
    """

    @staticmethod
    def set_compression(bot, data: bytes):
        threshold, _ = utils.unpack_varint(data)
        bot._conn.set_compression(threshold)

        gui.set_value("compression threshold", threshold)

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
        reason, _ = utils.extract_json_from_chat(data)
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
        logger.debug(f"Server difficulty: {bot._game_data.difficulty}")

        gui.set_value("difficulty",
                      {0: "peaceful", 1: "easy", 2: "normal", 3: "hard"}
                      .get(bot._game_data.difficulty))


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

        gui.set_value("player_id", bot._player.entity_id)
        gui.set_value("gamemode", bot._player.gamemode)
        gui.set_value("is_hardcore", bot._player.is_hardcore)
        gui.set_value("dimension", bot._player.dimension)
        gui.set_value("difficulty", bot._game_data.difficulty)
        gui.set_value("level_type", bot._game_data.level_type)


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

        gui.set_value("invulnerable", bot._player.is_invulnerable)
        gui.set_value("flying", bot._player.is_flying)
        gui.set_value("allow_flying", bot._player.is_allow_flying)
        gui.set_value("creative_mode", bot._player.is_creative_mode)


    @staticmethod
    def combat_event(bot, data: bytes):
        pass

    @staticmethod
    def player_list_item(bot, data: bytes):
        pass

    @staticmethod
    def player_position_and_look(bot, data: bytes):
        """ Auto-sends teleport confirm """
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

        gui.set_value("Player position", '------------------')
        gui.set_value("x", bot._player.pos_x)
        gui.set_value("y", bot._player.pos_y)
        gui.set_value("z", bot._player.pos_z)
        gui.set_value("yaw", bot._player.yaw)
        gui.set_value("pitch", bot._player.pitch)
        gui.set_value("------------------", '------------------')

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

        gui.set_value("Held slot", bot._player.active_slot)

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

        gui.set_value("Spawn position", bot._player.position)

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
