"""Holder for value converters."""

import json
import struct
import zlib

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


def extract_bool(data: memoryview) -> (bool, memoryview):
    """
    Extract boolean from bytes.

    :param data: memoryview of at least 1 byte from which extract
    :return True or False, memoryview of leftover bytes
    """
    assert data

    return bool(data[0]), data[1:]


def extract_byte(data: memoryview) -> (int, memoryview):
    """
    Extract byte from bytes.

    :param data: memoryview of at least 1 byte from which extract
    :return extracted byte, memoryview of leftover bytes
    """
    assert data

    return data[0] - ((data[0] & 0x80) << 1), data[1:]


# Not tested.
def extract_unsigned_byte(data: memoryview) -> (int, memoryview):
    """
    Extract unsigned byte from data.

    :param data: memoryview of at least 1 byte from which extract byte
    :return extracted unsigned byte, memoryview of leftover bytes
    """
    assert data

    return data[0], data[1:]


# Not tested.
def extract_short(data: memoryview) -> (int, memoryview):
    """
    Extract short from data.

    :param data: memoryview of at least 2 bytes from which extract short
    :return extracted short, memoryview of leftover bytes
    """
    assert len(data) > 1

    return int.from_bytes(data[0:2], byteorder="big", signed=True), data[2:]


# Not tested.
def extract_int(data: memoryview) -> (int, memoryview):
    """
    Extract int from data.

    :param data: memoryview of at least 4 bytes from which extract int
    :return extracted int, memoryview of leftover bytes
    """
    assert len(data) > 3

    return int.from_bytes(data[:4], byteorder="big", signed=True), data[4:]


def extract_long(data: memoryview) -> (int, memoryview):
    """
    Extract long from data.

    :param data: memoryview of at least 8 bytes from which extract int
    :return extracted int, memoryview of leftover bytes
    """
    assert len(data) > 7

    return int.from_bytes(data[:8], byteorder="big", signed=True), data[8:]


# Not tested.
def extract_unsigned_long(data: memoryview) -> (int, memoryview):
    """
    Extract long from data.

    :param data: memoryview of at least 8 bytes from which extract int
    :return extracted long, memoryview of leftover bytes
    """
    assert len(data) > 7

    return int.from_bytes(data[:8], byteorder="big", signed=False), data[8:]


def extract_float(data: memoryview) -> (float, memoryview):
    """
    Extract float from data.

    :param data: memoryview of at least 4 bytes from which extract float
    :return extracted float, memoryview of leftover bytes
    """
    assert len(data) > 3

    return struct.unpack('>f', data[:4])[0], data[4:]


def extract_double(data: memoryview) -> (float, memoryview):
    """
    Extract double from data.

    :param data: memoryview of at least 8 bytes from which extract double
    :return extracted double, memoryview of leftover bytes
    """
    assert len(data) > 7

    return struct.unpack('>d', data[:8])[0], data[8:]


# Not tested.
def extract_string_bytes(data: memoryview) -> (bytes, memoryview):
    """
    Extract string from given bytes.

    :param data: decompressed array of bytes
    :return bytes of unicode string, memoryview of leftover bytes
    """
    assert data

    string_len, data = extract_varint_as_int(data)

    assert data

    string = bytes(data[:string_len])

    return string, data[string_len:]


# Not tested.
def extract_position(data: memoryview) -> (Position, memoryview):
    """
    Extract Position(x, y, z) from data.

    :param data: memoryview of at least 8 bytes from which extract position
    :returns extracted position, memoryview of leftover bytes
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

    return Position(x, y, z), data[8:]


# Not tested.
def extract_json_from_chat(data: memoryview) -> (dict, memoryview):
    """
    Extract json from the chat.

    :param data: bytes from which to extract json
    :return extracted json, memoryview of leftover bytes
    """
    # TODO: return python JSON
    string, data = extract_string_bytes(data)
    return json.loads(string), data[len(string):]


# Not tested.
def extract_varint_as_int(data: memoryview) -> (int, memoryview):
    """
    Extract varint from uncompressed data and returns it as int.


    VarInt can be made up to 5 bytes.
    If not found end of VarInt raises ValueError.

    :raise ValueError: when VarInt not fit into int32
    :param data: bytes of data containing VarInt
    :returns value, memoryview of leftover bytes
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

    return number, data[i + 1:]


def decompress(data: memoryview) -> memoryview:
    # TODO: Add check, reintroduce InvalidUncompressedPacketError.
    data_length, data = extract_varint_as_int(data)
    if data_length != 0:  # If data length is not zero.
        return memoryview(zlib.decompress(bytes(data)))
    return data
