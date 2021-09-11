from pyinstrument import Profiler

from data_structures.host import Host
from data_structures.hero import Hero
from game import Game
from misc.logger import get_logger
from versions.version import VersionVersion

profiler = Profiler()
profiler.start()

logger = get_logger("mainLogger")

if __name__ == "__main__":

    host: Host = Host("127.0.0.1", 25565)

    hero: Hero = Hero(username="Bob")

    game_version: VersionVersion = VersionVersion.V1_12_2

    game = Game(host, hero)
    try:
        game.start()
    except Exception:
        pass
profiler.stop()

profiler.print()
