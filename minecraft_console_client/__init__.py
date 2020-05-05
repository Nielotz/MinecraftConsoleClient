import logging
logging.basicConfig(level=logging.DEBUG)

from client import Client, create_client
from player import Player


def run():
    # server_data: (str, int) = ("51.83.170.185", 9250)
    server_data: (str, int) = ("nssv.pl", 25565)

    mc_client: Client = create_client(socket_data=server_data)
    mc_player: Player = Player("Bob")
    if mc_client.login(mc_player):
       pass


if __name__ == "__main__":
    run()
