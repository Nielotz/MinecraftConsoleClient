"""Provides class which pairs VersionData with version"""
from enum import Enum

import versions.V1_12_2


class Version(Enum):
    """Version Enum containing VersionData."""

    V1_12_2 = versions.V1_12_2.VersionData
