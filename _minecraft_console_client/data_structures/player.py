import logging

from data_structures.player_data import PlayerData

logger = logging.getLogger("mainLogger")


class Player:
    """Main player object ."""

    data: PlayerData = None

    def __init__(self, username: str = None):
        """Create and initialize player."""
        self.data = PlayerData()
        self.data.username = username
