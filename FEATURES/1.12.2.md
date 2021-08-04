# Handled packet
## Receive
### LOGIN
- [X] 0x00: disconnect
- [ ] 0x01: encryption_request
- [X] 0x02: login_success
- [X] 0x03: set_compression

### PLAY
- [ ] 0x00: spawn_object
- [ ] 0x01: spawn_experience_orb
- [ ] 0x02: spawn_global_entity
- [ ] 0x03: spawn_mob
- [ ] 0x04: spawn_painting
- [ ] 0x05: spawn_player
- [ ] 0x06: animation
- [ ] 0x07: statistics
- [ ] 0x08: block_break_animation
- [ ] 0x09: update_block_entity
- [ ] 0x0A: block_action
- [X] 0x0B: block_change
- [ ] 0x0C: boss_bar
- [X] 0x0D: server_difficulty
- [ ] 0x0E: tab_complete
- [X] 0x0F: chat_message
- [ ] 0x10: multi_block_change
- [ ] 0x11: confirm_transaction
- [ ] 0x12: close_window
- [ ] 0x13: open_window
- [ ] 0x14: window_items
- [ ] 0x15: window_property
- [ ] 0x16: set_slot
- [ ] 0x17: set_cooldown
- [ ] 0x18: plugin_message
- [ ] 0x19: named_sound_effect
- [X] 0x1A: disconnect
- [X] 0x1B: entity_status
- [ ] 0x1C: explosion
- [ ] 0x1D: unload_chunk
- [X] 0x1E: change_game_state
- [X] 0x1F: keep_alive
- [ ] 0x20: chunk_data
- [ ] 0x21: effect
- [ ] 0x22: particle
- [X] 0x23: join_game
- [ ] 0x24: map
- [ ] 0x25: entity
- [ ] 0x26: entity_relative_move
- [ ] 0x27: entity_look_and_relative_move
- [ ] 0x28: entity_look
- [ ] 0x29: vehicle_move
- [ ] 0x2A: open_sign_editor
- [ ] 0x2B: craft_recipe_response
- [X] 0x2C: player_abilities
- [X] 0x2D: combat_event
- [ ] 0x2E: player_list_item
- [X] 0x2F: player_position_and_look
- [ ] 0x30: use_bed
- [ ] 0x31: unlock_recipes
- [ ] 0x32: destroy_entities
- [ ] 0x33: remove_entity_effect
- [ ] 0x34: resource_pack_send
- [X] 0x35: respawn
- [ ] 0x36: entity_head_look
- [ ] 0x37: select_advancement_tab
- [ ] 0x38: world_border
- [ ] 0x39: camera
- [ ] 0x3A: held_item_change
- [ ] 0x3B: display_scoreboard
- [ ] 0x3C: entity_metadata
- [ ] 0x3D: attach_entity
- [ ] 0x3E: entity_velocity
- [ ] 0x3F: entity_equipment
- [ ] 0x40: set_experience
- [X] 0x41: update_health
- [ ] 0x42: scoreboard_objective
- [ ] 0x43: set_passengers
- [ ] 0x44: teams
- [ ] 0x45: update_score
- [X] 0x46: spawn_position
- [ ] 0x47: time_update
- [ ] 0x48: title
- [ ] 0x49: sound_effect
- [ ] 0x4A: player_list_header_and_footer
- [ ] 0x4B: collect_item
- [ ] 0x4C: entity_teleport
- [ ] 0x4D: advancements
- [ ] 0x4E: entity_properties
- [ ] 0x4F: entity_effect

### STATUS

## Send
### LOGIN
- [X] 0x00: HANDSHAKE
- [X] 0x00: LOGIN_START

### PLAY
- [X] 0x00: TELEPORT_CONFIRM
- [ ] 0x01: TABCOMPLETE
- [ ] 0x02: CHAT_MESSAGE
- [X] 0x03: CLIENT_STATUS
- [ ] 0x04: CLIENT_SETTINGS
- [ ] 0x05: CONFIRM_TRANSACTION
- [ ] 0x06: ENCHANT_ITEM
- [ ] 0x07: CLICK_WINDOW
- [ ] 0x08: CLOSE_WINDOW
- [ ] 0x09: PLUGIN_MESSAGE
- [ ] 0x0A: USE_ENTITY
- [X] 0x0B: KEEP_ALIVE
- [ ] 0x0C: PLAYER
- [X] 0x0D: PLAYER_POSITION
- [X] 0x0E: PLAYER_POSITION_AND_LOOK
- [X] 0x0F: PLAYER_LOOK
- [ ] 0x10: VEHICLE_MOVE
- [ ] 0x11: STEER_BOAT
- [ ] 0x12: CRAFT_RECIPE_REQUEST
- [ ] 0x13: PLAYER_ABILITIES
- [ ] 0x14: PLAYER_DIGGING
- [ ] 0x15: ENTITY_ACTION
- [ ] 0x16: STEER_VEHICLE
- [ ] 0x17: CRAFTING_BOOK_DATA
- [ ] 0x18: RESOURCE_PACK_STATUS
- [ ] 0x19: ADVANCEMENT_TAB
- [ ] 0x1A: HELD_ITEM_CHANGE
- [ ] 0x1B: CREATIVE_INVENTORY_ACTION
- [ ] 0x1C: UPDATE_SIGN
- [ ] 0x1d: ANIMATION
- [ ] 0x1e: SPECTATE
- [ ] 0x1f: PLAYER_BLOCK_PLACEMENT
- [ ] 0x20: USE_ITEM

### STATUS
