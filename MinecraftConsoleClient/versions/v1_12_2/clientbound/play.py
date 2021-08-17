"""Module with functions related to given packet."""

import logging
from typing import NoReturn
from typing import TYPE_CHECKING

from commands import chat_commands
from data_structures.position import Position
from misc import converters
from misc.exceptions import DisconnectedByServerException
from misc.hashtables import GAMEMODE
from misc.hashtables import GAME_DIFFICULTY
from versions.v1_12_2.serverbound import packet_creator
from versions.v1_12_2.view.view import gui

logger = logging.getLogger("mainLogger")

if TYPE_CHECKING:
    import game


def combat_event(game_: "game.Game", data: bytes):
    """
    'Now only used to display the game over screen (with enter combat
    and end combat completely ignored by the Notchain client)'
    """
    event, data = converters.extract_varint_as_int(data)

    if event == 2:  # Entity dead
        player_id, data = converters.extract_varint_as_int(data)
        entity_id, data = converters.extract_int(data)
        message = converters.extract_json_from_chat(data)

        # 'Entity ID of the player that died
        # (should match the client's entity ID).'
        if entity_id == game_.data.player.data.entity_id:

            message = f"Player has been killed by: {entity_id}, " \
                      f"death message: '{message}' "

            game_.on_death()
        else:
            message = f"Entity: {player_id} has been " \
                      f"killed by: {entity_id}, death message: '{message}' "

        logger.info(message)
        gui.add_to_hotbar(message)


def player_list_item(game_: "game.Game", data: bytes):
    pass


def player_position_and_look(game_: "game.Game", data: bytes):
    """Auto-send teleport confirm, \
    and game_position_and_look (serverbound)."""
    _data = data[::]

    x, data = converters.extract_double(data)
    y, data = converters.extract_double(data)
    z, data = converters.extract_double(data)
    yaw, data = converters.extract_float(data)
    pitch, data = converters.extract_float(data)
    flags, teleport_id = converters.extract_byte(data)

    world_data = game_.data.world_data
    player_data = game_.data.player.data

    if player_data.position is None:
        player_data.position = Position(x, y, z)

        player_data.look_yaw = yaw
        player_data.look_pitch = pitch

        player_pos = player_data.position.pos

    else:
        player_pos = player_data.position.pos

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
            player_data.look_yaw += yaw
        else:
            player_data.look_yaw = yaw

        if flags & 0x10:
            player_data.look_pitch += pitch
        else:
            player_data.look_pitch = pitch

    logger.info("Player pos: %s Look: (yaw: %f, pitch: %f)",
                player_pos, player_data.look_yaw, player_data.look_pitch)

    gui.set_labels(("Player position", '------------------'),
                   ("x", player_pos["x"]),
                   ("y", player_pos["y"]),
                   ("z", player_pos["z"]),
                   ("yaw", player_data.look_yaw),
                   ("pitch", player_data.look_pitch),
                   ("------------------", '------------------'))

    add_packet = game_.to_send_packets.put

    # Teleport confirm.
    add_packet(packet_creator.play.teleport_confirm(teleport_id))

    # Answer player position and look.
    add_packet(
        packet_creator.play.player_position_and_look_confirm(_data))


def use_bed(game_: "game.Game", data: bytes):
    pass


def unlock_recipes(game_: "game.Game", data: bytes):
    pass


def destroy_entities(game_: "game.Game", data: bytes):
    pass


def remove_entity_effect(game_: "game.Game", data: bytes):
    pass


def resource_pack_send(game_: "game.Game", data: bytes):
    pass


def respawn(game_: "game.Game", data: bytes):
    world_data = game_.data.world_data

    world_data.dimension, data = converters.extract_int(data)
    world_data.difficulty = data[0]
    game_.data.player.gamemode = data[1]
    world_data.level_type = converters.extract_string(data[2:])[0]

    difficulty_name = GAME_DIFFICULTY[world_data.difficulty]

    logger.info("Player respawn: gamemode: %i, dimension: %i, "
                "game difficulty: %i(%s), game level_type: %s, ",
                game_.data.player.gamemode,
                world_data.dimension,
                world_data.difficulty, str(difficulty_name),
                world_data.level_type
                )

    gui.set_labels(
        ("dimension", world_data.dimension),
        ("game difficulty", difficulty_name),
        ("gamemode", game_.data.player.gamemode),
        ("game level_type", world_data.level_type)
    )


def entity_head_look(game_: "game.Game", data: bytes):
    pass


def select_advancement_tab(game_: "game.Game", data: bytes):
    pass


def world_border(game_: "game.Game", data: bytes):
    pass


def camera(game_: "game.Game", data: bytes):
    pass


