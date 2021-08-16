"""Module with data necessary to run on 1.12.2."""
import types

import versions.defaults
from misc.converters import convert_to_varint


class VersionData(versions.defaults.VersionData):
    """Hold version data."""

    release_name: str = "1.12.2"
    protocol_version_number: int = 340
    protocol_version_varint: bytes = convert_to_varint(340)  # b'\xd4\x02'

    from versions.v1_12_2.data_structures.game_data import GameData
    game_data: GameData = GameData()

    packet_creator: types.ModuleType
    import versions.v1_12_2.serverbound.packet_creator as packet_creator

    action_list: dict
    from versions.v1_12_2.clientbound.action_list import action_list
