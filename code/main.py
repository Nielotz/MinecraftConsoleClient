import logging
import data_types
logging.basicConfig(level=logging.INFO)

from server import Server


def run():
    server = Server(domain_name="nssv.pl", port=25565)


#if __name__ == "__main__":
    #run()
