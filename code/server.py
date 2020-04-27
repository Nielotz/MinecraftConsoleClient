import json
import time
import struct

import logging
logging.basicConfig(level=logging.INFO)

from packet import Packet


class Server:
    socket_data = None
    packet: Packet = None

    # TODO change params to class IP with ip parser, etc.
    def __init__(self, address, port):
        logging.info(f"Server address: '{address}:{port}'")

        self.socket_data = (address, port)
        self.packet = Packet()

    def connect(self, timeout=5):
        self.packet.connect(self.socket_data, timeout)

        #  TODO: verify connection
        logging.info("Connected")
        self._handshake()

    def __del__(self):
        logging.info("Disconnecting")

    def status(self):
        self.packet.send(b'\x00')  # Status request.
        # Read response, offset for string length
        data = self.packet.read(extra_varint=True)

        # Send and read unix time
        self.packet.send(b'\x01', time.time() * 1000)
        unix = self.packet.read()

        # Load json and return
        response = json.loads(data.decode('utf8'))
        response['ping'] = int(time.time() * 1000) - struct.unpack('Q', unix)[0]

        try:
            logging.info(f"Server info: version: {response['version']}")
            logging.info(f"    players: {response['players']}")
            logging.info(f"    ping:  {response['ping']}ms")
        except:
            pass

        return response


    def _handshake(self):
        self.packet.send(b'\x00\x00',  # Protocol Version
                         self.socket_data[0],  # Server Address
                         self.socket_data[1],  # Server Port
                         b'\x01'  # Next State (status)
                         )

