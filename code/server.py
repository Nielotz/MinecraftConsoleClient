import logging
import unicodedata
import time
import json
import struct

from connection import Connection
from hash_tables import PacketIDToBytes
import utils


class Server:
    socket_data = None

    def __init__(self, address: str, port: int):
        self.socket_data = (address, port)

    def get_status(self, timeout=5):
        """
        Create socket, connect to server, request for information.
        If server is online returns gathered information as JSON, otherwise None.

        :return: status or None
        :rtype: JSON or None
        """

        logging.info(f"Gathering data from: "
                     f"'{self.socket_data[0]}:{self.socket_data[1]}'")
        connection = Connection()

        try:
            connection.connect(self.socket_data, timeout)  # Status request.
        except OSError as e:
            logging.error(f"Can't connect. Reason: {e}")
            return False

        logging.info(f"Connected")

        data = [
            b"\x00",  # Protocol Version
            self.socket_data[0],  # Server Address
            self.socket_data[1],  # Server Port
            b"\x01"  # Next State (status)
        ]
        connection.send(PacketIDToBytes.STATUS, data)
        connection.send(PacketIDToBytes.STATUS, [])

        _, data = connection.read()

        # Send and read unix time
        connection.send(PacketIDToBytes.PING, [time.time() * 1000])
        _, unix = connection.read()
        unix = unix[1::]  # Skip first byte, for some reason

        # Load json and return
        string, _ = utils.extract_string_from_data(data[1::])

        response = json.loads(bytes(string).decode('utf8'))
        # TODO: fix json.decoder.JSONDecodeError: Unterminated string b'5'

        response['ping'] = int(time.time() * 1000) - struct.unpack('q', unix)[0]

        logging.info(f"""Server info: 
    name: {response['version']['name']}
    protocol: {response['version']['protocol']}, version :\
    {response['version']['protocol']} # Change to actual version
    ping: {response['ping']}ms
""")

        return response

