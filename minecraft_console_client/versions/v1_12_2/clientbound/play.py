"""Module with functions related to given packet."""

import logging
from typing import NoReturn

from commands import chat_commands
from data_structures.position import Position
from misc import converters
from misc.exceptions import DisconnectedError
from misc.hashtables import GAMEMODE
from misc.hashtables import GAME_DIFFICULTY
from versions.v1_12_2.serverbound import packet_creator
from versions.v1_12_2.view.view import gui

logger = logging.getLogger("mainLogger")


def combat_event(bot, data: bytes):
    """
    'Now only used to display the game over screen (with enter combat
    and end combat completely ignored by the Notchain client)'
    """
    event, data = converters.extract_varint(data)

    if event == 2:  # Entity dead
        player_id, data = converters.extract_varint(data)
        entity_id, data = converters.extract_int(data)
        message = converters.extract_json_from_chat(data)

        """'Entity ID of the player that died
        (should match the client's entity ID).'"""
        if entity_id == bot.game_data.player_data_holder.entity_id:

            message = f"Player has been killed by: {entity_id}, " \
                      f"death message: '{message}' "

            bot.on_death()
        else:
            message = f"Entity: {player_id} has been " \
                      f"killed by: {entity_id}, death message: '{message}' "

        logger.info(message)
        gui.add_to_hotbar(message)


def player_list_item(bot, data: bytes):
    pass


def player_position_and_look(bot, data: bytes):
    """Auto-send teleport confirm, \
    and player_position_and_look (serverbound)."""
    _data = data[::]

    x, data = converters.extract_double(data)
    y, data = converters.extract_double(data)
    z, data = converters.extract_double(data)
    yaw, data = converters.extract_float(data)
    pitch, data = converters.extract_float(data)
    flags, teleport_id = converters.extract_byte(data)

    player_data_holder = bot.game_data.player_data_holder
    if player_data_holder.position is None:
        player_data_holder.position = Position(x, y, z)
        player_data_holder.look_yaw = yaw
        player_data_holder.look_pitch = pitch

        player_pos = player_data_holder.position.pos

    else:
        player_pos = player_data_holder.position.pos

        if flags & 0x01:
            player_pos["x"] += x
        else:
            player_pos["x"] = x

        if flags & 0x02:
            player_pos["y"] += y
        else:
            player_pos["y"] = y

        if flags & 0x04:
            player_pos["z"] += z
        else:
            player_pos["z"] = z

        if flags & 0x08:
            player_data_holder.look_yaw += yaw
        else:
            player_data_holder.look_yaw = yaw

        if flags & 0x10:
            player_data_holder.look_pitch += pitch
        else:
            player_data_holder.look_pitch = pitch

    logger.info("Player pos: %s Look: (yaw: %f, pitch: %f)",
                player_pos, player_data_holder.look_yaw, player_data_holder.look_pitch)

    gui.set_labels(("Player position", '------------------'),
                   ("x", player_pos["x"]),
                   ("y", player_pos["y"]),
                   ("z", player_pos["z"]),
                   ("yaw", player_data_holder.look_yaw),
                   ("pitch", player_data_holder.look_pitch),
                   ("------------------", '------------------'))

    # Teleport confirm.
    bot.send_queue.put(packet_creator.play.teleport_confirm(teleport_id))

    # Answer player position and look.
    bot.send_queue.put(
        packet_creator.play.player_position_and_look_confirm(_data))


def use_bed(bot, data: bytes):
    pass


def unlock_recipes(bot, data: bytes):
    pass


def destroy_entities(bot, data: bytes):
    pass


def remove_entity_effect(bot, data: bytes):
    pass


def resource_pack_send(bot, data: bytes):
    pass


def respawn(bot, data: bytes):
    game_data = bot.game_data

    game_data.player_data_holder.dimension, data = converters.extract_int(data)
    game_data.difficulty = data[0]
    game_data.player_data_holder.gamemode = data[1]
    game_data.level_type = converters.extract_string(data[2:])[0]

    difficulty_name = GAME_DIFFICULTY[game_data.difficulty]

    logger.info("Player respawn: gamemode: %i, dimension: %i, "
                "game difficulty: %i(%s), game level_type: %s, ",
                game_data.player_data_holder.gamemode,
                game_data.player_data_holder.dimension,
                game_data.difficulty, str(difficulty_name),
                game_data.level_type
                )

    gui.set_labels(
        ("dimension", game_data.player_data_holder.dimension),
        ("game difficulty", difficulty_name),
        ("gamemode", game_data.player_data_holder.gamemode),
        ("game level_type", game_data.level_type)
    )


