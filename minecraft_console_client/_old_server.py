import logging
import time
import json
import struct

from connection import Connection
from packet import Status
from version import Version

import utils


def get_status(host, port, timeout=5):
    """
    Creates socket, connects to server, requests for information.
    If server is online returns gathered information as JSON, otherwise None.

    :return: status or None
    :rtype: JSON or None
    """

    logging.info(f"Gathering data from: '{host}:{port}'")
    connection = Connection()

    try:
        connection.connect((host, port), timeout)  # Status request.
    except OSError as e:
        logging.error(f"Can't connect. Reason: {e}")
        return False

    logging.info(f"Connected")

    packet = Status.handshake((host, port), Version.ANY)
    connection.send(packet)

    packet = Status.request()
    connection.send(packet)

    # len_of_data, data = connection.read()
    len_of_data, data = connection.receive()

    string, _ = utils.extract_string_from_data(data[1::])
    response = json.loads(bytes(string).decode('utf8'))

    # Send and read unix time
    packet = Status.ping(time.time() * 1000)
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

