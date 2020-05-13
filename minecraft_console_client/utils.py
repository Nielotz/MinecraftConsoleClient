import struct
import zlib
import json
import struct
from typing import Union, Any

from consts import MAX_INT, MIN_INT, MAX_UINT
from position import Position



def convert_to_varint(value: int) -> bytes:
    """
    Converts int to VarInt.
    If value not fit into int32 - raises ValueError

    :raises ValueError when value not fit into int32
    :returns VarInt in hex bytes
    :rtype bytes
    """

    if value > MAX_INT:
        raise ValueError(f"value: '{value}' is too big for VarInt")
    if value < MIN_INT:
        raise ValueError(f"value: '{value}' is too small for VarInt")

    if value == 0:
        return bytes(b'\x00')
    if value > 0:
        """
        Stolen from
        https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0
        """
        varint = bytearray()

        while value != 0:
            byte = value & 0x7F
            value >>= 7
            varint.extend(struct.pack('B', byte | (0x80 if value != 0 else 0)))
        return bytes(varint)

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


def unpack_varint(data: bytes) -> (int, bytes):
    """
    Unpacks varint from uncompressed data and returns unpacked int and leftover.
    If not found end of VarInt raise ValueError.

    VarInt can be made up to 5 bytes.

    Algorithm stolen from
    https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0

    :raise ValueError: when VarInt not fit into int32
    :param data: bytes of data containing VarInt
    :returns value, leftover of data or None
    :rtype int, Union[bytes, None]
    """

    number = 0

    for i in range(5):
        try:
            byte = data[i]
        except IndexError:
            raise ValueError("VarInt is too big!")

        number |= (byte & 0x7F) << 7 * i

        if not byte & 0x80:
            break
    else:
        raise ValueError("VarInt is too big!")

    if number > MAX_INT:
        number -= MAX_UINT

    try:
        return number, data[i + 1::]
    except IndexError:
        return number, None


def extract_data(data: bytes, compression=False) -> (int, bytes):
    """
    Extracts Packet ID and payload from packet data.

    :returns packet_id, leftover of data or None
    :rtype int, Union[bytes, None]
    """

    if compression:
        data_length, data = unpack_varint(data)
        if data_length:
            data = zlib.decompress(data)
        packet_id, data = unpack_varint(data)
        return packet_id, data

    else:
        packet_id, data = unpack_varint(data)
        return packet_id, data


def _pack_data(data: Any) -> bytes:
    """
    Pages the data.
    Stolen from
    https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0

    :param data: data to pack
    :returns bytes of paged data
    :rtype bytes
    """

    if type(data) is str:
        data = data.encode('utf8')
        return convert_to_varint(len(data)) + data
    elif type(data) is int:
        return struct.pack('H', data)
    elif type(data) is float:
        return struct.pack('q', int(data))
    else:
        return data


def pack_payload(packet_id: bytes, arr_with_payload) -> bytes:
    """
    Packs packet_id and data from arr_with_payload into blob of data.

    :returns packed bytes
    :rtype bytes
    """
    data = bytearray(packet_id)

    for arg in arr_with_payload:
        data.extend(_pack_data(arg))

    return bytes(data)


def extract_string(data: bytes) -> (bytes, Union[bytes, None]):
    """
    Extracts string from given bytes.

    :param data: decompressed array of bytes
    :return bytes of string(unicode(pure bytes)), leftover of data or None
    :rtype bytes, Union[bytes, None]
    """

    string_len, data = unpack_varint(data)

    string = data[:string_len:]
    try:
        data = data[string_len::]
    except IndexError:
        data = None
    return string, data


def extract_json_from_chat(data: bytes) -> (dict, Union[bytes, None]):
    string, leftover = extract_string(data)

    return json.loads(string), leftover


def extract_int(data: bytes) -> (int, Union[bytes, None]):
    """
    Extracts int from bytes.

    :param data: bytes from which extract int
    :return extracted int, leftover of data or None
    :rtype int, Union[bytes, None]
    """
    value = int.from_bytes(data[0:4:], byteorder="big", signed=True)
    try:
        return value, data[4::]
    except IndexError:
        return value, None


def extract_unsigned_byte(data: bytes) -> (int, Union[bytes, None]):
    """
    Extracts unsigned byte from bytes.

    :param data: bytes from which extract int
    :return extracted unsigned byte, leftover of data or None
    :rtype int, Union[bytes, None]
    """
    value = int.from_bytes(data[0:1:], byteorder="big", signed=True)
    assert data[0] == value
    try:
        return value, data[1::]
    except IndexError:
        return value, None


def extract_boolean(data: bytes) -> (bool, Union[bytes, None]):
    """
    Extracts boolean from bytes.

    :param data: bytes from which extract
    :return True or False, leftover of data or None
    :rtype bool, Union[bytes, None]
    """
    try:
        return data[0], data[1::]
    except IndexError:
        return data[0] and True, None


def extract_byte(data: bytes) -> (int, Union[bytes, None]):
    """
    Extracts byte from bytes.

    :param data: bytes from which extract
    :return byte, leftover of data or None
    :rtype byte, Union[bytes, None]
    """
    value = int.from_bytes(data[0:1:], byteorder="big", signed=True)
    try:
        return value, data[1::]
    except IndexError:
        return value, None

# def extract_slot(data: bytes) -> (Item, bytes):
#     """
#     Extracts slot item from given bytes.
#     Slot:
#         Boolean  True if there is an item in this position; false if it is empty.
#         VarInt    The item ID. Omitted if present is false
#         Item Count Optional Byte
#         NBT        If 0, there is no NBT data, and no further data follows.
#
#     :param data: bytes from which extract int
#
#     :return item containing item data, leftover
#     :rtype Item, bytes
#     """
#     return Item(data)


def extract_float(data: bytes) -> (float, Union[bytes, None]):
    """
    Extracts float from bytes.

    :param data: bytes from which extract float
    :return extracted float, leftover of data or None
    :rtype float, Union[bytes, None]
    """

    value: float = struct.unpack('>f', data[0:4:])[0]
    try:
        return value, data[4::]
    except IndexError:
        return value, None


def extract_double(data: bytes) -> (float, Union[bytes, None]):
    """
    Extracts double from bytes.

    :param data: bytes from which extract double
    :return extracted double, leftover of data or None
    :rtype float, Union[bytes, None]
    """

    value: float = struct.unpack('>d', data[0:8:])[0]
    try:
        return value, data[8::]
    except IndexError:
        return value, None


def extract_position(data: bytes) -> (Position, Union[bytes, None]):
    """
    Extracts Position(x, y, z) from data.

    Stolen from https://github.com/MaksymilianK/NSSV-bot.
    Thanks!

    :returns extracted position, leftover or None when no data left
    :rtype Position, Union[bytes, None]
    """
    # TODO: optimize.
    val = int.from_bytes(data[0:8], byteorder="big", signed=True)

    x = val >> 38
    y = ((val << 26) & 0xfff0000000000000) >> 52
    z = ((val << 38) & 0xffffffc000000000) >> 38

    if z >= 2 ** 25:
        z -= 2 ** 26

    position = Position((x, y, z))

    try:
        return position, data[8::]
    except IndexError:
        return position, None


