"""Holder for specific exceptions."""


class DisconnectedError(Exception):
    """Raised when bot has been disconnected by server."""


class InvalidUncompressedPacketError(Exception):
    """Raised when size of uncompressed packet \
    is below compression threshold."""
