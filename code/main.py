import logging
logging.basicConfig(level=logging.DEBUG)

from client import Server, get_status
from player import Player


def run():
    server = Server(host="77.55.209.200", port=25565)
    player = Player(u"Bob")
    server.login(player)

    # get_status(address="77.55.209.200", port=25565)

    # minecraft_version.check()


if __name__ == "__main__":
    run()
