import versions.defaults

gui = versions.gui


class VersionData(versions.defaults.VersionData):
    release_name = "1.12.2"
    protocol_version_number = 340
    protocol_version_varint = b'\xd4\x02'  # Can be calculated using utils

    packet_creator = None
    action_list = None


from versions.V1_12_2.serverbound import packet_creator
import versions.V1_12_2.clientbound.action_list as clientbound_action_list



VersionData.packet_creator = packet_creator
VersionData.action_list = clientbound_action_list.action_list
