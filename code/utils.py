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


def unpack_varint(data: bytes):
    """Unpack first varint from data.
    Int can be made up to 4 bytes,
    If not found end of int raise ValueError
    :returns: value, end idx of var
    :rtype: int, int
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
    return number, i


def uncompress(data: memoryview):
    return zlib.decompress(bytes(data))


def unpack_str_from_data(data: memoryview):
    string_len, end_of_length_value = unpack_varint(bytes(data))

    string = bytes(data[end_of_length_value+1:string_len:])
    return string.decode("utf-8")
