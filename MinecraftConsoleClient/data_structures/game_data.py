import data_structures.hero
import versions.version
from data_structures.host import Host
from versions.version import CurrentVersion


class GameData:
    def __init__(self, host: Host,
                 hero: data_structures.hero.Hero):
        self.host: Host = host
        # TODO: check is server responding / online
        self.hero: data_structures.hero.Hero = hero

        # TODO: check username
        self.version_data: versions.base.VersionData = CurrentVersion.version_data

        if self.version_data is None:
            raise RuntimeError("Did not set CurrentVersion! use CurrentVersion.select(version) before anything else.")

        # TODO: check is game data valid, then remove other checks
        from versions.base.data_structures.world_data import WorldData as WorldData
        self.world_data: WorldData = self.version_data.world_data
