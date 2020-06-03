from data_structures.entity import Entity
from data_structures.position import Position


class Player(Entity):
    uuid: str = None
    gamemode: int = None
    is_hardcore: bool = None
    dimension: int = None
    is_invulnerable: bool = None
    is_flying: bool = None
    is_allow_flying: bool = None
    is_creative_mode: bool = None
    flying_speed: float = None
    fov_modifier: float = None
    active_slot: int = None
    spawn_position: Position = None
    username: str = None
    food: int = None
    food_saturation: float = None
