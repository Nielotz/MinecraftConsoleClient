"""Container for game class."""

import logging

import player
import data_structures.host
import versions.version

logger = logging.getLogger("mainLogger")


class Game:
    """
    Ultimate Container for Life, the Universe, and Everything.

    Main container for game data.
    """
    host = None
    game_version = None
    player_ = None

    def __init__(self,
                 host: data_structures.host.Host,
                 player_: player.Player,
                 game_version: versions.version.Version):
        """
        Create game.

        :param host: where to connect to
        :param player_: to connect as who
        :param game_version: to connect in which game version
        """
        self.host = host
        self.player_ = player_
        self.game_version = game_version

    def run(self):
        """Start game."""

        error_message = self.player_.start()

        self.exit(error_message or "normal exit")

    def exit(self, message=None):
        """Stop everything. Close files, connections."""
        if message is None:
            logger.info("Game stopped peacefully")
        else:
            logger.warning("Game stopped abruptly")
