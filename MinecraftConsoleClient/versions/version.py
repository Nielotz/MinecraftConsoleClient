"""Provides class which pairs VersionData with version."""

from enum import Enum


class VersionVersion(Enum):
    """Version Enum pairing to VersionData."""

    import versions.v1_12_2
    V1_12_2 = versions.v1_12_2.VersionData


class CurrentVersion:
    """
    Current Version data holder.

    Need to set version_data using select() to run the game code.
    """

    version_data: VersionVersion.value = None

    @staticmethod
    def select(version: VersionVersion.value):
        CurrentVersion.version_data = version
        return version

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("Cannot create Version object! ")