def held_item_change(game_: "game.Game", data: bytes):
    player = game_.data.player.data

    player.active_slot = converters.extract_byte(data)[0]
    logger.debug("Held slot changed to %i", player.active_slot)

    gui.set_labels(("Held slot", player.active_slot))


def display_scoreboard(game_: "game.Game", data: bytes):
    pass


def entity_metadata(game_: "game.Game", data: bytes):
    pass


def attach_entity(game_: "game.Game", data: bytes):
    pass


def entity_velocity(game_: "game.Game", data: bytes):
    pass


def entity_equipment(game_: "game.Game", data: bytes):
    pass


def set_experience(game_: "game.Game", data: bytes):
    pass


def update_health(game_: "game.Game", data: bytes):
    """Auto-respawn player."""
    player = game_.data.player.data

    player.health, data = converters.extract_float(data)
    player.food, data = converters.extract_varint_as_int(data)
    player.food_saturation = converters.extract_float(data)[0]

    logger.info("Updated player. Health: %f, Food: %i, Food_saturation: %f",
                player.health, player.food, player.food_saturation)

    gui.set_labels(("health", player.health),
                   ("food", player.food),
                   ("food_saturation", player.food_saturation))

    if not player.health > 0:
        game_.on_death()


def scoreboard_objective(game_: "game.Game", data: bytes):
    pass


def set_passengers(game_: "game.Game", data: bytes):
    pass


def teams(game_: "game.Game", data: bytes):
    pass


def update_score(game_: "game.Game", data: bytes):
    pass


def spawn_position(game_: "game.Game", data: bytes):
    position = converters.extract_position(data)[0]

    logger.info("Changed player spawn position to %s", position)

    gui.set_labels(("Spawn position", position))


def time_update(game_: "game.Game", data: bytes):
    pass


def title(game_: "game.Game", data: bytes):
    pass


def sound_effect(game_: "game.Game", data: bytes):
    pass


def player_list_header_and_footer(game_: "game.Game", data: bytes):
    pass


def collect_item(game_: "game.Game", data: bytes):
    pass


def entity_teleport(game_: "game.Game", data: bytes):
    pass


def advancements(game_: "game.Game", data: bytes):
    pass


def entity_properties(game_: "game.Game", data: bytes):
    pass


def entity_effect(game_: "game.Game", data: bytes):
    pass


def block_break_animation(game_: "game.Game", data: bytes):
    pass


def statistics(game_: "game.Game", data: bytes):
    pass


def animation(game_: "game.Game", data: bytes):
    pass


def spawn_player(game_: "game.Game", data: bytes):
    pass


def spawn_painting(game_: "game.Game", data: bytes):
    pass


def spawn_mob(game_: "game.Game", data: bytes):
    pass


def spawn_global_entity(game_: "game.Game", data: bytes):
    pass


def spawn_experience_orb(game_: "game.Game", data: bytes):
    pass


def spawn_object(game_: "game.Game", data: bytes):
    pass


def unload_chunk(game_: "game.Game", data: bytes):
    pass


def explosion(game_: "game.Game", data: bytes):
    pass


def entity_status(game_: "game.Game", data: bytes):
    entity_id, byte = converters.extract_int(data)
    status = converters.extract_byte(data)[0]
    logger.debug("Entity with id: %i status changed to: %i",
                 entity_id, status)


def named_sound_effect(game_: "game.Game", data: bytes):
    pass


def plugin_message(game_: "game.Game", data: bytes):
    pass


def set_cooldown(game_: "game.Game", data: bytes):
    pass


def set_slot(game_: "game.Game", data: bytes):
    pass


def window_property(game_: "game.Game", data: bytes):
    pass


def window_items(game_: "game.Game", data: bytes):
    pass


def open_window(game_: "game.Game", data: bytes):
    pass


def close_window(game_: "game.Game", data: bytes):
    pass


def confirm_transaction(game_: "game.Game", data: bytes):
    pass


def multi_block_change(game_: "game.Game", data: bytes):
    pass


def chat_message(game_: "game.Game", data: bytes):
    json_data, position = converters.extract_json_from_chat(data)

    chat_commands.interpret(game_, str(json_data))

    gui.add_to_chat(f"{position}: {json_data}")


def tab_complete(game_: "game.Game", data: bytes):
    pass


def update_block_entity(game_: "game.Game", data: bytes):
    pass


def server_difficulty(game_: "game.Game", data: bytes):
    difficulty = converters.extract_unsigned_byte(data)[0]
    difficulty_name = GAME_DIFFICULTY[difficulty]

    game_.data.world_data.difficulty = difficulty

    logger.debug("Server difficulty: %i(%s)",
                 difficulty, difficulty_name)

    gui.set_labels(("game difficulty", difficulty_name))


def boss_bar(game_: "game.Game", data: bytes):
    pass


def block_action(game_: "game.Game", data: bytes):
    pass


