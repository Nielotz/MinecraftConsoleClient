from data_structures.position import Position


class Look:
    def __init__(self,
                 yaw: float = None,
                 pitch: float = None):
        self.yaw: float = yaw
        self.pitch: float = pitch


class Velocity:
    def __init__(self,
                 x: int = 0,
                 y: int = 0,
                 z: int = 0):
        self.x: int = x
        self.y: int = y
        self.z: int = z


class Entity:
    def __init__(self, id_: int = None,
                 position: Position = None,  # Has to be None on default, see player_position_and_look packet.
                 look: Look = Look(),
                 health: float = None,
                 on_ground: bool = None,
                 velocity: Velocity = Velocity()):
        self.id_: int = id_
        self.position: Position = position
        self.look: Look = look
        self.health: float = health
        self.on_ground: bool = on_ground
        self.velocity: Velocity = velocity
        self.flying_speed: float
        self.is_invulnerable: bool