def entity_head_look(bot, data: bytes):
    pass


def select_advancement_tab(bot, data: bytes):
    pass


def world_border(bot, data: bytes):
    pass


def camera(bot, data: bytes):
    pass


def held_item_change(bot, data: bytes):
    player = bot.game_data.player_data_holder

    player.active_slot = converters.extract_byte(data)[0]
    logger.debug("Held slot changed to %i", player.active_slot)

    gui.set_labels(("Held slot", player.active_slot))


def display_scoreboard(bot, data: bytes):
    pass


def entity_metadata(bot, data: bytes):
    pass


def attach_entity(bot, data: bytes):
    pass


def entity_velocity(bot, data: bytes):
    pass


def entity_equipment(bot, data: bytes):
    pass


def set_experience(bot, data: bytes):
    pass


def update_health(bot, data: bytes):
    """Auto-respawn bot."""
    player = bot.game_data.player_data_holder

    player.health, data = converters.extract_float(data)
    player.food, data = converters.extract_varint(data)
    player.food_saturation = converters.extract_float(data)[0]

    logger.info("Updated player. Health: %f, Food: %i, Food_saturation: %f",
                player.health, player.food, player.food_saturation)

    gui.set_labels(("health", player.health),
                   ("food", player.food),
                   ("food_saturation", player.food_saturation))

    if not player.health > 0:
        bot.on_death()


def scoreboard_objective(bot, data: bytes):
    pass


def set_passengers(bot, data: bytes):
    pass


def teams(bot, data: bytes):
    pass


def update_score(bot, data: bytes):
    pass


def spawn_position(bot, data: bytes):
    position = converters.extract_position(data)[0]

    logger.info("Changed player spawn position to %s", position)

    gui.set_labels(("Spawn position", position))


def time_update(bot, data: bytes):
    pass


def title(bot, data: bytes):
    pass


def sound_effect(bot, data: bytes):
    pass


def player_list_header_and_footer(bot, data: bytes):
    pass


def collect_item(bot, data: bytes):
    pass


def entity_teleport(bot, data: bytes):
    pass


def advancements(bot, data: bytes):
    pass


def entity_properties(bot, data: bytes):
    pass


def entity_effect(bot, data: bytes):
    pass


def block_break_animation(bot, data: bytes):
    pass


def statistics(bot, data: bytes):
    pass


def animation(bot, data: bytes):
    pass


def spawn_player(bot, data: bytes):
    pass


def spawn_painting(bot, data: bytes):
    pass


def spawn_mob(bot, data: bytes):
    pass


def spawn_global_entity(bot, data: bytes):
    pass


def spawn_experience_orb(bot, data: bytes):
    pass


def spawn_object(bot, data: bytes):
    pass


def unload_chunk(bot, data: bytes):
    pass


def explosion(bot, data: bytes):
    pass


def entity_status(bot, data: bytes):
    entity_id, byte = converters.extract_int(data)
    status = converters.extract_byte(data)[0]
    logger.debug("Entity with id: %i status changed to: %i",
                 entity_id, status)


def named_sound_effect(bot, data: bytes):
    pass


def plugin_message(bot, data: bytes):
    pass


def set_cooldown(bot, data: bytes):
    pass


def set_slot(bot, data: bytes):
    pass


def window_property(bot, data: bytes):
    pass


def window_items(bot, data: bytes):
    pass


def open_window(bot, data: bytes):
    pass


def close_window(bot, data: bytes):
    pass


def confirm_transaction(bot, data: bytes):
    pass


def multi_block_change(bot, data: bytes):
    pass


def chat_message(bot, data: bytes):
    json_data, position = converters.extract_json_from_chat(data)

    chat_commands.interpret(bot, str(json_data))

    gui.add_to_chat(f"{position}: {json_data}")


def tab_complete(bot, data: bytes):
    pass


def update_block_entity(bot, data: bytes):
    pass


def server_difficulty(bot, data: bytes):
    difficulty = converters.extract_unsigned_byte(data)[0]
    difficulty_name = GAME_DIFFICULTY[difficulty]

    bot.game_data.difficulty = difficulty

    logger.debug("Server difficulty: %i(%s)",
                 difficulty, difficulty_name)

    gui.set_labels(("game difficulty", difficulty_name))


def boss_bar(bot, data: bytes):
    pass


def block_action(bot, data: bytes):
    pass


def block_change(bot, data: bytes):
    pass


