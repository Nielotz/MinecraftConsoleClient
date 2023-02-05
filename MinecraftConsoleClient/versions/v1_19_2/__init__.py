"""Default module for game versions. Provide view of file structure."""
from misc.converters import convert_to_varint
from types import ModuleType


class VersionData:
    """Hold version data."""

    release_name: str = "1.19.2"
    protocol_version_number: int = 760
    protocol_version_varint: bytes = convert_to_varint(protocol_version_number)

    packet_creator: ModuleType
    action_list: dict
