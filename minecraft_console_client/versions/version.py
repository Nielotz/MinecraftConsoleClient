"""Provides class which pairs VersionData with version."""

from enum import Enum

import versions.v1_12_2


class Version(Enum):
    """Version Enum containing VersionData."""

    v1_12_2 = versions.v1_12_2.VersionData
