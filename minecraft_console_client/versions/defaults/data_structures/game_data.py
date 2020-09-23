"""Holder for GameData."""
from versions.defaults.data_structures.world.world import World


class GameData:
    """Contain data related to the game."""

    difficulty = None
    level_type = None
    is_raining: bool = None
    compression_threshold: int = -1
    world: World = None
