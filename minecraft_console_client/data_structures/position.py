"""Holder for Position."""


class Position:
    """Hold and allow easy manipulation with positional data."""

    def __init__(self, x: float, y: float, z: float):
        """Create Position(x, y, z) object."""
        self.pos = {'x': x, 'y': y, 'z': z}

    def get_values(self):
        """Return tuple(x, y, z)."""
        pos = self.pos
        return pos['x'], pos['y'], pos['z']

    def __repr__(self):
        """Return string representation of position dictionary."""
        return str(self.pos)
