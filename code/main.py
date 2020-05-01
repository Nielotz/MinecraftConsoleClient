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
    #    pass


if __name__ == "__main__":
    run()
