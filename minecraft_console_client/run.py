import logging

logger = logging.getLogger("mainLogger")

from bot import Bot
from versions.version import Version
from data_structures.host import Host


def run():
    # Initialize variables.

    # host: Host = Host("188.68.236.16", 25565)
    host: Host = Host("51.83.170.185", 9250)
    # host: Host = Host("nssv.pl", 25565)

    game_version: Version = Version.V1_12_2
    username = "Bob"

    # Create basic objects.
    bot: Bot = Bot(host=host, version=game_version, username=username)

    error_message = bot.start()
    bot.exit(error_message or "normal exit")
