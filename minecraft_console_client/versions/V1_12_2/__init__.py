import versions.defaults
from versions.V1_12_2.clientbound import Clientbound
from versions.V1_12_2.creator import Creator as PacketCreator


# See versions.defaults.__init__.
class VersionData(versions.defaults.VersionData):
    release_name = "1.12.2"
    protocol_version_number = 340
    protocol_version_varint = b'\xd4\x02'  # Can be calculated using utils

    Creator = PacketCreator

    action_list = {
        "login": {
            0: Clientbound.disconnect,
            # 1: Clientbound._encryption_request,
            2: Clientbound.login_success,
            3: Clientbound.set_compression,
        },
        "play": {
            # 0x00: Clientbound.spawn_object,
            # 0x01: Clientbound.spawn_experience_orb,
            # 0x02: Clientbound.spawn_global_entity,
            # 0x03: Clientbound.spawn_mob,
            # 0x04: Clientbound.spawn_painting,
            # 0x05: Clientbound.spawn_player,
            # 0x06: Clientbound.animation,
            # 0x07: Clientbound.statistics,
            # 0x08: Clientbound.block_break_animation,
            # 0x09: Clientbound.update_block_entity,
            # 0x0A: Clientbound.block_action,
            # 0x0B: Clientbound.block_change,
            # 0x0C: Clientbound.boss_bar,
            0x0D: Clientbound.server_difficulty,
            # 0x0E: Clientbound.tab_complete,
            # 0x0F: Clientbound.chat_message,
            # 0x10: Clientbound.multi_block_change,
            # 0x11: Clientbound.confirm_transaction,
            # 0x12: Clientbound.close_window,
            # 0x13: Clientbound.open_window,
            # 0x14: Clientbound.window_items,
            # 0x15: Clientbound.window_property,
            # 0x16: Clientbound.set_slot,
            # 0x17: Clientbound.set_cooldown,
            # 0x18: Clientbound.plugin_message,
            # 0x19: Clientbound.named_sound_effect,
            0x1A: Clientbound.disconnect,
            0x1B: Clientbound.entity_status,
            # 0x1C: Clientbound.explosion,
            # 0x1D: Clientbound.unload_chunk,
            # 0x1E: Clientbound.change_game_state,
            # 0x1F: Clientbound.keep_alive,
            0x20: Clientbound.chunk_data,
            # 0x21: Clientbound.effect,
            # 0x22: Clientbound.particle,
            0x23: Clientbound.join_game,
            # 0x24: Clientbound.map,
            # 0x25: Clientbound.entity,
            # 0x26: Clientbound.entity_relative_move,
            # 0x27: Clientbound.entity_look_and_relative_move,
            # 0x28: Clientbound.entity_look,
            # 0x29: Clientbound.vehicle_move,
            # 0x2A: Clientbound.open_sign_editor,
            # 0x2B: Clientbound.craft_recipe_response,
            0x2C: Clientbound.player_abilities,
            # 0x2D: Clientbound.combat_event,
            # 0x2E: Clientbound.player_list_item,
            0x2F: Clientbound.player_position_and_look,
            # 0x30: Clientbound.use_bed,
            # 0x31: Clientbound.unlock_recipes,
            # 0x32: Clientbound.destroy_entities,
            # 0x33: Clientbound.remove_entity_effect,
            # 0x34: Clientbound.resource_pack_send,
            # 0x35: Clientbound.respawn,
            # 0x36: Clientbound.entity_head_look,
            # 0x37: Clientbound.select_advancement_tab,
            # 0x38: Clientbound.world_border,
            # 0x39: Clientbound.camera,
            0x3A: Clientbound.held_item_change,
            # 0x3B: Clientbound.display_scoreboard,
            # 0x3C: Clientbound.entity_metadata,
            # 0x3D: Clientbound.attach_entity,
            # 0x3E: Clientbound.entity_velocity,
            # 0x3F: Clientbound.entity_equipment,
            # 0x40: Clientbound.set_experience,
            # 0x41: Clientbound.update_health,
            # 0x42: Clientbound.scoreboard_objective,
            # 0x43: Clientbound.set_passengers,
            # 0x44: Clientbound.teams,
            # 0x45: Clientbound.update_score,
            0x46: Clientbound.spawn_position,
            # 0x47: Clientbound.time_update,
            # 0x48: Clientbound.title,
            # 0x49: Clientbound.sound_effect,
            # 0x4A: Clientbound.player_list_header_and_footer,
            # 0x4B: Clientbound.collect_item,
            # 0x4C: Clientbound.entity_teleport,
            # 0x4D: Clientbound.advancements,
            # 0x4E: Clientbound.entity_properties,
            # 0x4F: Clientbound.entity_effect,
        }
    }
