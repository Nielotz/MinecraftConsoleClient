import socket
import struct


class Packet:
    connection: socket.socket = None

    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        self.connection.shutdown(socket.SHUT_RDWR)
        self.connection.close()

    def connect(self, socket_data: (str, int), timeout=5):
        self.connection.settimeout(timeout)
        self.connection.connect(socket_data)

    #  extra_varint == is_nested_another_length ?
    def read(self, extra_varint=False):
        return self._read_fully(extra_varint)

    def send(self, *args):
        return self._send_data(*args)

    def _unpack_varint(self):
        """Unpack the varint.
        Stolen from
        https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0
        """
        data = 0
        for i in range(5):
            ordinal = self.connection.recv(1)

            if len(ordinal) == 0:
                break

            byte = ord(ordinal)
            data |= (byte & 0x7F) << 7 * i

            if not byte & 0x80:
                break

        return data

    #  extra_varint == is_nested_another_length ?
    def _read_fully(self, extra_varint=False):
        """ Read the connection and return the bytes.
        Stolen from
        https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0
        """
        packet_length = self._unpack_varint()
        packet_id = self._unpack_varint()
        byte = b''

        if extra_varint:
            # Packet contained netty header offset for this
            if packet_id > packet_length:
                self._unpack_varint()

            extra_length = self._unpack_varint()

            while len(byte) < extra_length:
                byte += self.connection.recv(extra_length)

        else:
            byte = self.connection.recv(packet_length)

        return byte

    def _pack_data(self, data):
        """ Page the data.
        Stolen from
        https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0
        """
        if type(data) is str:
            data = data.encode('utf8')
            return self._pack_varint(len(data)) + data
        elif type(data) is int:
            return struct.pack('H', data)
        elif type(data) is float:
            return struct.pack('Q', int(data))
        else:
            return data

    def _pack_varint(self, data):
        """ Pack the var int.
        Stolen from
        https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0
        """
        ordinal = b''

        while True:
            byte = data & 0x7F
            data >>= 7
            ordinal += struct.pack('B', byte | (0x80 if data > 0 else 0))

            if data == 0:
                break

        return ordinal

    def _send_data(self, *args):
        """ Send the data on the connection.
        Stolen from
        https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0
        """
        data = b''

        for arg in args:
            data += self._pack_data(arg)

        self.connection.send(self._pack_varint(len(data)) + data)


