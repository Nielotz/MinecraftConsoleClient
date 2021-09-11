"""Provides class which pairs VersionData with version."""

from enum import Enum

import versions.v1_12_2
import versions.base


class VersionVersion(Enum):
    """Version Enum pairing to VersionData."""

    V1_12_2: versions.base.VersionData = versions.v1_12_2.VersionData


class CurrentVersion:
    """
    Current Version data holder.

    Need to set version_data using select() to run the game code.
    """

    version_data: VersionVersion.V1_12_2 = VersionVersion.V1_12_2

    @staticmethod
    def select(version: VersionVersion.V1_12_2):
        CurrentVersion.version_data = version.value
        return version.value

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("Cannot create CurrentVersion object! Instead use class fields and static methods.")
