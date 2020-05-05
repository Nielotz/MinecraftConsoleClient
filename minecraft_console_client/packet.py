from collections import namedtuple
from enum import Enum
import logging
import queue
import threading
import select
import time

from version import VersionNamedTuple, Version
from state import State
from connection import Connection
import utils

PacketIDNamedTuple = namedtuple("PacketIDNamedTuple", "int bytes")


class PacketID(Enum):
    """
    Packet name => PacketIDNamedTuple(int, hex byte value in two's complement)
    """

    REQUEST = PacketIDNamedTuple(0, b'\x00')
    HANDSHAKE = PacketIDNamedTuple(0, b'\x00')
    LOGIN_START = PacketIDNamedTuple(0, b'\x00')
    TELEPORT_CONFIRM = PacketIDNamedTuple(0, b'\x00')
    DISCONNECT_LOGIN = PacketIDNamedTuple(0, b'\x00')
    PING = PacketIDNamedTuple(0, b'\x01')
    LOGIN_SUCCESS = PacketIDNamedTuple(2, b'\x02')
    CHAT_MESSAGE_SERVERBOUND = PacketIDNamedTuple(2, b'\x02')
    CLIENT_STATUS = PacketIDNamedTuple(3, b'\x03')
    SET_COMPRESSION = PacketIDNamedTuple(3, b'\x03')
    CLIENT_SETTINGS = PacketIDNamedTuple(4, b'\x04')
    PLUGIN_MESSAGE_SERVERBOUND = PacketIDNamedTuple(9, b'\x09')
    KEEP_ALIVE_SERVERBOUND = PacketIDNamedTuple(11, b'\x0b')
    CHAT_MESSAGE_CLIENTBOUND = PacketIDNamedTuple(15, b'\x0F')
    OPEN_WINDOW = PacketIDNamedTuple(19, b'\x13')
    PLUGIN_MESSAGE_CLIENTBOUND = PacketIDNamedTuple(15, b'\x18')
    DISCONNECT_PLAY = PacketIDNamedTuple(26, b'\x1A')
    CHANGE_GAME_STATE = PacketIDNamedTuple(30, b'\x1E')
    KEEP_ALIVE_CLIENTBOUND = PacketIDNamedTuple(31, b'\x1F')
    JOIN_GAME = PacketIDNamedTuple(35, b'\x23')
    PLAYER_POSITION_AND_LOOK = PacketIDNamedTuple(47, b'\x2F')
    RESPAWN = PacketIDNamedTuple(53, b'\x35')
    PLAYER_LIST_HEADER_AND_FOOTER = PacketIDNamedTuple(74, b'\x4A')


# class PacketDisconnect()

def _pack_packet(packet_id: PacketID, arr_with_payload):
    """
    Stolen from
    https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0
    """
    data = bytearray(packet_id.value.bytes)
    logging.debug(f"[SEND] {packet_id.name} {arr_with_payload}")

    for arg in arr_with_payload:
        data.extend(utils.pack_data(arg))

    # logging.debug(f"[PACKED] {data}")

    return data


class Login:
    @staticmethod
    def create_handshake(server_data: (str, int),
                         protocol_version: VersionNamedTuple) -> bytearray:
        """ Returns handshake packet ready to send """
        data = [
            protocol_version.version_number_bytes,  # Protocol Version
            server_data[0],  # Server Address
            server_data[1],  # Server Port
            State.LOGIN.value  # Next State (login)
            ]
        packed_packet = _pack_packet(PacketID.HANDSHAKE, data)

        return packed_packet

    @staticmethod
    def create_login_start(username):
        """ Returns "login start" packet """
        packed_packet = _pack_packet(PacketID.LOGIN_START, [username])
        return packed_packet


class Status:

    @staticmethod
    def create_request():
        """ Returns request packet """
        packed_packet = _pack_packet(PacketID.REQUEST, [])
        return packed_packet

    @staticmethod
    def create_ping(actual_time: float):
        """ Returns ping packet """
        packed_packet = _pack_packet(PacketID.PING, [actual_time])
        return packed_packet

    @staticmethod
    def create_handshake(server_data: (str, int),
                         protocol_version: Version) -> bytearray:
        """ Returns handshake packet """
        data = [
            protocol_version.value.version_number_bytes,  # Protocol Version
            server_data[0],  # Server Address
            server_data[1],  # Server Port
            State.STATUS.value  # Next State (login)
            ]
        packed_packet = _pack_packet(PacketID.HANDSHAKE, data)

        return packed_packet


class Listener:
    @staticmethod
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
                            logging.warning(f"Buffer for incoming packets is full!")

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
                            logging.warning(f"Buffer for incoming packets is full!")

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