def change_game_state(bot, data: bytes):
    value = converters.extract_float(data[1:])[0]
    # reason = data[0]  # reason = utils.extract_unsigned_byte()[0]
    game_data = bot.game_data

    # TODO: Do sth with this:

    def invalid_bed(val: float):
        logger.info("Invalid bed")
        gui.add_to_hotbar("Invalid bed")

    def end_raining(_):
        game_data.is_raining = False
        logger.info("Stopped raining")
        gui.set_labels(("game: is_raining: ", False))

    def begin_raining(_):
        game_data.is_raining = True
        logger.info("Started raining")
        gui.set_labels(("game: is_raining: ", True))

    def change_gamemode(val: float):
        game_data.player_data_holder.gamemode = GAMEMODE[round(value)]
        logger.info("Updated gamemode: %i", game_data.player_data_holder.gamemode)
        gui.set_labels(("gamemode", game_data.player_data_holder.gamemode))

    def exit_end(val: float):
        pass

    def demo_message(val: float):
        pass

    def arrow_hitting_player(_bot, val: float):
        logger.info("An arrow hit a player")

    def fade_value(val: float):
        pass

    def fade_time(val: float):
        pass

    def play_elder_guardian_mob_appearance(val: float):
        pass


def keep_alive(bot, data: bytes):
    """Auto-sends keep alive packet."""
    bot.send_queue.put(packet_creator.play.keep_alive(data))


def chunk_data(bot, data: bytes):
    pass


def effect(bot, data: bytes):
    pass


def particle(bot, data: bytes):
    pass


def join_game(bot, data: bytes):
    game_data = bot.game_data
    player = game_data.player_data_holder

    player.entity_id, data = converters.extract_int(data)

    gamemode, data = converters.extract_unsigned_byte(data)

    player.gamemode = GAMEMODE[gamemode & 0b00000111]

    player.is_hardcore = bool(gamemode & 0b00001000)

    player.dimension, data = converters.extract_int(data)

    game_data.difficulty, data = \
        converters.extract_unsigned_byte(data)
    difficulty_name = GAME_DIFFICULTY[game_data.difficulty]

    # Was once used by the client to draw the player list,
    # but now is ignored.
    # bot.player._server_data["max_players"], data = \
    #     utils.extract_unsigned_byte(data)

    data = data[1:]

    # default, flat, largeBiomes, amplified, default_1_1
    game_data.level_type = converters.extract_string(data)[0]

    # Reduced Debug Info
    # bot.player._server_data["RDI"], data = utils.extract_boolean(data)
    logger.info("Join game read: player_id: %i, gamemode: %r, hardcore: %r, "
                "dimension: %r, game difficulty: %r (%r), game level_type: %r",
                player.entity_id,
                player.gamemode,
                player.is_hardcore,
                player.dimension,
                game_data.difficulty, difficulty_name,
                game_data.level_type
                )

    gui.set_labels(
        ("player_id", player.entity_id),
        ("gamemode", player.gamemode),
        ("is_hardcore", player.is_hardcore),
        ("dimension", player.dimension),
        ("game difficulty", difficulty_name),
        ("game level_type", game_data.level_type)
    )


def map_(bot, data: bytes):
    pass


def entity(bot, data: bytes):
    pass


def entity_relative_move(bot, data: bytes):
    pass


def entity_look_and_relative_move(bot, data: bytes):
    pass


def entity_look(bot, data: bytes):
    pass


def vehicle_move(bot, data: bytes):
    pass


def open_sign_editor(bot, data: bytes):
    pass


def craft_recipe_response(bot, data: bytes):
    pass


def player_abilities(bot, data: bytes):
    player = bot.game_data.player_data_holder

    flags, data = converters.extract_byte(data)
    player.is_invulnerable = bool(flags & 0x01)
    player.is_flying = bool(flags & 0x02)
    player.is_allow_flying = bool(flags & 0x04)
    player.is_creative_mode = bool(flags & 0x08)

    player.flying_speed, data = converters.extract_float(data)

    player.fov_modifier = converters.extract_float(data)[0]

    logger.info("Player abilities changed: invulnerable: %r, flying: %r, "
                "allow_flying: %r, creative_mode: %r",
                player.is_invulnerable,
                player.is_flying,
                player.is_allow_flying,
                player.is_creative_mode
                )

    gui.set_labels(("invulnerable", player.is_invulnerable),
                   ("flying", player.is_flying),
                   ("allow_flying", player.is_allow_flying),
                   ("creative_mode", player.is_creative_mode))


def disconnect(bot, data: bytes) -> NoReturn:
    player = bot.game_data.player_data_holder

    reason = converters.extract_json_from_chat(data)[0]
    # reason should be dict Chat type.
    logger.error("% has been disconnected by server. Reason: '%r'",
                 player.username, reason['text'])
    raise DisconnectedError("Disconnected by server.")
