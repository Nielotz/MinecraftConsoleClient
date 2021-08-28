"""Holder for value converters."""

import json
import struct
from typing import Union

from data_structures.position import Position
from misc.consts import MAX_INT, MAX_UINT


def convert_to_varint(value: int) -> bytes:
    """
    Convert int to VarInt.

    :raises ValueError when value not fit into int32
    :returns VarInt in hex bytes
    """

    # Ifs always return.
    if value == 0:
        return bytes(b'\x00')
    if value > 0:
        # Modified version of stolen code from
        # https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0

        varint = bytearray()

        while True:
            byte = value & 0x7F
            value >>= 7
            if value == 0:
                varint.extend(struct.pack('B', byte))
                return bytes(varint)
            varint.extend(struct.pack('B', byte | 0x80))

    # When value is negative
    # Negative varint always has 5 bytes
    varint = bytearray(b'\x80\x80\x80\x80\x00')
    value_in_bytes = value.to_bytes(4, byteorder="little", signed=True)
    varint[0] |= value_in_bytes[0]
    varint[1] |= (value_in_bytes[1] << 1) & 0xFF | value_in_bytes[0] >> 7
    varint[2] |= (value_in_bytes[2] << 2) & 0xFF | value_in_bytes[1] >> 6
    varint[3] |= (value_in_bytes[3] << 3) & 0xFF | value_in_bytes[2] >> 5
    varint[4] |= value_in_bytes[3] >> 4

    return bytes(varint)


def pack_float(value: float) -> bytes:
    """
    Pack float into 4 bytes and return them.

    :param value: value to be packed
    :return: bytes of packed float
    """
    return struct.pack("!f", value)


def pack_double(value: float) -> bytes:
    """
    Pack float into 8 bytes and return them.

    :param value: value to be packed
    :return: bytes of packed float
    """
    return struct.pack("!d", value)


# Not tested.
def pack_unsigned_short(value: int) -> bytes:
    """
    Pack unsigned short into 2 bytes and return them.

    :param value: value to be packed
    :return: bytes of packed value
    """
    return struct.pack("!H", value)


def pack_bool(value: bool) -> bytes:
    """
    Pack value into 1 byte and return it.

    :param value: value to be packed
    :return: bytes of packed float
    """
    if value:
        return b'\x01'
    return b'\x00'


def pack_byte(value) -> bytes:
    """
    Pack value into 1 byte and return it.

    :param value: value to be packed
    :return: bytes of packed float
    """
    return struct.pack("!b", value)


def pack_long(value: float) -> bytes:
    """
    Pack long into 8 bytes and return them.

    :param value: value to be packed
    :return: bytes of packed long
    """
    return struct.pack("!q", value)


# Not tested.
def pack_string(value: str) -> bytes:
    """
    Prefix value with its length as varint.

    :param value: value to be packed
    :return: bytes of packed string
    """
    value = value.encode("utf-8")
    return b''.join((convert_to_varint(len(value)), value))


def extract_bool(data: Union[bytes, memoryview]) -> (bool, int):
    """
    Extract boolean from bytes.

    :param data: bytes or memoryview of at least 1 byte from which extract
    :return True or False, number of read bytes
    """
    assert data

    return data[0] and True, 1


def extract_byte(data: Union[bytes, memoryview]) -> (int, int):
    """
    Extract byte from bytes.

    :param data: bytes or memoryview of at least 1 byte from which extract
    :return byte, number of read bytes
    """
    assert data

    return data[0] - ((data[0] & 0x80) << 1), 1


# Not tested.
def extract_unsigned_byte(data: Union[bytes, memoryview]) -> (int, int):
    """
    Extract unsigned byte from data.

    :param data: bytes or memoryview of at least 1 byte from which extract byte
    :return extracted unsigned byte, number of read bytes
    """
    assert data

    return data[0], 1


# Not tested.
def extract_short(data: Union[bytes, memoryview]) -> (int, int):
    """
    Extract short from data.

    :param data: bytes or memoryview of at least 2 bytes from which extract short
    :return extracted short, number of read bytes
    """
    assert len(data) > 1

    return int.from_bytes(data[0:2], byteorder="big", signed=True), 2


