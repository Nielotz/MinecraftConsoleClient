import struct
import zlib


def convert_to_varint(value: int) -> bytes:
    """
    Convert int to VarInt.

    Stolen from
    https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0

    :returns VarInt
    :rtype bytes
    """
    varint = b''
    while value != 0:
        byte = value & 0x7F
        value >>= 7
        varint += struct.pack('B', byte | (0x80 if value > 0 else 0))
    return varint


def unpack_varint(data: memoryview) -> (int, memoryview):
    """
    Unpack varint from uncompressed data and return unpacked int and leftover.
    VarInt can be made up to 5 bytes.
    If not found end of VarInt raise ValueError.

    Algorithm stolen from
    https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0

    :param data: memoryview of data containing VarInt
    :returns value, leftover of data
    :rtype int, memoryview
    """

    number = 0

    for i in range(5):
        byte = data[i]

        number |= (byte & 0x7F) << 7 * i

        if not byte & 0x80:
            break
    else:
        raise ValueError("VarInt is too big!")
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