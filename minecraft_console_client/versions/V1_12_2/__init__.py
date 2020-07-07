import versions.defaults


class VersionData(versions.defaults.VersionData):
    release_name = "1.12.2"
    protocol_version_number = 340
    protocol_version_varint = b'\xd4\x02'  # Can be calculated using utils

    packet_creator = None
    action_list = None


#  Due to a circular import, imports needs to be here.
import versions.V1_12_2.serverbound.packet_creator as packet_creator
from versions.V1_12_2.clientbound.action_list import action_list

VersionData.packet_creator = packet_creator
VersionData.action_list = action_list
