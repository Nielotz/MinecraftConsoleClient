import logging

logger = logging.getLogger("mainLogger")

from bot import Bot
from versions.version import Version


def run():
    # Initialize variables.
    # server_data: (str, int) = ("188.68.236.16", 25565)
    server_data: (str, int) = ("51.83.170.185", 9250)
    # server_data: (str, int) = ("nssv.pl", 25565)
    game_version: Version = Version.V1_12_2
    username = "Bob"

    # Create basic objects.
    bot: Bot = Bot(host=server_data, version=game_version, username=username)

    message = bot.start()
    bot.exit(message or "normal exit")
