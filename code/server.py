import logging
import time
import json
import struct

from connection import Connection
from state import State
from packet import Status, Login
from version import Version

import utils


class Server:
    """
    Main server related action manager.

    """

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

        packet = Status.create_handshake(self.socket_data, Version.ANY)
        connection.send(packet)

        packet = Status.create_request()
        connection.send(packet)

        # len_of_data, data = connection.read()
        len_of_data, data = connection.receive()

        string, _ = utils.extract_string_from_data(data[1::])
        response = json.loads(bytes(string).decode('utf8'))

        # Send and read unix time
        packet = Status.create_ping(time.time() * 1000)
        connection.send(packet)

        len_of_data, unix = connection.receive()

        unix = unix[1::]  # Skip first byte, for some reason

        # Load json and return

        response['ping'] = int(time.time() * 1000) - struct.unpack('q', unix)[0]

        logging.info(f"""Server info: 
    name: {response['version']['name']}
    protocol: {response['version']['protocol']}
    ping: {response['ping']}ms
""")

        return response

