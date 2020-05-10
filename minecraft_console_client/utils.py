import struct
import zlib
import json
import struct


from consts import MAX_INT, MIN_INT, MAX_UINT


class Item:
    present = False
    item_id = None
    item_count = None
    NBT = None

    def __init__(self, data: bytes = None):
        if data is not None:
            present = (data[0] & 0x01) and True
            if present:
                self.item_id, data = unpack_varint(data[1::])
                self.item_count, data = extract_byte(data)
                x, data = extract_byte(data)
                if x != 0:
                    print(x, data)
                    print()







def __convert_to_vartype(value: int, vartype_length: int):
    """
        Converts value into variable length variable.
        Target varint bytes length specifies vartype_length.
        vartype_length has to be at least byte_size(value) + 1

        This is minecraft protocol's implementation of VarInt, VarLong.
        For positive number, VarType behave normally:
          Two's complement (U2), little-endian, with deleted unnecessary bytes!

        ! For negative number VarType always fit into specified length, e.g:    !
        !   VarInt = 5 bytes, VarLong = 10 bytes, VarType = vartype_length bytes!
        ! Sample:
        !   0 => b'\x00'    128 => b'\x80\x01'   255 => b'\xff\x01'
        !   VarInt(-1) == VarType(-1, 5) => b'\xff\xff\xff\xff\x0f'
        !   VarLong(-1) == VarType(-1, 10) => TODO:
        !   VarType(-1, 3) => b'\xff\xff\x03'
        !   VarType(-2, 3) => b'\xfe\xff\x03'

        :returns VarInt in hex bytes
        :rtype bytes
    """
    raise RuntimeError("Function not ready yet!")
    if value == 0:
        return b'\x00'
    # TODO: check speed (struct.pack vs varint[0]), then make this func


def convert_to_varint(value: int) -> bytes:
    """
    Converts int to VarInt.
    If value not fit into int32 - raises ValueError

    :raises ValueError when value not fit in int32
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
        return varint

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
    :rtype int, bytes
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

    :returns packet_id, payload
    :rtype int, bytes
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


def pack_data(data):
    """
    Pages the data.
    Stolen from
    https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0
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


def extract_string_from_data(data: bytes) -> (bytes, bytes):
    """
    Extracts string from given bytes.

    :param data: decompressed array of bytes
    :return bytes of string(unicode(pure bytes)), bytes of leftover
    :rtype bytes, bytes
    """

    string_len, data = unpack_varint(data)

    string = data[:string_len:]
    try:
        data = data[string_len::]
    except IndexError:
        data = None
    return string, data


def extract_json_from_chat(data: bytes) -> dict:
    string, leftover = extract_string_from_data(data)

    return json.loads(string)


def extract_int(data: bytes) -> (int, bytes):
    """
    Extracts int from bytes.

    :param data: bytes from which extract int
    :return extracted int, leftover
    :rtype int, bytes
    """
    value = int.from_bytes(data[0:4:], byteorder="big", signed=True)
    try:
        return value, data[4::]
    except IndexError:
        return value, None


def extract_unsigned_byte(data: bytes) -> (int, bytes):
    """
    Extracts unsigned byte from bytes.

    :param data: bytes from which extract int
    :return extracted unsigned byte, leftover
    :rtype int, bytes
    """
    value = int.from_bytes(data[0:1:], byteorder="big", signed=True)
    assert data[0] == value
    try:
        return value, data[1::]
    except IndexError:
        return value, None


def extract_boolean(data: bytes) -> (bool, bytes):
    """
    Extracts boolean from bytes.

    :param data: bytes from which extract
    :return True or False, leftover
    :rtype bool, bytes
    """
    try:
        return data[0], data[1::]
    except IndexError:
        return data[0] and True, None


def extract_byte(data: bytes) -> (int, bytes):
    """
    Extracts byte from bytes.

    :param data: bytes from which extract
    :return byte, leftover
    :rtype byte, bytes
    """
    value = int.from_bytes(data[0:1:], byteorder="big", signed=True)
    try:
        return value, data[1::]
    except IndexError:
        return value, None


def extract_slot(data: bytes) -> (Item, bytes):
    """
    Extracts slot item from given bytes.
    Slot:
        Boolean  True if there is an item in this position; false if it is empty.
        VarInt    The item ID. Omitted if present is false
        Item Count Optional Byte
        NBT        If 0, there is no NBT data, and no further data follows.

    :param data: bytes from which extract int

    :return item containing item data, leftover
    :rtype Item, bytes
    """
    return Item(data)


def extract_float(data: bytes) -> (float, bytes):
    value: float = struct.unpack('>f', data[0:4:])[0]
    try:
        return value, data[4::]
    except IndexError:
        return value, None


def extract_double(data: bytes) -> (float, bytes):
    value: float = struct.unpack('>d', data[0:8:])[0]
    try:
        return value, data[8::]
    except IndexError:
        return value, None


