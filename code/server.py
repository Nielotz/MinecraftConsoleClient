import logging
import time
import json
import struct

from connection import Connection
from state import State
from packet import PacketID

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

        data = [
            utils.convert_to_varint(340),  # Protocol Version
            self.socket_data[0],  # Server Address
            self.socket_data[1],  # Server Port
            State.REQUEST.value
        ]

        connection.send(PacketID.REQUEST, data)
        connection.send(PacketID.REQUEST, [])

        # len_of_data, data = connection.read()
        len_of_data, data = connection.receive()

        # Send and read unix time
        connection.send(PacketID.PING, [time.time() * 1000])
        len_of_data, unix = connection.receive()

        unix = unix[1::]  # Skip first byte, for some reason

        # Load json and return
        string, _ = utils.extract_string_from_data(data[1::])

        response = json.loads(bytes(string).decode('utf8'))

        response['ping'] = int(time.time() * 1000) - struct.unpack('q', unix)[0]

        logging.info(f"""Server info: 
    name: {response['version']['name']}
    protocol: {response['version']['protocol']}, version :\
    {response['version']['protocol']} # Change to actual version
    ping: {response['ping']}ms
""")

        return response

