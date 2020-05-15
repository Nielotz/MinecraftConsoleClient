from versions.defaults.creator import Creator as DefaultCreator
from versions.defaults.packet import Packet

from versions.defaults import clientbound_action_list
# print(dir(versions))


class VersionData:
    release_name = ""
    protocol_version_number = 0
    protocol_version_varint = b''  # Can be calculated using utils

    Creator = DefaultCreator

    action_list = clientbound_action_list.action_list
