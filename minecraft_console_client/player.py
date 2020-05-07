import logging
import sys
import queue
import threading
import time

from connection import Connection
from version import Version, VersionNamedTuple
import action
import utils

from packet import Creator


def critic_exit(message=None):
    logging.critical(f"Something went wrong: {message}")
    sys.exit(-1)


class Player:
    """
    Manages player behavior. Highest API level
    Imitate last stage e.g. "game": system->client->GAME
    """
    _host: (str, int) = None
    version: VersionNamedTuple = None
    action_list: dict = None

    listener: threading.Thread = None
    sender: threading.Thread = None

    _conn: Connection = None

    _data: dict = {"username": "Anyone"}

    received_queue: queue.Queue = queue.Queue()
    to_send_queue: queue.Queue = queue.Queue()

    __stop_threads = False

    def __init__(self, host: (str, int), version: Version, username: str):
        """
        :param host: host data (address, port) to which client connects to
        :param version: VersionNamedTuple object from VERSION,
                        tells which version of protocol to use
        :param username:
        """

        logging.info("Creating player".center(60, "-"))

        self._data["username"] = username
        logging.info("|" +
                     f"Username: '{self._data['username']}'".center(58, " ") +
                     "|")

        self.version = version.value
        logging.info("|" +
                     f"Client version: '{self.version.release_name}'".center(58, " ") + "|")

        self._host = host
        logging.info("|" + f"Server address: '{self._host[0]}: {self._host[1]}'"
                     .center(58, " ") + "|")
        self._conn = Connection()

        self.action_list = action.get_action_list(self.version)

        logging.info("".center(60, "-"))

        self.listener = threading.Thread(target=self.start_listening,
                         args=(self.received_queue, 0,),
                         daemon=True
                         )

        self.sender = threading.Thread(target=self.start_sending,
                         args=(self.to_send_queue, ),
                         daemon=True
                         )

    def __del__(self):
        self.stop()  # Temporally

    def start(self):
        """ Starts as bot. """

        logging.info(f"Starting bot: '{self._data['username']}'")
        if not self.connect_to_server():
            critic_exit("Can't connect to the server")
            return False
        try:
            self.listener.start()
            self.sender.start()
        except Exception:
            self.stop("Cannot create thread")

        if not self.login():
            if not self.stop("Cannot login to the server"):
                critic_exit("Cannot stop threads")
            else:
                logging.info("Cannot login to the server")
                return False
        logging.info("Successfully logged in.")

    # TODO: Refract
    def stop(self, reason=""):
        logging.info(f"Stopping program. Reason: {reason}")
        __stop_threads = True
        success = [True, True]
        if self.listener is not None and self.listener.is_alive():
            success[0] = False
            logging.debug(f"Stopping receiving thread. Attempt 0/5")
            attempt = 1
            time.sleep(5)
            while attempt < 6:
                if not self.listener.is_alive():
                    logging.debug("Successfully stopped receiving thread.")
                    success[0] = True
                    break
                logging.debug(f"Stopping receiving thread. Attempt {attempt}/5")
                time.sleep(5)
                attempt += 1
            else:
                if self.listener.is_alive():
                    logging.warning("Failed to stop receiving thread.")
                else:
                    success[0] = True
                    logging.debug("Successfully stopped receiving thread.")
        else:
            logging.debug("Successfully stopped receiving thread.")

        if self.sender is not None and self.sender.is_alive():
            success[1] = False
            logging.debug(f"Stopping sending thread. Attempt 0/5")
            attempt = 1
            time.sleep(5)
            while attempt < 6:
                if not self.sender.is_alive():
                    logging.debug("Successfully stopped sending thread.")
                    success[1] = True
                    break
                logging.debug(f"Stopping sending thread. Attempt {attempt}/5")
                time.sleep(5)
                attempt += 1
            else:
                if self.sender.is_alive():
                    logging.warning("Failed to stop sending thread.")
                else:
                    logging.debug("Successfully stopped sending thread.")
                    success[1] = True
        else:
            logging.debug("Successfully stopped receiving thread.")

        return success[0] and success[1]

    def connect_to_server(self):
        """
        Connects to server.

        :returns: success
        :rtype: bool

        """
        # TODO: add retry, timeout, etc...
        if not self.__connect():
            return False
        return True

    def login(self):
        """
        # TODO: Make this comment readable
        Login to offline (non-premium) server e.g. without encryption.

        :return True when logged in otherwise False
        :rtype bool
        """
        logging.info("Trying to log in in offline mode")

        logging.info("Established connection with: "
                     f"'{self._host[0]}:"
                     f"{self._host[1]}'")

        packet = Creator.Login.handshake(self._host, self.version)
        self.to_send_queue.put(packet)

        packet = Creator.Login.login_start(self._data["username"])
        self.to_send_queue.put(packet)

        for i in range(10):  # Try for 10 packets
            data = self.received_queue.get(timeout=10)
            if len(data) == 0:
                logging.error("Received 0 bytes")
                return False
            packet_id, data = utils.unpack_varint(data)

            if self.interpret_login_packet(packet_id, data):
                return True
        return False

    def interpret_packet(self, packet_id: int, payload: bytes):
        logging.debug(f"[1/2] Interpreting packet with id: {packet_id}")

        if packet_id in self.action_list:
            self.action_list[packet_id](self, payload)
        else:
            logging.debug("[2/2] Not implemented yet")

    def interpret_login_packet(self, packet_id: int, payload: bytes):
        logging.debug(f"[1/2] Interpreting packet with id: {packet_id}")

        if packet_id in self.action_list:
            self.action_list[packet_id](self, payload)
            if packet_id == 2:
                return True
        else:
            logging.debug("[2/2] Not implemented yet")
        return False

    def start_listening(self, buffer: queue.Queue,
                        check_delay=0.050):
        """
        Similar to start_sending. Has to starts as daemon.
        Starts listening packets incoming from server.
        When received packet (if need) - decompresses,
        then inserts it into buffer.
        It is blocking function, so has to be run in a new thread.
        Otherwise thread should closes right after the parent thread closes.

        Job:
            Receives all packets waiting to be received,
            appends them to buffer specified in constructor,
            sleeps for check_delay [seconds].
            Repeat.

        :param buffer: queue.Queue (FIFO) where read packets append to
        :param check_delay: delay in seconds that
                            specifies how long sleep between receiving packets
        """

        if not threading.current_thread().daemon:
            raise RuntimeError("Thread start_sending ")

        while not self.__stop_threads:
            _, packet = self._conn.receive_packet()
            while buffer.full():
                time.sleep(check_delay)
                logging.warning(f"Buffer for incoming packets is full!")

            buffer.put(packet)
            # logging.debug(f"[RECEIVED] {len(packet)} bytes.")

    def start_sending(self, buffer: queue.Queue):
        """
        Similar to start_listen. Has to starts as daemon.
        Starts waiting for packets to appear in buffer then send it to the server.
        It is blocking function, so has to be run in a new thread.
        Thread will stop before 10 sec pass after self.__stop_threads set to True.

        Job:
            Freeze until packet appear in buffer,
            send it the connection.
            Repeat.

        :param buffer: queue.Queue (FIFO) from where packets are reads
        """

        if not threading.current_thread().daemon:
            raise RuntimeError(
                "Thread running start_sending() has to be a daemon!")

        # TODO: change to wait and signals
        while not self.__stop_threads:
            try:
                packet = buffer.get(block=True, timeout=10)
            except queue.Empty:
                pass
            else:
                self._conn.send(packet)

    def __connect(self, timeout=5):
        """
        Connects to server.
        Not raises exceptions.

        :param timeout: connection timeout
        :returns True when connected, otherwise False
        :rtype bool
        """

        try:
            self._conn.connect(self._host, timeout)
        except OSError as e:
            logging.critical(f"Can't connect to: "
                             f"'{self._host[0]}:"
                             f"{self._host[1]}'"
                             f", reason: {e}")
            return False
        return True



