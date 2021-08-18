"""Default module for game versions. Provide view of file structure."""
import types

from versions.defaults.data_structures.world_data import WorldData


class VersionData:
    """Hold version data."""

    release_name: str = ""
    protocol_version_number: int = 0
    protocol_version_varint: bytes = b''  # Can be calculated using utils.

    world_data: WorldData = WorldData()

    packet_creator: types.ModuleType
    from versions.defaults.serverbound import packet_creator

    action_list: dict
    from versions.defaults.clientbound.action_list import action_list

