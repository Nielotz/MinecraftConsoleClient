"""Module with functions related to given packet."""

import logging
from typing import TYPE_CHECKING, Any

from commands import chat_commands
from data_structures.position import Position
from misc import converters
from misc.exceptions import DisconnectedByServerException
from misc.hashtables import GAMEMODE, GAME_DIFFICULTY
from versions.v1_12_2.packet.clientbound.packet_specific import PacketSpecific
from versions.v1_12_2.serverbound import packet_creator
from versions.v1_12_2.view.view import gui

logger = logging.getLogger("mainLogger")

if TYPE_CHECKING:
    import game


class CombatEvent(PacketSpecific):
    """
    'Now only used to display the game over screen (with enter combat
    and end combat completely ignored by the Notchain client)'
    """

    def __init__(self):
        self.event: int = -1
        self.player_id: int = -1
        self.entity_id: int = -1
        self.message: Any = None

    def read_data(self, data: memoryview):
        self.event, data = converters.extract_varint_as_int(data)

        # TODO: Extract to const
        if self.event == 2:  # Entity dead
            self.player_id, data = converters.extract_varint_as_int(data)
            self.entity_id, data = converters.extract_int(data)
            self.message = converters.extract_json_from_chat(data)

    def default_handler(self, game_: "game.Game"):
        if self.event == 2:
            # 'Entity ID of the player that died
            # (should match the client's entity ID).'
            if self.entity_id == game_.data.hero.entity.id_:

                message = f"Player has been killed by: {self.entity_id}, " \
                          f"death message: '{self.message}' "

                game_.on_death()
            else:
                message = f"Entity: {self.player_id} has been " \
                          f"killed by: {self.entity_id}, death message: '{self.message}' "

            logger.info(message)
            gui.add_to_hotbar(message)


class PlayerListItem(PacketSpecific):
    pass


class PlayerPositionAndLook(PacketSpecific):
    """Auto-send teleport confirm, and game_position_and_look (serverbound)."""

    def __init__(self):
        self.data: memoryview = memoryview(b'-1')
        self.x: float = -1
        self.y: float = -1
        self.z: float = -1
        self.yaw: float = -1
        self.pitch: float = -1
        self.flags: int = -1
        self.teleport_id = None

    def read_data(self, data: memoryview):
        self.data = data

        self.x, data = converters.extract_double(data)
        self.y, data = converters.extract_double(data)
        self.z, data = converters.extract_double(data)
        self.yaw, data = converters.extract_float(data)
        self.pitch, data = converters.extract_float(data)
        self.flags, self.teleport_id = converters.extract_byte(data)


    def default_handler(self, game_: "game.Game"):
        world_data = game_.data.world_data
        player_data = game_.data.hero

        player_pos = player_data.entity.position
        x, y, z = self.x, self.y, self.z
        yaw, pitch = self.yaw, self.pitch
        flags = self.flags
        teleport_id = self.teleport_id

        if player_pos is None:
            player_pos = player_data.entity.position = Position(x, y, z)

            player_data.entity.look.yaw = yaw
            player_data.entity.look.pitch = pitch

        else:
            if flags & 0x01:
                player_pos.x += x
            else:
                player_pos.x = x

            if flags & 0x02:
                player_pos.y += y
            else:
                player_pos.y = y

            if flags & 0x04:
                player_pos.z += z
            else:
                player_pos.z = z

            if flags & 0x08:
                player_data.entity.look.yaw += yaw
            else:
                player_data.entity.look.yaw = yaw

            if flags & 0x10:
                player_data.entity.look.pitch += pitch
            else:
                player_data.entity.look.pitch = pitch

            logger.info("Player pos: %s Look: (yaw: %f, pitch: %f)",
                        player_pos, player_data.entity.look.yaw, player_data.entity.look.pitch)

            gui.set_labels(("Player position", '------------------'),
                           ("x", player_pos.x),
                           ("y", player_pos.y),
                           ("z", player_pos.z),
                           ("yaw", player_data.entity.look.yaw),
                           ("pitch", player_data.entity.look.pitch),
                           ("------------------", '------------------'))

            add_packet = game_.to_send_packets.put

            # Teleport confirm.
            add_packet(packet_creator.play.teleport_confirm(teleport_id))

            # TODO: Check can move to the top, and do not copy.
            # Answer player position and look.
            add_packet(packet_creator.play.player_position_and_look_confirm(bytes(self.data)))


class UseBed(PacketSpecific):
    pass


class UnlockRecipes(PacketSpecific):
    pass


class DestroyEntities(PacketSpecific):
    pass


