"""Module with data necessary to run on 1.12.2."""

import versions.defaults


class VersionData(versions.defaults.VersionData):
    """Hold version data."""

    release_name = "1.12.2"
    protocol_version_number = 340
    protocol_version_varint = b'\xd4\x02'  # Can be calculated using utils

    game_data = None
    packet_creator = None
    action_list = None


#  Due to a circular import, imports needs to be here.
import versions.v1_12_2.serverbound.packet_creator as packet_creator
from versions.v1_12_2.clientbound.action_list import action_list
from versions.v1_12_2.data_structures.game_data import GameData

VersionData.packet_creator = packet_creator
VersionData.action_list = action_list
VersionData.game_data = GameData()
