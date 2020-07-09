"""Holder for GameData."""

from data_structures.player_data_holder import PlayerDataHolder


class GameData:
    """Contain data related to the game."""

    difficulty = None
    level_type = None
    is_raining: bool = None
    player_data_holder: PlayerDataHolder = None