class RemoveEntityEffect(PacketSpecific):
    pass


class ResourcePackSend(PacketSpecific):
    pass


class Respawn(PacketSpecific):
    def __init__(self):
        self.dimension: int = -1
        self.difficulty = None
        self.gamemode = None
        self.level_type: bytes = b'-1'

    def read_data(self, data: memoryview):
        self.dimension, data = converters.extract_int(data)
        self.difficulty = data[0]
        self.gamemode = data[1]
        self.level_type, _ = converters.extract_string_bytes(data[2:])

    def default_handler(self, game_: "game.Game"):
        world_data = game_.data.world_data

        world_data.dimension = self.dimension
        world_data.difficulty = self.difficulty
        game_.data.hero.gamemode = self.gamemode

        world_data.level_type = self.level_type

        difficulty_name = GAME_DIFFICULTY[world_data.difficulty]

        logger.info("Player respawn: gamemode: %i, dimension: %i, "
                    "game difficulty: %i(%s), game level_type: %s, ",
                    game_.data.hero.gamemode,
                    world_data.dimension,
                    world_data.difficulty, str(difficulty_name),
                    world_data.level_type
                    )

        gui.set_labels(
            ("dimension", world_data.dimension),
            ("game difficulty", difficulty_name),
            ("gamemode", game_.data.hero.gamemode),
            ("game level_type", world_data.level_type)
        )


class EntityHeadLook(PacketSpecific):
    pass


class SelectAdvancementTab(PacketSpecific):
    pass


class WorldBorder(PacketSpecific):
    pass


class Camera(PacketSpecific):
    pass


class HeldItemChange(PacketSpecific):
    def __init__(self):
        self.active_slot: int = -1

    def read_data(self, data: memoryview):
        self.active_slot, _ = converters.extract_byte(data)
    def default_handler(self, game_: "game.Game"):
        player = game_.data.hero

        player.active_slot = self.active_slot
        logger.debug("Held slot changed to %i", player.active_slot)

        gui.set_labels(("Held slot", player.active_slot))


class DisplayScoreboard(PacketSpecific):
    pass


class EntityMetadata(PacketSpecific):
    pass


class AttachEntity(PacketSpecific):
    pass


class EntityVelocity(PacketSpecific):
    pass


class EntityEquipment(PacketSpecific):
    pass


class SetExperience(PacketSpecific):
    pass


class UpdateHealth(PacketSpecific):
    def __init__(self):
        self.health: float = -1
        self.food: int = -1
        self.food_saturation: float = -1

    def read_data(self, data: memoryview):
        self.health, data = converters.extract_float(data)
        self.food, data = converters.extract_varint_as_int(data)
        self.food_saturation = converters.extract_float(data)[0]

    def default_handler(self, game_: "game.Game"):
        """Auto-respawn player."""

        player = game_.data.hero

        player.health = self.health
        player.food = self.food
        player.food_saturation = self.food_saturation

        logger.info("Updated player. Health: %f, Food: %i, Food_saturation: %f",
                    player.health, player.food, player.food_saturation)

        gui.set_labels(("health", player.health),
                       ("food", player.food),
                       ("food_saturation", player.food_saturation))

        if not player.health > 0:
            game_.on_death()


class ScoreboardObjective(PacketSpecific):
    pass


class SetPassengers(PacketSpecific):
    pass


class Teams(PacketSpecific):
    pass


class UpdateScore(PacketSpecific):
    pass


class SpawnPosition(PacketSpecific):
    def __init__(self):
        # noinspection PyTypeChecker
        self.position: Position = None

    def read_data(self, data: memoryview):
        self.position, _ = converters.extract_position(data)
    def default_handler(self, game_: "game.Game"):
        logger.info("Changed player spawn position to %s", self.position)

        gui.set_labels(("Spawn position", self.position))


class TimeUpdate(PacketSpecific):
    pass


class Title(PacketSpecific):
    pass


class SoundEffect(PacketSpecific):
    pass


class PlayerListHeaderAndFooter(PacketSpecific):
    pass


class CollectItem(PacketSpecific):
    pass


class EntityTeleport(PacketSpecific):
    pass


class Advancements(PacketSpecific):
    pass


class EntityProperties(PacketSpecific):
    pass


class EntityEffect(PacketSpecific):
    pass


class BlockBreakAnimation(PacketSpecific):
    pass


class Statistics(PacketSpecific):
    pass


class Animation(PacketSpecific):
    pass


class SpawnPlayer(PacketSpecific):
    pass


class SpawnPainting(PacketSpecific):
    pass


class SpawnMob(PacketSpecific):
    pass