# Not tested.
def extract_int(data: Union[bytes, memoryview]) -> (int, int):
    """
    Extract int from data.

    :param data: bytes or memoryview of at least 4 bytes from which extract int
    :return extracted int, number of read bytes
    """
    assert len(data) > 3

    return int.from_bytes(data[:4], byteorder="big", signed=True), 4


def extract_long(data: Union[bytes, memoryview]) -> (int, int):
    """
    Extract long from data.

    :param data: bytes or memoryview of at least 8 bytes from which extract int
    :return extracted int, number of read bytes
    """
    assert len(data) > 7

    return int.from_bytes(data[:8], byteorder="big", signed=True), 8


# Not tested.
def extract_unsigned_long(data: Union[bytes, memoryview]) -> (int, int):
    """
    Extract long from data.

    :param data: bytes or memoryview of at least 8 bytes from which extract int
    :return extracted long, number of read bytes
    """
    assert len(data) > 7

    return int.from_bytes(data[:8], byteorder="big", signed=False), 8


def extract_float(data: Union[bytes, memoryview]) -> (float, int):
    """
    Extract float from data.

    :param data: bytes or memoryview of at least 4 bytes from which extract float
    :return extracted float, number of read bytes
    """
    assert len(data) > 3

    return struct.unpack('>f', data[:4])[0], 4


def extract_double(data: Union[bytes, memoryview]) -> (float, int):
    """
    Extract double from data.

    :param data: bytes or memoryview of at least 8 bytes from which extract double
    :return extracted double, number of read bytes
    """
    assert len(data) > 7

    return struct.unpack('>d', data[:8])[0], 8


# Not tested.
def extract_string_bytes(data: Union[bytes, memoryview]) -> (bytes, int):
    """
    Extract string from given bytes.

    :param data: decompressed array of bytes
    :return bytes of unicode string, number of read bytes
    """
    assert data

    string_len, read_bytes = extract_varint_as_int(data)

    assert data[read_bytes - 1:]

    string = data[read_bytes: read_bytes + string_len]

    return string, read_bytes + len(string)


# Not tested.
def extract_position(data: Union[bytes, memoryview]) -> (Position, int):
    """
    Extract Position(x, y, z) from data.

    :param data: bytes or memoryview of at least 8 bytes from which extract position
    :returns extracted position, number of read bytes
    """
    # TODO: replace from_bytes with struct.. or another way.
    assert len(data) > 7

    val = int.from_bytes(data[:8], byteorder="big", signed=True)

    z = val & 0x3ffffff
    val >>= 26
    y = val & 0xfff
    x = val >> 12

    if z >= 0x2000000:  # 2 ** 25
        z -= 0x4000000  # 2 ** 26

    return Position(x, y, z), 8


# Not tested.
def extract_json_from_chat(data: Union[bytes, memoryview]) -> (dict, int):
    """
    Extract json from the chat.

    :param data: bytes from which to extract json
    :return extracted json, number of read bytes
    """
    # TODO: return python JSON
    string, read_bytes = extract_string_bytes(data)
    return json.loads(string), read_bytes + len(string)


# Not tested.
def extract_varint_as_int(data: Union[bytes, memoryview]) -> (int, int):
    """
    Extract varint from uncompressed data and returns it as int.


    VarInt can be made up to 5 bytes.
    If not found end of VarInt raises ValueError.

    :raise ValueError: when VarInt not fit into int32
    :param data: bytes of data containing VarInt
    :returns value, number of read bytes
    """
    assert data

    number = 0
    for i in range(5):
        assert len(data) > i - 1

        number |= (data[i] & 0x7F) << 7 * i
        if not data[i] & 0x80:
            break
    else:
        raise ValueError("VarInt is too big!")

    if number > MAX_INT:
        number -= MAX_UINT

    return number, i + 1


# Not tested.
def extract_packet_id(data: Union[bytes, memoryview]) -> (int, int):
    """
    Extract packet ID and payload from packet data.

    :returns packet_id
    """
    return extract_varint_as_int(data)
