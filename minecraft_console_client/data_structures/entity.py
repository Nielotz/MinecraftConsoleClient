from data_structures.position import Position


class Entity:
    entity_id: int = None
    position: Position = None
    look_yaw: float = 0
    look_pitch: float = 0
    health: float = None
    on_ground: bool = None
    velocity: [int, int, int] = [None, None, None]  # (x, y, z)

