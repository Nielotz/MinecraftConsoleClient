"""Module with data necessary to run on 1.12.2."""
import types

import versions.defaults


class VersionData(versions.defaults.VersionData):
    """Hold version data."""

    release_name = "1.12.2"
    protocol_version_number = 340
    protocol_version_varint = b'\xd4\x02'  # Can be calculated using utils

    from versions.v1_12_2.data_structures.game_data import GameData
    game_data: GameData = GameData()

    packet_creator: types.ModuleType
    import versions.v1_12_2.serverbound.packet_creator as packet_creator

    action_list: dict
    from versions.v1_12_2.clientbound.action_list import action_list