class SpawnGlobalEntity(PacketSpecific):
    pass


class SpawnExperienceOrb(PacketSpecific):
    pass


class SpawnObject(PacketSpecific):
    pass


class UnloadChunk(PacketSpecific):
    pass


class Explosion(PacketSpecific):
    pass


class EntityStatus(PacketSpecific):
    def __init__(self):
        self.entity_id: int = -1
        self.status:int = -1

    def read_data(self, data: memoryview):
        self.entity_id, data = converters.extract_int(data)  # data is 1 byte
        self.status, _ = converters.extract_byte(data)
    def default_handler(self, game_: "game.Game"):
        logger.debug("Entity with id: %i status changed to: %i",
                     self.entity_id, self.status)


class NamedSoundEffect(PacketSpecific):
    pass


class PluginMessage(PacketSpecific):
    pass


class SetCooldown(PacketSpecific):
    pass


class SetSlot(PacketSpecific):
    pass


class WindowProperty(PacketSpecific):
    pass


class WindowItems(PacketSpecific):
    pass


class OpenWindow(PacketSpecific):
    pass


class CloseWindow(PacketSpecific):
    pass


class ConfirmTransaction(PacketSpecific):
    pass


class MultiBlockChange(PacketSpecific):
    pass


class ChatMessage(PacketSpecific):
    def __init__(self):
        self.json_data: Any = None

        # noinspection PyTypeChecker
        self.position: Position = None

    def read_data(self, data: memoryview):
        self.json_data, self.position = converters.extract_json_from_chat(data)
    def default_handler(self, game_: "game.Game"):
        chat_commands.interpret(game_, str(self.json_data))

        gui.add_to_chat(f"{self.position}: {self.json_data}")


class TabComplete(PacketSpecific):
    pass


class UpdateBlockEntity(PacketSpecific):
    pass


class ServerDifficulty(PacketSpecific):
    def __init__(self):
        self.difficulty: int = -1
        self.difficulty_name: str = "-1"

    def read_data(self, data: memoryview):
        self.difficulty, _ = converters.extract_unsigned_byte(data)
        self.difficulty_name = GAME_DIFFICULTY[self.difficulty]
    def default_handler(self, game_: "game.Game"):
        game_.data.world_data.difficulty = self.difficulty

        logger.debug("Server difficulty: %i(%s)",
                     self.difficulty, self.difficulty_name)

        gui.set_labels(("game difficulty", self.difficulty_name))


class BossBar(PacketSpecific):
    pass


class BlockAction(PacketSpecific):
    pass


class BlockChange(PacketSpecific):
    def __init__(self):
        # noinspection PyTypeChecker
        self.position: Position = None
        self.block_id: int = -1

    def read_data(self, data: memoryview):
        self.position, data = converters.extract_position(data)
        self.block_id, _ = converters.extract_varint_as_int(data)

    def default_handler(self, game_: "game.Game"):
        # For debug purposes.
        from versions.base.consts import BLOCK as ID_
        block_type, metadata = self.block_id >> 4, self.block_id & 15
        try:
            print(f"{self.position} is now "
                  f"{ID_[block_type][metadata]['name']}({block_type}:{metadata})")
        except KeyError:
            print(f"{self.position} is unsupported({block_type}:{metadata})")


class ChangeGameState(PacketSpecific):
    def __init__(self):
        self.value: float = -1

    def read_data(self, data: memoryview):
        self.value, _ = converters.extract_float(data[1:])
        # reason = data[0]  # reason = utils.extract_unsigned_byte()[0]
    def default_handler(self, game_: "game.Game"):
        world_data = game_.data.world_data

        # # TODO: Do sth with this:
        #
        # def invalid_bed(val: float):
        #     logger.info("Invalid bed")
        #     gui.add_to_hotbar("Invalid bed")
        #
        # def end_raining(_):
        #     world_data.is_raining = False
        #     logger.info("Stopped raining")
        #     gui.set_labels(("game: is_raining: ", False))
        #
        # def begin_raining(_):
        #     world_data.is_raining = True
        #     logger.info("Started raining")
        #     gui.set_labels(("game: is_raining: ", True))
        #
        # def change_gamemode(val: float):
        #     data.gamemode = GAMEMODE[round(value)]
        #     logger.info("Updated gamemode: %i", data.gamemode)
        #     gui.set_labels(("gamemode", data.gamemode))
        #
        # def exit_end(val: float):
        #     pass
        #
        # def demo_message(val: float):
        #     pass
        #
        # def arrow_hitting_player(_player, val: float):
        #     logger.info("An arrow hit a player")
        #
        # def fade_value(val: float):
        #     pass
        #
        # def fade_time(val: float):
        #     pass
        #
        # def play_elder_guardian_mob_appearance(val: float):
        #     pass


