import json
import struct
import zlib

from data_structures.position import Position
from misc.consts import MAX_INT, MAX_UINT


class PacketDataReader:
    def __init__(self, packet_data: bytes, compressed=False):
        self._data = packet_data

        if compressed:
            self.decompress()
        else:
            self._data_start_idx = 0

    def decompress(self):
        if self.extract_varint_as_int():  # If data length is not zero.
            self._data = zlib.decompress(self._data[self._data_start_idx:])
            self._data_start_idx = 0

    def extract_bool(self) -> bool:
        """
        Extract boolean from bytes.

        :return True or False
        """
        assert len(self._data) > self._data_start_idx

        value = self._data[self._data_start_idx] and True

        self._data_start_idx += 1

        return value

    def extract_byte(self) -> int:
        """
        Extract byte from bytes.

        :return byte
        """
        assert len(self._data) > self._data_start_idx

        byte = self._data[self._data_start_idx]

        self._data_start_idx += 1

        return byte - ((byte & 0x80) << 1)

    # Not tested.
    def extract_unsigned_byte(self) -> int:
        """
        Extract unsigned byte from bytes.

        :return extracted unsigned byte
        """
        assert len(self._data) > self._data_start_idx

        value = self._data[self._data_start_idx]

        self._data_start_idx += 1

        return value

    # Not tested.
    def extract_short(self) -> int:
        """
        Extract short from bytes.

        :return extracted short
        """
        assert len(self._data) > self._data_start_idx + 2

        value = int.from_bytes(self._data[self._data_start_idx:self._data_start_idx + 2], byteorder="big", signed=True)

        self._data_start_idx += 2

        return value

    # Not tested.
    def extract_int(self) -> int:
        """
        Extract int from bytes.

        :return extracted int
        """
        assert len(self._data) > self._data_start_idx + 3

        value = int.from_bytes(self._data[self._data_start_idx:self._data_start_idx + 4:], byteorder="big", signed=True)

        self._data_start_idx += 4

        return value

    def extract_long(self) -> int:
        """
        Extract long from bytes.

        :return extracted int
        """
        assert len(self._data) > self._data_start_idx + 7

        value = int.from_bytes(self._data[self._data_start_idx:self._data_start_idx + 8:], byteorder="big", signed=True)

        self._data_start_idx += 8

        return value

    # Not tested.
    def extract_unsigned_long(self) -> int:
        """
        Extract long from bytes.

        :return extracted long
        """
        assert len(self._data) > self._data_start_idx + 7

        value = int.from_bytes(self._data[self._data_start_idx:self._data_start_idx + 8:],
                               byteorder="big", signed=False)

        self._data_start_idx += 8

        return value

    def extract_float(self) -> float:
        """
        Extract float from bytes.

        :return extracted float
        """
        assert len(self._data) > self._data_start_idx + 3

        value = struct.unpack('>f', self._data[self._data_start_idx:self._data_start_idx + 4:])[0]

        self._data_start_idx += 4

        return value

    def extract_double(self) -> float:
        """
        Extract double from bytes.

        :return extracted double
        """
        assert len(self._data) > self._data_start_idx + 7

        value = struct.unpack('>d', self._data[self._data_start_idx:self._data_start_idx + 8:])[0]

        self._data_start_idx += 8

        return value

    # Not tested.
    def extract_string_bytes(self) -> bytes:
        """
        Extract string from given bytes.

        :return bytes of unicode string
        """
        assert len(self._data) > self._data_start_idx

        string_len = self.extract_varint_as_int()

        assert len(self._data) > self._data_start_idx + string_len

        value = self._data[self._data_start_idx:self._data_start_idx + string_len]

        self._data_start_idx += 1

        return value

    # Not tested.
    def extract_position(self) -> Position:
        """
        Extract Position(x, y, z) from self._data.

        :returns extracted position
        """
        # TODO: replace from_bytes with struct.. or another way.
        assert len(self._data) > self._data_start_idx + 7

        val = int.from_bytes(self._data[self._data_start_idx:self._data_start_idx + 8], byteorder="big", signed=True)

        self._data_start_idx += 8

        z = val & 0x3ffffff
        val >>= 26
        y = val & 0xfff
        x = val >> 12

        if z >= 0x2000000:  # 2 ** 25
            z -= 0x4000000  # 2 ** 26

        return Position(x, y, z)

    # Not tested.
    def extract_json_from_chat(self) -> dict:
        """
        Extract json from the chat.

        :return extracted json
        """
        return json.loads(self.extract_string_bytes())

    # Not tested.
    def extract_varint_as_int(self) -> int:
        """
        Extract varint from uncompressed self._data and returns it as int.

        VarInt can be made up to 5 bytes.
        If not found end of VarInt raises ValueError.

        :raise ValueError: when VarInt not fit into int32
        :returns value
        """
        assert len(self._data) > self._data_start_idx

        number = 0
        for i in range(5):
            assert len(self._data) > self._data_start_idx + i

            byte = self._data[self._data_start_idx + i]

            self._data_start_idx += 1

            number |= (byte & 0x7F) << 7 * i

            if not byte & 0x80:
                break
        else:
            raise ValueError("VarInt is too big!")

        if number > MAX_INT:
            number -= MAX_UINT

        return number

    # Not tested.
    def extract_packet_id(self) -> int:
        """
        Extract packet ID and payload from packet data.

        :returns packet_id
        """
        return self.extract_varint_as_int()
