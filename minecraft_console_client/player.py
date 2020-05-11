from mob import Mob
from position import Position


class Player(Mob):
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


