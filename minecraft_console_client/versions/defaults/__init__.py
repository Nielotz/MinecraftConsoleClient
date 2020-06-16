import versions.defaults.clientbound.action_list as clientbound_action_list
from versions.defaults.serverbound import packet_creator


class VersionData:
    release_name = ""
    protocol_version_number = 0
    protocol_version_varint = b''  # Can be calculated using utils

    packet_creator = packet_creator
    action_list = clientbound_action_list.action_list
