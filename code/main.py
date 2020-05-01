import logging
logging.basicConfig(level=logging.DEBUG)

from client import Client
from server import Server
from player import Player


def run():
    server = Server(address="nssv.pl", port=25565)
    server.get_status()

    # client = Client(host=server)
    # player = Player("Bob")
    # if client.login(player):
    #     pass


    # get_status(address="77.55.209.200", port=25565)


if __name__ == "__main__":
    run()
