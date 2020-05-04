import struct
import zlib
from consts import MAX_INT, MIN_INT,  MAX_UINT


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
    Unpack varint from uncompressed data and return unpacked int and leftover.
    VarInt can be made up to 5 bytes.
    If not found end of VarInt raise ValueError.

    Algorithm stolen from
    https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0

    :raise ValueError: when VarInt not fit into int32
    :param data: bytes of data containing VarInt
    :returns value, leftover of data
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

    if len(data) > i + 2:
        return number, data[i + 1::]
    return number, None


def decompress(data: memoryview) -> bytes:
    return zlib.decompress(data)


def extract_data(data: memoryview, compression=False) -> (int, memoryview):
    """
    Extract Packet ID and payload from packet data

    :returns packet_id, payload
    :rtype int, memoryview(payload)
    """

    if compression:
        data_length, data = unpack_varint(data)
        if data_length:
            data = decompress(data)
        packet_id, data = unpack_varint(data)
        return packet_id, data

    else:
        packet_id, data = unpack_varint(data)
        return packet_id, data


def extract_string_from_data(data: memoryview) -> (memoryview, memoryview):
    """
    Extract string from given data passed as memoryview.

    :param data: memoryview of decompressed array of bytes
    :return memoryview of string(unicode(pure bytes)), memoryview of leftover
    :rtype memoryview, memoryview
    """

    string_len, data = unpack_varint(data)

    string = data[:string_len:]
    data = data[string_len::]
    return string, data


def pack_data(data):
    """
    Page the data.
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


