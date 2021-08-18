"""Holder for specific exceptions."""


class DisconnectedByServerException(Exception):
    pass


class InvalidUncompressedPacketError(Exception):
    """Raised when size of uncompressed packet is below compression threshold."""


class InvalidActionPacketError(Exception):
    """Raised when not found action group in action list."""
