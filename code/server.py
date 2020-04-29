import json
import time
import struct

import logging
logging.basicConfig(level=logging.INFO)

from connection import Connection
from hash_tables import ProtocolVersion


def get_status(address, port):
        """
        Create socket, connect to server, request for information.
        On success return json, on error False
        Should not raise exception

        :returns: False or server information
        :rtype: json
        """
        # Todo: add to json / log version in str sample: 1.12.2

        logging.info(f"Gathering data from: '{address}:{port}'")
        connection = Connection()

        logging.info(f"Connecting to: '{address}:{port}'")
        try:
            connection.connect((address, port), 5)  # Status request.
        except OSError as e:
            logging.error(f"Can't connect to: '{address}:{port}', reason: {e}")
            return False
        else:
            logging.info(f"Connected")

        connection.send(b'\x00\x00',  # Protocol Version
                        address,  # Server Address
                        port,  # Server Port
                        b'\x01'  # Next State (status)
                        )
        connection.send(b'\x00')

        # Read response, offset for string length
        data = connection.read(extra_varint=True)

        # Send and read unix time
        connection.send(b'\x01', time.time() * 1000)
        unix = connection.read()

        # TODO: Fix JSONDecodeError("Expecting value", s, err.value) from None
        #   raised when server is starting

        # Load json and return
        response = json.loads(data.decode('utf8'))
        response['ping'] = int(time.time() * 1000) - struct.unpack('Q', unix)[0]

        try:
            logging.info(f"Server info: version: {response['version']} \n"
                         f"    ping:  {response['ping']}ms")  # \n for long name

        except:  # Issue with logging, e.g. some of response fields not exist
            pass

        return response


class Server:
    socket_data = None
    connection: Connection = None

    def __init__(self, host, port):
        # TODO change params to class IP with ip parser, etc.

        logging.info(f"Server address: '{host}:{port}'")

        self.socket_data = (host, port)
        self.connection = Connection()

    def connect(self, timeout=5):
        logging.info(f"Connecting to: "
                     f"'{self.socket_data[0]}:{self.socket_data[1]}'")
        try:
            self.connection.connect(self.socket_data, timeout)  # Status request.
        except OSError as e:
            logging.error(f"Can't connect to: "
                          f"'{self.socket_data[0]}:{self.socket_data[1]}'"
                          f", reason: {e}")
            return False

        logging.info("Connected")
        return True

    def __del__(self):
        pass



