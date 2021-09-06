"""Holder for Player."""


class Hero:
    """Contain data related to the player."""

    def __init__(self, username: str):
        from data_structures.entity import Entity
        self.entity: Entity = Entity()

        self.username: str = username

        self.fov_modifier: float = -1
        self.flying_speed: float = -1
        self.active_slot: int = -1

        from data_structures.position import Position
        self.spawn_position: Position = Position(0, 0, 0)

        self.uuid: str = ""
        self.gamemode: int = -1
        self.is_hardcore: bool = False
        self.dimension: int = 0
        self.is_invulnerable: bool = False
        self.is_flying: bool = False
        self.is_allow_flying: bool = False
        self.is_creative_mode: bool = False
        self.food: int = -1
        self.food_saturation: float = -1
