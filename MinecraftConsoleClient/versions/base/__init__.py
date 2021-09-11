"""Default module for game versions. Provide view of file structure."""


class VersionData:
    """Hold version data."""

    release_name: str = ""
    protocol_version_number: int = 0
    protocol_version_varint: bytes = b''  # Can be calculated using utils.

    from versions.base.data_structures.world_data import WorldData
    world_data: WorldData = WorldData()

    from types import ModuleType
    packet_creator: ModuleType
    from versions.base.serverbound import packet_creator

    action_list: dict
    from versions.base.clientbound.action_list import action_list

    from versions.base.defaults import Defaults
    defaults: Defaults = Defaults()
