"""Holder for Entity."""

from data_structures.position import Position


class Entity:
    """Contain data related to entity."""

    entity_id: int = None
    position: Position = None
    look_yaw: float = None
    look_pitch: float = None
    health: float = None
    on_ground: bool = None
    velocity: [int, int, int] = [None, None, None]  # (x, y, z)
