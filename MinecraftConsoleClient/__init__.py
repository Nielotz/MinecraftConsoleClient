if __name__ == "__main__":

    from data_structures.host import Host

    host: Host = Host("192.168.56.1", 25565)
    # host: Host = Host("188.68.236.16", 25565)
    # host: Host = Host("89.22.210.172", 25565) konrad
    # host: Host = Host("185.243.53.224", 25577)
    # host: Host = Host("nssv.pl", 25565)

    from versions.version import VersionVersion, CurrentVersion

    # CurrentVersion have to be set using select() before anything related to the game starts.
    game_version: VersionVersion = CurrentVersion.select(VersionVersion.V1_12_2)

    from data_structures.hero import Hero

    # Here you can create hero, and specify game nick.
    hero: Hero = Hero(username="Bob")

    from game import Game

    # Start game.
    game = Game(host, hero, game_version)

    # TODO: rewrite:
    # Check exited with error.
    error = game.start()

    from misc.logger import get_logger

    logger = get_logger("mainLogger")

    if error is not None:
        logger.error("Game has been abruptly stopped. Reason: %r", error)
    else:
        logger.info("Game has been closed.")
