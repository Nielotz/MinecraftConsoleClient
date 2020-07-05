import logging

logger = logging.getLogger("mainLogger")

from misc import utils
from versions.V1_12_2.serverbound.packet_id import login
from versions.V1_12_2 import VersionData


def handshake(host_data: (str, int)) -> bytes:
    """ Returns handshake packet ready to send """
    data = [
        VersionData.protocol_version_varint,  # Protocol Version.
        host_data[0],  # Server Address
        host_data[1],  # Server Port
        b'\x02'  # Next State (login)
    ]
    return utils.pack_data(login.HANDSHAKE, data)


def login_start(username) -> bytes:
    """ Returns "login start" packet """
    return utils.pack_data(login.LOGIN_START, [username])
