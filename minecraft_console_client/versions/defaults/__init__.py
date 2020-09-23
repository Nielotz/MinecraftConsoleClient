"""Default module for game versions. Provide view of file structure."""

from typing import TYPE_CHECKING

from versions.defaults.clientbound.action_list import action_list as al
from versions.defaults.serverbound import packet_creator

from versions.defaults.data_structures.game_data import GameData


class VersionData:
    """Hold version data."""

    release_name = ""
    protocol_version_number = 0
    protocol_version_varint = b''  # Can be calculated using utils.

    game_data = GameData()
    packet_creator = packet_creator  # Module.
    action_list: dict = al
