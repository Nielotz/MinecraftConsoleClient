"""Module with data necessary to run on 1.12.2."""

import versions.base


class VersionData(versions.base.VersionData):
    """Hold version data."""

    release_name: str = "1.12.2"
    protocol_version_number: int = 340

    from misc.converters import convert_to_varint
    protocol_version_varint: bytes = convert_to_varint(340)  # b'\xd4\x02'

    from versions.v1_12_2.data_structures.world_data import WorldData
    world_data: WorldData = WorldData()

    from types import ModuleType
    packet_creator: ModuleType
    import versions.v1_12_2.serverbound.packet_creator as packet_creator

    packets_specifics: dict
    from versions.v1_12_2.packet.clientbound import packets_specifics

    from versions.v1_12_2.defaults import Defaults
    defaults: Defaults = Defaults()