class KeepAlive(PacketSpecific):
    def __init__(self):
        self.data: memoryview = memoryview(b"-1")

    def read_data(self, data: memoryview):
        self.data = data

    def default_handler(self, game_: "game.Game"):
        """Auto-sends keep alive packet."""

        game_.to_send_packets.put(packet_creator.play.keep_alive(self.data))


class ChunkData(PacketSpecific):
    def __init__(self):
        self.data: bytes = b'-1'

    def read_data(self, data: memoryview):
        self.data = data
    def default_handler(self, game_: "game.Game"):
        game_.data.world_data.world.parse_chunk_packet(self.data)


class Effect(PacketSpecific):
    pass


class Particle(PacketSpecific):
    pass


class JoinGame(PacketSpecific):
    def __init__(self):
        self.entity_id: int = -1
        self.gamemode: int = -1
        self.gamemode_name: str = "-1"
        self.is_hardcore: bool = False
        self.dimension: int = -1
        self.difficulty: int = -1
        self.difficulty_name: str = "-1"
        self.level_type:bytes = b"-1"

    def read_data(self, data: memoryview):
        self.entity_id, data = converters.extract_int(data)

        self.gamemode, data = converters.extract_unsigned_byte(data)
        self.gamemode_name = GAMEMODE[self.gamemode & 0b00000111]
        self.is_hardcore = bool(self.gamemode & 0b00001000)

        self.dimension, data = converters.extract_int(data)

        self.difficulty, data = converters.extract_unsigned_byte(data)
        self.difficulty_name = GAME_DIFFICULTY[self.difficulty]

        # Was once used by the client to draw the player list, but now is ignored.
        # player.player._server_data["max_players"], data =  utils.extract_unsigned_byte(data)

        data = data[1:]
        # default, flat, largeBiomes, amplified, default_1_1
        self.level_type, _ = converters.extract_string_bytes(data)

    def default_handler(self, game_: "game.Game"):
        world_data = game_.data.world_data
        player = game_.data.hero

        player.entity_id = self.entity_id

        gamemode = self.gamemode

        player.gamemode = self.gamemode_name

        player.is_hardcore = self.is_hardcore

        player.dimension = self.dimension

        world_data.difficulty = self.difficulty
        difficulty_name = self.difficulty_name

        # default, flat, largeBiomes, amplified, default_1_1
        world_data.level_type = self.level_type

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


class Map(PacketSpecific):
    pass


class Entity(PacketSpecific):
    pass


class EntityRelativeMove(PacketSpecific):
    pass


class EntityLookAndRelativeMove(PacketSpecific):
    pass


class EntityLook(PacketSpecific):
    pass


class VehicleMove(PacketSpecific):
    pass


class OpenSignEditor(PacketSpecific):
    pass


class CraftRecipeResponse(PacketSpecific):
    pass


class PlayerAbilities(PacketSpecific):
    def __init__(self):
        self.flags: int = -1
        self.is_invulnerable: bool = False
        self.is_flying: bool = False
        self.is_allow_flying: bool = False
        self.is_creative_mode: bool = False
        self.flying_speed: float = -1
        self.fov_modifier: float = -1

    def read_data(self, data: memoryview):
        self.flags, data = converters.extract_byte(data)
        self.is_invulnerable = bool(self.flags & 0x01)
        self.is_flying = bool(self.flags & 0x02)
        self.is_allow_flying = bool(self.flags & 0x04)
        self.is_creative_mode = bool(self.flags & 0x08)

        self.flying_speed, data = converters.extract_float(data)

        self.fov_modifier, _ = converters.extract_float(data)

    def default_handler(self, game_: "game.Game"):
        player = game_.data.world_data

        player.is_invulnerable = self.is_invulnerable
        player.is_flying = self.is_flying
        player.is_allow_flying = self.is_allow_flying
        player.is_creative_mode = self.is_creative_mode

        player.flying_speed = self.flying_speed

        player.fov_modifier = self.fov_modifier

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


class Disconnect(PacketSpecific):
    def __init__(self):
        self.reason: dict = {-1:-1}

    def read_data(self, data: memoryview):
        self.reason, _ = converters.extract_json_from_chat(data)

    def default_handler(self, game_: "game.Game"):
        player = game_.data.hero

        # reason should be dict Chat type.
        logger.error("% has been disconnected by server. Reason: '%r'",
                     player.username, self.reason['text'])
        raise DisconnectedByServerException("Disconnected by server.")
