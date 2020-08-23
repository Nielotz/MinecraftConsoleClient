"""Holder for GameData."""

from typing import TYPE_CHECKING

from versions.defaults.data_structures.game_data\
    import GameData as BaseGameData

from versions.v1_12_2.data_structures.world import World


class GameData(BaseGameData):
    """Contain data related to the game."""
    world: World = None

    def __init__(self):
        self._init_world()

    def _init_world(self):
        """Initialize world data."""
        self.world = World()
