import versions.defaults
from versions.V1_12_2.creator import Creator as PacketCreator
from versions.V1_12_2 import clientbound_action_list


# See versions.defaults.__init__.
class VersionData(versions.defaults.VersionData):
    release_name = "1.12.2"
    protocol_version_number = 340
    protocol_version_varint = b'\xd4\x02'  # Can be calculated using utils

    Creator = PacketCreator

    action_list = clientbound_action_list.action_list
