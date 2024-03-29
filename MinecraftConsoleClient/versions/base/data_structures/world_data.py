"""Holder for GameData."""
from versions.base.data_structures.world.world import World


class WorldData:
    """Contain data related to the game."""

    difficulty = None
    level_type = None
    is_raining: bool = None
    compression_threshold: int = -1
    world: World = None
