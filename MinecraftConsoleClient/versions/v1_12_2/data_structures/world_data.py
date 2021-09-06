from versions.base.data_structures.world_data import WorldData as BaseWorldData

from versions.v1_12_2.data_structures.world.world import World


class WorldData(BaseWorldData):
    world: World = None

    def __init__(self):
        self._init_world()

    def _init_world(self):
        self.world = World()