def block_change(game_: "game.Game", data: bytes):
    position, data = converters.extract_position(data)
    block_id, _ = converters.extract_varint_as_int(data)

    # For debug purposes.
    from versions.defaults.consts import BLOCK as ID_
    block_type, metadata = block_id >> 4, block_id & 15
    try:
        print(f"{position} is now "
              f"{ID_[block_type][metadata]['name']}({block_type}:{metadata})")
    except KeyError:
        print(f"{position} is unsupported({block_type}:{metadata})")


def change_game_state(game_: "game.Game", data: bytes):
    value = converters.extract_float(data[1:])[0]
    # reason = data[0]  # reason = utils.extract_unsigned_byte()[0]
    world_data = game_.data.world_data

    # TODO: Do sth with this:

    def invalid_bed(val: float):
        logger.info("Invalid bed")
        gui.add_to_hotbar("Invalid bed")

    def end_raining(_):
        world_data.is_raining = False
        logger.info("Stopped raining")
        gui.set_labels(("game: is_raining: ", False))

    def begin_raining(_):
        world_data.is_raining = True
        logger.info("Started raining")
        gui.set_labels(("game: is_raining: ", True))

    def change_gamemode(val: float):
        data.gamemode = GAMEMODE[round(value)]
        logger.info("Updated gamemode: %i", data.gamemode)
        gui.set_labels(("gamemode", data.gamemode))

    def exit_end(val: float):
        pass

    def demo_message(val: float):
        pass

    def arrow_hitting_player(_player, val: float):
        logger.info("An arrow hit a player")

    def fade_value(val: float):
        pass

    def fade_time(val: float):
        pass

    def play_elder_guardian_mob_appearance(val: float):
        pass


def keep_alive(game_: "game.Game", data: bytes):
    """Auto-sends keep alive packet."""
    game_.data.to_send_packets.put(packet_creator.play.keep_alive(data))


def chunk_data(game_: "game.Game", data: bytes):
    game_.data.world_data.world.parse_chunk_packet(data)


def effect(game_: "game.Game", data: bytes):
    pass


def particle(game_: "game.Game", data: bytes):
    pass


def join_game(game_: "game.Game", data: bytes):
    world_data = game_.data.world_data
    player = game_.data.player

    player.entity_id, data = converters.extract_int(data)

    gamemode, data = converters.extract_unsigned_byte(data)

    player.gamemode = GAMEMODE[gamemode & 0b00000111]

    player.is_hardcore = bool(gamemode & 0b00001000)

    player.dimension, data = converters.extract_int(data)

    world_data.difficulty, data = \
        converters.extract_unsigned_byte(data)
    difficulty_name = GAME_DIFFICULTY[world_data.difficulty]

    # Was once used by the client to draw the player list,
    # but now is ignored.
    # player.player._server_data["max_players"], data = \
    #     utils.extract_unsigned_byte(data)

    data = data[1:]

    # default, flat, largeBiomes, amplified, default_1_1
    world_data.level_type = converters.extract_string(data)[0]

    # Reduced Debug Info
    # player.player._server_data["RDI"], data = utils.extract_boolean(data)
    logger.info("Join game read: player_id: %i, gamemode: %r, hardcore: %r, "
                "dimension: %r, game difficulty: %r (%r), game level_type: %r",
                player.entity_id,
                player.gamemode,
                player.is_hardcore,
                player.dimension,
                world_data.difficulty, difficulty_name,
                world_data.level_type
                )

    gui.set_labels(
        ("player_id", player.entity_id),
        ("gamemode", player.gamemode),
        ("is_hardcore", player.is_hardcore),
        ("dimension", player.dimension),
        ("game difficulty", difficulty_name),
        ("game level_type", world_data.level_type)
    )


def map_(game_: "game.Game", data: bytes):
    pass


def entity(game_: "game.Game", data: bytes):
    pass


def entity_relative_move(game_: "game.Game", data: bytes):
    pass


def entity_look_and_relative_move(game_: "game.Game", data: bytes):
    pass


def entity_look(game_: "game.Game", data: bytes):
    pass


def vehicle_move(game_: "game.Game", data: bytes):
    pass


def open_sign_editor(game_: "game.Game", data: bytes):
    pass


def craft_recipe_response(game_: "game.Game", data: bytes):
    pass


def player_abilities(game_: "game.Game", data: bytes):
    player = game_.data.world_data

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


def disconnect(game_: "game.Game", data: bytes) -> NoReturn:
    player = game_.data.player.data

    reason = converters.extract_json_from_chat(data)[0]
    # reason should be dict Chat type.
    logger.error("% has been disconnected by server. Reason: '%r'",
                 player.username, reason['text'])
    raise DisconnectedByServerException("Disconnected by server.")
