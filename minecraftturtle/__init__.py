import logging
logging.basicConfig(level=logging.DEBUG)

from client import Client, create_client
from server import Server
from player import Player


def run():
    server: Server = Server(address="nssv.pl", port=25565)
    server.get_status()

    client: Client = create_client(host=server)
    player: Player = Player("Bob")
    if client.login(player):
       pass


if __name__ == "__main__":
    run()
