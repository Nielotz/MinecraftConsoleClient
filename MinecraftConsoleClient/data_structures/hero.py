"""Holder for Player."""

from data_structures.entity import Entity
from data_structures.position import Position


class Hero:
    """Contain data related to the player."""

    def __init__(self,
                 username: str = None,
                 fov_modifier: float = None,
                 flying_speed: float = None,
                 active_slot: int = None,
                 uuid: str = None,
                 gamemode: int = None,
                 is_hardcore: bool = None,
                 dimension: int = None,
                 is_invulnerable: bool = None,
                 is_flying: bool = None,
                 is_allow_flying: bool = None,
                 is_creative_mode: bool = None,
                 spawn_position: Position = None,
                 food: int = None,
                 food_saturation: float = None,
                 entity: Entity = Entity()):

        self.entity: Entity = entity

        self.username: str = username

        self.fov_modifier: float = fov_modifier
        self.flying_speed: float = flying_speed
        self.active_slot: int = active_slot

        self.uuid: str = uuid
        self.gamemode: int = gamemode
        self.is_hardcore: bool = is_hardcore
        self.dimension: int = dimension
        self.is_invulnerable: bool = is_invulnerable
        self.is_flying: bool = is_flying
        self.is_allow_flying: bool = is_allow_flying
        self.is_creative_mode: bool = is_creative_mode
        self.spawn_position: Position = spawn_position
        self.food: int = food
        self.food_saturation: float = food_saturation
