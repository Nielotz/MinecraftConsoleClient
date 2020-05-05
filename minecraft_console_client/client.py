import logging

from connection import Connection
from player import Player

from version import Version, VersionNamedTuple
from packet import PacketID, Login
import queue
import threading
import select
import time


import utils


def create_client(socket_data: (str, int)):
    # TODO:
    """
    Creates object Client.

    :return: Client
    """

    return Client(socket_data, Version.V1_12_2)


class Client:
    """
    Main client action manager.
    Provides methods to control:
        client,
        client.player: Player.
    """

    player: Player = None
    _socket_data: (str, int) = None
    _connection: Connection = None
    _version: VersionNamedTuple = None

    def __init__(self, socket_data: (str, int), version: Version):
        """
        :param host: Server object to which client connects to
        :param version: VersionNamedTuple object from VERSION,
                        tells which version of protocol to use
        """

        logging.info(f"Server address: '{socket_data[0]}:"
                     f"{socket_data[1]}'")

        self._socket_data = socket_data
        self._version = version.value
        self._connection = Connection()

    def login(self, player: Player):
        """
        # TODO: Make this comment readable
        Login to offline (non-premium) server e.g. without encryption, as player.

        :param player: Player
        :return True when logged in otherwise False
        :rtype bool
        """
        logging.info("Trying to log in in offline mode")

        if not self.__connect():
            return False
        self.player = player

        logging.info("Established connection with: "
                     f"'{self._socket_data[0]}:"
                     f"{self._socket_data[1]}'")

        packet = Login.create_handshake(self._socket_data, self._version)
        self._connection.send(packet)

        packet = Login.create_login_start(self.player.data["username"])
        self._connection.send(packet)

        is_logged = self.__handle_login_packets()
        return is_logged

    def __connect(self, timeout=5):
        """
        Connects to server.
        Not raises exceptions.

        :param timeout: connection timeout
        :returns True when connected, otherwise False
        :rtype bool
        """

        try:
            self._connection.connect(self._socket_data, timeout)
        except OSError as e:
            logging.critical(f"Can't connect to: "
                             f"'{self._socket_data[0]}:"
                             f"{self._socket_data[1]}'"
                             f", reason: {e}")
            return False
        return True

    # TODO: Packets...
    def __handle_login_packets(self) -> bool:
        """
        Handles packets send by server during login process e.g.:
        "Set Compression (optional)" and "Login Success".

        :returns True when successfully logged in, otherwise False
        :rtype bool
        """

        packet_length, data = self._connection.receive_packet()

        # Protection from crash when server is starting
        if len(data) == 0:
            return False

        packet_id, data = utils.unpack_varint(data)

        logging.debug(f"[RECEIVED] ID: {packet_id}, payload: {bytes(data)}")

        if packet_id == PacketID.SET_COMPRESSION.value.int:
            threshold, _ = utils.unpack_varint(data)
            self._connection.set_compression(threshold)

            # Next packet have to be login success
            packet_length, data = self._connection.receive_packet()
            packet_id, data = utils.extract_data(data,
                    compression=not (self._connection._compression_threshold < 0)
                                                 )

        logging.debug(f"[RECEIVED] ID: {packet_id}, payload: {bytes(data)}")

        if packet_id == 2:  # PacketID.LOGIN_SUCCESS.value:
            uuid, data = utils.extract_string_from_data(data)
            uuid = bytes(uuid).decode('utf-8')
            self.player.data["uuid"] = uuid
            logging.info(f"Player UUID: {uuid}")
            return True

        return False


def start_listen(conn: Connection, buffer: queue.Queue, check_delay=0.050):
    """
    Starts listening packets incoming from server.
    It is blocking function, so has to be run in a new thread.
    Starting thread as daemon gives free performance boost.
    Otherwise thread should closes right after the parent thread closes.

    Job:
        Receives all packets waiting to be received,
        appends them to buffer specified in constructor,
        sleeps for check_delay [seconds].
        Repeat.

    :param conn: socket.socket to receive packets from
    :param buffer: queue.Queue (FIFO) where read packets append to
    :param check_delay: delay in seconds that
                        specifies how long sleep between receiving packets
    """

    conn.setblocking(False)
    ready = select.select([conn], [], [], 0.01)

    # Test#1:
    #   check is better to sleep, or use recv with setblocking(True)

    _skipped = 0  # Only for test #1
    _hit = 0  # Only for test #1
    _sum = 0  # Only for test #1

    # After testing this code will be cleaned up.
    if threading.current_thread().daemon:
        while True:
            if ready:  # Only for test #1
                while ready:
                    _hit += 1  # Only for test #1
                    _, packet = conn.receive_packet()
                    while buffer.full():
                        time.sleep(check_delay)
                        logging.warning(
                            f"Buffer for incoming packets is full!")

                    buffer.put(packet)
                    logging.debug(f"[RECEIVED] {len(packet)} bytes.")

            else:  # Only for test #1
                _skipped += 1  # Only for test #1
                time.sleep(check_delay)

            if _sum > 10:  # Only for test #1
                print(f"Hit: {_hit}, skip: {_skipped}")  # Only for test #1
                _skipped = 0  # Only for test #1
                _hit = 0  # Only for test #1
                _sum = 0  # Only for test #1
    else:
        logging.warning("Please start listen() in a daemon!")
        while threading.main_thread().is_alive():
            if ready:  # Only for test #1
                while ready:
                    _hit += 1  # Only for test #1
                    _, packet = conn.receive_packet()
                    while buffer.full():
                        time.sleep(check_delay)
                        logging.warning(
                            f"Buffer for incoming packets is full!")

                    buffer.put(packet)
                    logging.debug(f"[RECEIVED] {len(packet)} bytes.")

            else:  # Only for test #1
                _skipped += 1  # Only for test #1
                time.sleep(check_delay)

            if _sum > 10:  # Only for test #1
                print(f"Hit: {_hit}, skip: {_skipped}")  # Only for test #1
                _skipped = 0  # Only for test #1
                _hit = 0  # Only for test #1
                _sum = 0  # Only for test #1

        else:
            print("While loop makes sense!")