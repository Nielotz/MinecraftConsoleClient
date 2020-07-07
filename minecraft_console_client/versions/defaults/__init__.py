from versions.defaults.clientbound.action_list import action_list
from versions.defaults.serverbound import packet_creator


class VersionData:
    release_name = ""
    protocol_version_number = 0
    protocol_version_varint = b''  # Can be calculated using utils.

    packet_creator = packet_creator  # Module.
    action_list: dict = action_list
