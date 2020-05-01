import struct
import zlib


def convert_to_varint(value: int):
    """ Convert the var int.
    Stolen from
    https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0
    """
    varint = b''
    while True:
        byte = value & 0x7F
        value >>= 7
        varint += struct.pack('B', byte | (0x80 if value > 0 else 0))
        if value == 0:
            break
    return varint


def unpack_varint(data: bytes, start_idx=0) -> (int, int):
    """Unpack varint from data from start_idx index.
    Int can be made up to 4 bytes,
    If not found end of int raise ValueError
    :returns: value, end idx of var
    :rtype: int, int
    Algorithm stolen from
    https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0
    """
    if start_idx != 0:
        _data = data[start_idx::]
    else:
        _data = data

    number = 0

    for i in range(5):
        byte = _data[i]

        number |= (byte & 0x7F) << 7 * i

        if not byte & 0x80:
            break
    else:  # Not sure is range(5) valid, on error try range(6)
        raise ValueError("VarInt is too big!")
    return number, start_idx + i


def unpack_varint_new(data: memoryview, ) -> (int, memoryview):
    """ Unpack varint from data and return unpacked int, leftover
    Int can be made up to 4 bytes,
    If not found end of int raise ValueError
    :returns: value, leftover of data
    :rtype: int, memoryview
    Algorithm stolen from
    https://gist.github.com/MarshalX/40861e1d02cbbc6f23acd3eced9db1a0
    """
    number = 0

    for i in range(5):
        byte = data[i]

        number |= (byte & 0x7F) << 7 * i

        if not byte & 0x80:
            break
    else:  # Not sure is range(5) valid, on error try range(6)
        raise ValueError("VarInt is too big!")
    if len(data) > i + 2:
        return number, data[i + 1::]
    return number, None


def decompress(data: memoryview):
    print(bytes(data))
    return zlib.decompress(data)


def extract_data(data: memoryview, compression=False):
    """ Extract Packet ID and payload from packet data
    :returns: packet_id, payload
    :rtype: int, memoryview(payload)
    """
    if compression:
        data_length, data = unpack_varint_new(data)
        if data_length:
            data = decompress(data)
        packet_id, data = unpack_varint_new(data)
        return packet_id, data

    else:
        packet_id, data = unpack_varint_new(data)
        return packet_id, data


def extract_string_from_data(data: memoryview) -> (memoryview, memoryview):
    """
    Extract string from given data passed as memoryview.

    :param data: memoryview of decompressed array of bytes
    :return: memoryview of string(unicode(pure bytes)), memoryview of leftover
    :rtype: memoryview, memoryview
    """
    string_len, data = unpack_varint_new(data)

    string = data[:string_len:]
    data = data[string_len::]
    return string, data
