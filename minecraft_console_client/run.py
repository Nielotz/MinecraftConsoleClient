import logging

from player import Player
from data_structures.host import Host
from versions.version import Version

logger = logging.getLogger("mainLogger")


def run():
    # Initialize variables.

    # host: Host = Host("188.68.236.16", 25565)
    host: Host = Host("51.83.170.185", 9250)
    # host: Host = Host("nssv.pl", 25565)

    game_version: Version = Version.v1_12_2
    username = "Bob"

    # Create basic objects.
    bot: Player = Player(host=host, version=game_version, username=username)

    error_message = bot.start()
    bot.exit(error_message or "normal exit")
