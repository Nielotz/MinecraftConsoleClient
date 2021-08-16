"""Provides functions which generate given packet."""

import logging

from misc import converters

from versions.v1_12_2.serverbound.packet_id import login

logger = logging.getLogger("mainLogger")


def handshake(host_data: (str, int)) -> bytes:
    """Return handshake packet ready to send."""

    from versions.v1_12_2 import VersionData
    data = [
        login.HANDSHAKE,
        VersionData.protocol_version_varint,  # Protocol Version.
        converters.pack_string(host_data[0]),  # Server Address
        converters.pack_unsigned_short(host_data[1]),  # Server Port
        b'\x02'  # Next State (login)
    ]
    return b''.join(data)


def login_start(username) -> bytes:
    """Return "login start" packet."""
    return b''.join((login.LOGIN_START,
                     converters.pack_string(username)))
