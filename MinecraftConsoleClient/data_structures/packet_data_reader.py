import zlib
from enum import Enum

from misc.converters import extract_bool, \
    extract_byte, extract_unsigned_byte, extract_short, extract_long, extract_int, extract_unsigned_long, \
    extract_float, extract_double, \
    extract_string_bytes, extract_varint_as_int, extract_packet_id, extract_position, extract_json_from_chat


class TypeToExtract(Enum):
    BOOL: extract_bool
    BYTE: extract_byte
    UNSIGNED_BYTE: extract_unsigned_byte
    SHORT: extract_short
    INT: extract_int
    LONG: extract_long
    UNSIGNED_LONG: extract_unsigned_long
    FLOAT: extract_float
    DOUBLE: extract_double
    STRING_BYTES: extract_string_bytes
    VARINT_AS_INT: extract_varint_as_int
    POSITION: extract_position
    JSON_FROM_CHAT: extract_json_from_chat
    STRING_BYTES: extract_string_bytes
    PACKET_ID: extract_packet_id


class PacketDataReader:
    def __init__(self, packet_data: bytes, compressed=False):
        self._data = packet_data
        self._data_start_idx = 0

        if compressed:
            self.decompress()

    def decompress(self):
        if self.extract(TypeToExtract.VARINT_AS_INT):  # If data length is not zero.
            self._data = zlib.decompress(self._data[self._data_start_idx:])
            self._data_start_idx = 0

    def extract(self, type_to_extract: TypeToExtract):
        value, bytes_read = type_to_extract.value(self._data)
        self._data_start_idx += bytes_read
        return value
