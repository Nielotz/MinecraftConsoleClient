from versions.defaults.clientbound import Clientbound
from versions.defaults.packet import Packet
from versions.defaults.creator import Creator as DefaultCreator

# print(dir(versions))


class VersionData:
    release_name = ""
    protocol_version_number = 0
    protocol_version_varint = b''  # Can be calculated using utils

    Creator = DefaultCreator

    action_list = {
            "login": {},
            "status": {},
            "play": {}
    }
