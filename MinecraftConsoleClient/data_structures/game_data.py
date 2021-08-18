import data_structures.host
import data_structures.player
import versions.version
from misc.logger import get_logger
from versions.defaults.data_structures.world_data import WorldData as WorldData

logger = get_logger("game_data")


class GameData:
    def __init__(self, host: data_structures.host.Host,
                 player: data_structures.player.Player,
                 game_version: versions.version.Version):
        self.host: data_structures.host.Host = host
        # TODO: check is server responding / online
        self.player: data_structures.player.Player = player
        # TODO: check username
        self.version_data: versions.defaults.VersionData = game_version.value
        # TODO: check is game data valid, then remove other checks
        self.world_data: WorldData = self.version_data.world_data
