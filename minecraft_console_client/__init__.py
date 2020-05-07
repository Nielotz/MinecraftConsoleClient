import logging
logging.basicConfig(level=logging.DEBUG)

from player import Player
from version import VersionNamedTuple, Version


def run():
    # Initialize variables.
    server_data: (str, int) = ("51.83.170.185", 9250)
    # server_data: (str, int) = ("nssv.pl", 25565)
    game_version: VersionNamedTuple = Version.V1_12_2
    username = "Bob"

    # Create basic objects.
    mc_player: Player = Player(host=server_data,
                               version=game_version,
                               username=username)

    mc_player.start()


if __name__ == "__main__":
    run()
