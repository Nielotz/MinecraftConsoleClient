"""Holder for Position."""


class Position:
    """Hold and allow easy manipulation with positional data."""

    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        """Create Position(x, y, z) object."""

        self.x = x
        self.y = y
        self.z = z

    def set(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        """Return string representation of position dictionary."""
        return f"x: {self.x}, y: {self.y}, z: {self.z}"
