import socket
import struct

import logging

from hash_tables import PacketIDToBytes
from consts import MAX_INT
import utils


class Connection:
    """
    Handle reading(sending) data from(to) server.
    Auto clean-up when instance being deleted.
    """
    # TODO: improve __del__ to make sure socket closed correctly e.g.
    #   exception catch only "Can't close not open socket"

    connection: socket.socket = None
    """ None when disabled, or number of bytes"""
    compression_threshold = -1

    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        try:
            self.connection.shutdown(socket.SHUT_RDWR)
            logging.info("Shutdown connection")
        except:
            pass
        try:
            self.connection.close()
            logging.info("Closed socket")
        except:
            pass

    def set_compression(self, threshold: int):
        self.compression_threshold = threshold

        if threshold < 0:
            logging.info(f"Compression is disabled")
        else:
            logging.info(f"Compression is enabled, threshold: {threshold}")

    """ Start connection using socket_data(ip/hostname, port).
    On error raise default socket exceptions
    """
    def connect(self, socket_data: (str, int), timeout=5):
        self.connection.settimeout(timeout)
        self.connection.connect(socket_data)

    #  extra_varint == is_nested_another_length ?
    """ Reads packet and returns whole packet (to verify) """
    #  TODO: Verify what is extra_varint,
    #   add exception handling,
    #   add auto uncompress
    def send(self, packet_id: PacketIDToBytes, data):
        return self._send_data(packet_id, data)

    def receive(self) -> (int, memoryview):
        """ Read data from connection
        and return length and memoryview of that data.
        https://stackoverflow.com/a/17668009

        :returns: length of packet, memoryview of read bytes
        :rtype": int, memoryview
        """
        packet_length = self._read_packet_length()

        fragments = []
        read_bytes = 0
        while read_bytes < packet_length:
            packet = self.connection.recv(packet_length - read_bytes)
            if not packet:
                return None
            fragments.append(packet)
            read_bytes += len(packet)

        return packet_length, b''.join(fragments)

    def _read_packet_length(self) -> int:
        """Read and unpack unknown length (up to 5 bytes) varint.
        If not found end of VarInt raise ValueError.
        Stolen from
        https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0

        :returns: varint
        :rtype: int
        """
        length = 0
        for i in range(5):
            ordinal = self.connection.recv(1)

            if len(ordinal) == 0:
                break

            byte = ord(ordinal)
            length |= (byte & 0x7F) << 7 * i

            if not byte & 0x80:
                break
        else:
            raise ValueError("VarInt is too big!")
        if length > MAX_INT:
            raise ValueError("VarInt is too big!")

        return length

    def _send_data(self, packet_id: PacketIDToBytes, arr_with_payload):
        """ Send the data on the connection.
        Stolen from
        https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0
        """
        data = packet_id.value
        logging.debug(f"[SEND] {packet_id.name} {arr_with_payload}")
        data_log = [data, ]
        for arg in arr_with_payload:
            data += utils.pack_data(arg)
            data_log.append(utils.pack_data(arg))

        self.connection.send(utils.convert_to_varint(len(data)) + data)
