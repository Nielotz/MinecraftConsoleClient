"""Holder for value converters."""

import json
import struct
import zlib
from typing import Union

from data_structures.position import Position
from misc.consts import MAX_INT, MAX_UINT


def convert_to_varint(value: int) -> bytes:
    """
    Convert int to VarInt.

    :raises ValueError when value not fit into int32
    :returns VarInt in hex bytes
    :rtype bytes
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


def extract_varint(data: bytes) -> (int, bytes):
    """
    Unpack varint from uncompressed data.

    VarInt can be made up to 5 bytes.
    If not found end of VarInt raises ValueError.

    :raise ValueError: when VarInt not fit into int32
    :param data: bytes of data containing VarInt
    :returns value, leftover of data or None
    :rtype int, Union[bytes, None]
    """
    number = 0
    for i in range(5):
        byte = data[i]

        number |= (byte & 0x7F) << 7 * i

        if not byte & 0x80:
            break
    else:
        raise ValueError("VarInt is too big!")

    if number > MAX_INT:
        number -= MAX_UINT

    if len(data) > i + 1:
        return number, data[i + 1:]
    return number, None


def extract_data(data: bytes, compression=False) -> (int, bytes):
    """
    Extract packet ID and payload from packet data.

    :returns packet_id, leftover of data or None
    :rtype int, Union[bytes, None]
    """
    if compression:
        data_length, data = extract_varint(data)
        if data_length:
            data = zlib.decompress(data)
        packet_id, data = extract_varint(data)
    else:
        packet_id, data = extract_varint(data)

    return packet_id, data


def pack_float(value: float) -> bytes:
    """
    Pack float into 4 bytes and return them.

    :param value: value to be packed
    :return: bytes of packed float
    :rtype: bytes
    """
    return struct.pack("!f", value)


def pack_double(value: float) -> bytes:
    """
    Pack float into 8 bytes and return them.

    :param value: value to be packed
    :return: bytes of packed float
    :rtype: bytes
    """
    return struct.pack("!d", value)


def pack_unsigned_short(value: int) -> bytes:
    """
    Pack unsigned short into 2 bytes and return them.

    :param value: value to be packed
    :return: bytes of packed value
    :rtype: bytes
    """
    return struct.pack("!H", value)


def pack_long(value: float) -> bytes:
    """
    Pack long into 8 bytes and return them.

    :param value: value to be packed
    :return: bytes of packed long
    :rtype: bytes
    """
    return struct.pack("!q", value)


def pack_byte(value) -> bytes:
    """
    Pack value into 1 byte and return it.

    :param value: value to be packed
    :return: bytes of packed float
    :rtype: bytes
    """
    return struct.pack("!b", value)


def pack_bool(value: bool) -> bytes:
    """
    Pack value into 1 byte and return it.

    :param value: value to be packed
    :return: bytes of packed float
    :rtype: bytes
    """
    if value:
        return b'\x01'
    return b'\x00'


def pack_string(value: str) -> bytes:
    """
    Prefix value with its length as varint.

    :param value: value to be packed
    :return: bytes of packed string
    :rtype: bytes
    """
    value = value.encode("utf-8")
    return b''.join((convert_to_varint(len(value)), value))


def extract_string(data: bytes) -> (bytes, Union[bytes, None]):
    """
    Extract string from given bytes.

    :param data: decompressed array of bytes
    :return bytes of unicode string, leftover of data or None
    :rtype bytes, Union[bytes, None]
    """
    string_len, data = extract_varint(data)
    string = data[:string_len:]

    if len(data) > string_len:
        data = data[string_len:]
        return string, data

    return string, None


def extract_json_from_chat(data: bytes) -> (dict, Union[bytes, None]):
    """
    Extract json from the chat.

    :param data: bytes from which to extract json
    :return extracted json, leftover of data or None
    :rtype int, Union[bytes, None]
    """
    # TODO: return python JSON
    string, leftover = extract_string(data)
    return json.loads(string), leftover


def extract_int(data: bytes) -> (int, Union[bytes, None]):
    """
    Extract int from bytes.

    :param data: at least 4 bytes from which extract int
    :return extracted int, leftover of data or None
    :rtype int, Union[bytes, None]
    """
    value = int.from_bytes(data[:4:], byteorder="big", signed=True)

    if len(data) > 4:
        return value, data[4:]
    return value, None


def extract_unsigned_byte(data: bytes) -> (int, Union[bytes, None]):
    """
    Extract unsigned byte from bytes.

    :param data: at least 1 byte from which extract byte
    :return extracted unsigned byte, leftover of data or None
    :rtype int, Union[bytes, None]
    """
    if len(data) > 1:
        return data[0], data[1:]
    return data[0], None


def extract_boolean(data: bytes) -> (bool, Union[bytes, None]):
    """
    Extract boolean from bytes.

    :param data: at least 1 byte from which extract
    :return True or False, leftover of data or None
    :rtype bool, Union[bytes, None]
    """
    if len(data) > 1:
        return data[0] and True, data[1:]
    return data[0] and True, None


def extract_byte(data: bytes) -> (int, Union[bytes, None]):
    """
    Extract byte from bytes.

    :param data: at least 1 byte from which extract
    :return byte, leftover of data or None
    :rtype byte, Union[bytes, None]
    """
    # int.from_bytes(data[:1:], byteorder="big", signed=True)

    # If negative subtract 256
    if len(data) > 1:
        return data[0] - ((data[0] & 0x80) << 1), data[1:]
    return data[0] - ((data[0] & 0x80) << 1), None


def extract_float(data: bytes) -> (float, Union[bytes, None]):
    """
    Extract float from bytes.

    :param data: at least 4 bytes from which extract float
    :return extracted float, leftover of data or None
    :rtype float, Union[bytes, None]
    """
    value: float = struct.unpack('>f', data[:4:])[0]
    if len(data) > 4:
        return value, data[4:]
    return value, None


def extract_double(data: bytes) -> (float, Union[bytes, None]):
    """
    Extract double from bytes.

    :param data: at least 8 bytes from which extract double
    :return extracted double, leftover of data or None
    :rtype float, Union[bytes, None]
    """
    value: float = struct.unpack('>d', data[:8:])[0]
    if len(data) > 8:
        return value, data[8:]
    return value, None


def extract_position(data: bytes) -> (Position, Union[bytes, None]):
    """
    Extract Position(x, y, z) from data.

    :param data: at least 8 bytes from which extract position
    :returns extracted position, leftover or None when no data left
    :rtype Position, Union[bytes, None]
    """
    # TODO: replace from_bytes with struct.. or another way.
    val = int.from_bytes(data[:8], byteorder="big", signed=True)

    z = val & 0x3ffffff
    val >>= 26
    y = val & 0xfff
    x = val >> 12

    if z >= 0x2000000:  # 2 ** 25
        z -= 0x4000000  # 2 ** 26

    position = Position(x, y, z)

    if len(data) > 8:
        return position, data[8:]
    return position, None


def extract_long(data: bytes) -> (int, Union[bytes, None]):
    """
    Extract long from bytes.

    :param data: at least 8 bytes from which extract int
    :return extracted int, leftover of data or None
    :rtype int, Union[bytes, None]
    """
    value = int.from_bytes(data[:8:], byteorder="big", signed=True)

    if len(data) > 8:
        return value, data[8:]
    return value, None
