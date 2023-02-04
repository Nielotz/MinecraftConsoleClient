"""Provides functions which generate given packet."""

from misc import converters

from versions.v1_12_2.packet.serverbound.create.packet_id import LOGIN as LOGIN_PACKETS_IDS


def handshake(host: str, port: int) -> bytes:
    """Return handshake packet ready to send."""

    from versions.v1_12_2 import VersionData
    data = [
        LOGIN_PACKETS_IDS.HANDSHAKE,
        VersionData.protocol_version_varint,  # Protocol Version.
        converters.pack_string(host),  # Server Address
        converters.pack_unsigned_short(port),  # Server Port
        b'\x02'  # Next State (login)
    ]
    return b''.join(data)


def login_start(username: str) -> bytes:
    """Return "login start" packet."""

    return b''.join((LOGIN_PACKETS_IDS.LOGIN_START,
                     converters.pack_string(username)))
