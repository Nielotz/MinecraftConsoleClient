import zlib
from enum import Enum
from typing import Union

from misc.converters import extract_bool, \
    extract_byte, extract_unsigned_byte, extract_short, extract_long, extract_int, extract_unsigned_long, \
    extract_float, extract_double, \
    extract_string_bytes, extract_varint_as_int, extract_packet_id, extract_position, extract_json_from_chat


class TypeToExtract(Enum):
    BOOL: callable = extract_bool
    BYTE: callable = extract_byte
    UNSIGNED_BYTE: callable = extract_unsigned_byte
    SHORT: callable = extract_short
    INT: callable = extract_int
    LONG: callable = extract_long
    UNSIGNED_LONG: callable = extract_unsigned_long
    FLOAT: callable = extract_float
    DOUBLE: callable = extract_double
    STRING_BYTES: callable = extract_string_bytes
    VARINT_AS_INT: callable = extract_varint_as_int
    POSITION: callable = extract_position
    JSON_FROM_CHAT: callable = extract_json_from_chat
    PACKET_ID: callable = extract_packet_id


class PacketDataReader:
    def __init__(self, packet_data: Union[memoryview, bytes], compressed=False):
        self._data = packet_data
        self._data_start_idx = 0

        if compressed:
            self.decompress()

    def decompress(self):
        if self.extract(TypeToExtract.VARINT_AS_INT):  # If data length is not zero.
            self._data = zlib.decompress(self._data[self._data_start_idx:])
            self._data_start_idx = 0

    def extract(self, type_to_extract: TypeToExtract.BOOL):
        value, bytes_read = type_to_extract(self._data[self._data_start_idx:])
        self._data_start_idx += bytes_read
        return value
