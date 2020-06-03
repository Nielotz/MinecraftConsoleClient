from data_structures.position import Position


class Mob:
    entity_id: int = None
    position: Position = None
    look_yaw: float = 0
    look_pitch: float = 0
    health: float = None
    on_ground: bool = None
    velocity_x: int = None
    velocity_y: int = None
    velocity_z: int = None

