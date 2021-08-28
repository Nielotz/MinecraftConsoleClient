from pyinstrument import Profiler

from data_structures.host import Host
from data_structures.player import Player
from game import Game
from misc.logger import get_logger
from versions.version import Version

profiler = Profiler()
profiler.start()

logger = get_logger("mainLogger")

if __name__ == "__main__":

    host: Host = Host("192.168.56.1", 25565)
    # host: Host = Host("188.68.236.16", 25565)
    # host: Host = Host("89.22.210.172", 25565) konrad
    # host: Host = Host("185.243.53.224", 25577)
    # host: Host = Host("nssv.pl", 25565)

    player: Player = Player(username="Bob")

    game_version: Version = Version.v1_12_2

    game = Game(host, player, game_version)
    try:
        game.start()
    except Exception:
        pass
profiler.stop()

profiler.print()
