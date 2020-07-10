"""Default module for game versions. Provide view of file structure."""

from versions.defaults.clientbound.action_list import action_list as al
from versions.defaults.serverbound import packet_creator


class VersionData:
    """Hold version data."""

    release_name = ""
    protocol_version_number = 0
    protocol_version_varint = b''  # Can be calculated using utils.

    packet_creator = packet_creator  # Module.
    action_list: dict = al
