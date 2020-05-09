import logging

logger = logging.getLogger("mainLogger")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# fh = logging.FileHandler()
# fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

from player import Player
from version import VersionNamedTuple, Version


def run():
    # Initialize variables.
    server_data: (str, int) = ("51.83.170.185", 9250)
    # server_data: (str, int) = ("nssv.pl", 25565)
    game_version: Version = Version.V1_12_2
    username = "Bob"

    # Create basic objects.
    bot: Player = Player(host=server_data,
                         version=game_version,
                         username=username)

    message = bot.start()
    bot.stop(message or "normal exit")


if __name__ == "__main__":
    run()


