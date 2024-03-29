"""Creator and manager of connection to the server."""

import logging
import queue
import socket
import threading
import zlib
from contextlib import suppress

from misc import converters
from misc.consts import MAX_INT
from misc.hashtables import VARINT_BYTES

logger = logging.getLogger('mainLogger')


class Connection:
    """
    Main class that creates and handles TCP connection between server(host) and client.

    Handles reading (sending) data from (to) the server.

    Auto-closes connection when instance being deleted.
    """

    # Positive threshold means number of bytes before start compressing otherwise compression is disabled.
    compression_threshold: int = -1
    _connection: socket.socket = None

    _listener: threading.Thread = None
    _sender: threading.Thread = None

    _ready = threading.Event()

    def __init__(self):
        """Create instance of Connection."""
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        """Close connection."""
        self.close()

    def set_blocking(self, is_blocking: bool = True):
        """Change socket behavior."""
        self._connection.setblocking(is_blocking)

    def connect(self, socket_data: (str, int), timeout: int = 5):
        """
        Start connection using socket_data(ip / hostname, port).

        On error raises standard socket exceptions.

        :param socket_data: tuple(host, port)
        :param timeout: connection timeout
        """
        self._connection.settimeout(timeout)
        self._connection.connect(socket_data)

    def _receive_packet(self) -> bytes:
        """
        Read whole packet from connection.

        Taken from: https://stackoverflow.com/a/17668009

        Returns b'' when connection is broken or sth.

        :returns read bytes
        """
        recv = self._connection.recv
        read_bytes = 0
        fragments = []

        # TODO: Check influence of sleep to the performance.
        # Broad try, because when sth went wrong here we are in danger.
        try:
            packet_length = self._read_packet_length()

            while read_bytes < packet_length:
                packet_part = recv(packet_length - read_bytes)

                if not packet_part:
                    return b''

                fragments.append(packet_part)
                read_bytes += len(packet_part)

        except BrokenPipeError:
            logger.critical("Connection has been broken.")

        except ValueError as err:
            logger.critical("Invalid varint. %s", err)

        except OSError as err:
            logger.critical("Probably connection has been shut down: %s", err)

        except Exception as err:
            logger.critical("<connection#2>Uncaught exception [{}] "
                            "occurred: [%s] %s", err.__class__.__name__, err)
        else:
            return b''.join(fragments)

        return b''

    def start_listener(self, received_queue: queue.Queue) -> bool:
        """
        Start thread that listens packets incoming from the server.

        Similar to start_sending.
        Thread has to be started as daemon.
        Inserts received packet as bytes into received_queue.
        Thread ends when length of a packet or declared length equals zero.
        When connection has been interrupted puts b'' into queue.

        :param received_queue: where to put received packets
        :returns started successfully
        """
        if self._listener is not None and self._listener.is_alive():
            logger.error("Listener already started")
            return False

        self._ready = threading.Event()
        self._listener = threading.Thread(target=self._listen,
                                          args=(received_queue,),
                                          daemon=True)

        # TODO: Tight exceptions.
        with suppress(Exception):
            self._listener.start()
            return self._ready.wait(15)
        return False

    def start_sender(self, to_send: queue.Queue) -> bool:
        """
        Start new thread-daemon which waits for packets to appear in\
        to_send then sends it to the server.

        Similar to start_listening.

        :param to_send: queue from where get and send packets
        :returns started successfully
        """
        if self._sender is not None and self._sender.is_alive():
            logger.error("Sender already started")
            return False

        self._ready = threading.Event()

        self._sender = threading.Thread(target=self._send,
                                        args=(to_send,),
                                        daemon=True
                                        )
        with suppress(Exception):
            self._sender.start()
            return self._ready.wait(15)
        return False

    def _read_packet_length(self) -> int:
        """
        Read and unpack unknown length (up to 5 bytes) VarInt.

        If not found end of VarInt raises ValueError.
        Stolen from
        gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0

        :returns VarInt: int
        """
        # TODO: Merge with converter.
        packet_length = 0
        recv = self._connection.recv
        for i in range(5):
            ordinal = recv(1)
            value, is_next = VARINT_BYTES[ordinal]

            if value is None:
                break
            packet_length |= value << 7 * i

            if not is_next:
                break
        else:
            raise ValueError("VarInt is too big!")

        if packet_length > MAX_INT:
            raise ValueError("VarInt is too big!")

        return packet_length

    def close(self):
        """
        Try to close connection, and stop threads in a nice way.

        Does not ensure that! But gives its best.
        """
        # Shut down one or both halves of the connection.
        with suppress(Exception):
            self._connection.shutdown(socket.SHUT_RDWR)
            logger.info("Shutdown connection")

        # Close a socket file descriptor.
        with suppress(Exception):
            if self._connection.fileno() != -1:
                self._connection.close()
                self._connection: None = None
                logger.info("Closed socket")

        # Closing connection makes listener exit.
        with suppress(Exception):
            if self._listener.is_alive():
                logger.debug("Trying to stop listener...")
                self._listener.join(timeout=20)
                if not self._listener.is_alive():
                    logger.debug("Stopped listener")

        # When listener exits, sends packet that exits sender.
        with suppress(Exception):
            if self._sender.is_alive():
                logger.debug("Trying to stop sender...")
                self._sender.join(timeout=10)
                if not self._sender.is_alive():
                    logger.debug("Stopped sender")

        logger.info("Closed connection")

    def _listen(self, received: queue.Queue):
        """
        Listen for incoming packets, then put into received.

        Similar to _sender.
        Starts listening packets incoming from server.
        When received packet inserts it into buffer queue (received).
        It is blocking function, so has to be run as a daemon.
        Closes when:
            receive packet longer or shorted than declared,
            len(packet) or declared length equals zero.
        On exit puts b'' into queue.

        DOES NOT DECOMPRESS!

        :param received: queue.Queue (FIFO) where read packets append to
        """
        if not threading.current_thread().daemon:
            raise RuntimeError("Thread running start_listening() has to start as daemon!")

        self._ready.set()

        while True:
            packet = self._receive_packet()

            if not packet:
                logger.critical("Received empty packet. Exiting.")
                break
            received.put(packet)

        received.put(None)
        logger.info("Exiting listening thread")

    def _send(self, to_send: queue.Queue):
        """
        Get packet from to_send and send to the server.

        Similar to _listen.
        Starts waiting for bytes to appear in to_send queue then sends it to server.
        It is blocking function, so has to be run in as a daemon.
        Quits when get b'' from to_send queue.

        Job:
            Freezes until packet appear in buffer.
            If compression is enabled and packet exceeds compression_threshold - compresses.
            Sends it to the host.
            Repeat.

        :param to_send: queue.Queue from where to read bytes to send
        """
        if not threading.current_thread().daemon:
            raise RuntimeError("Thread running start_sending() has to be a daemon!")

        self._ready.set()

        to_varint = converters.convert_to_varint
        while True:
            # packet: b'VarInt(Packet ID)' + b'VarInt(Data)'
            payload = to_send.get()

            if not payload:
                logger.critical("Packet is empty.")
                break

            payload_len = len(payload)

            # Compression is disabled
            if self.compression_threshold < 0:
                packet = to_varint(payload_len) + payload

            else:
                # When compression disabled for this packet
                if payload_len < self.compression_threshold:
                    payload = b'\x00' + payload
                else:  # Compression is enabled
                    payload = to_varint(payload_len) + zlib.compress(payload)

                packet = to_varint(len(payload)) + payload
            # End of compression

            try:
                self._connection.sendall(packet)
            except ConnectionAbortedError:
                # Client closed connection.
                logger.critical("Connection has been shut down by client. ")
                break
            except BrokenPipeError:
                # Server closed connection or socket has been shutdown.
                logger.critical(
                    "Probably connection has been shut down. Try again.")
                break
            except OSError as err:
                logger.critical(
                    "Probably connection has been shut down: %s", err)
                break
            except Exception as err:
                logger.critical("<connection#1>Uncaught exception [%s] "
                                "occurred: {%s}", err.__class__.__name__, err)
                break

        logger.info("Exiting sending thread")
