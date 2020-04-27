import logging
logging.basicConfig(level=logging.DEBUG)

from server import Server


def run():
    server = Server(address="nssv.pl", port=25565)
    server.connect()
    server.status()

if __name__ == "__main__":
    run()
