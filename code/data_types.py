import logging


def convert_int_to_int_bytes(value: int):
    val_size = value.bit_length() >> 3  # Change bits to bytes.
    val_bytes = value.to_bytes(val_size, byteorder="big", signed=False)
    return val_bytes


class VarInt:
    def __init__(self):
        pass

    """Sample usage:
    int_to_VarInt(2147483647) -> b'\xff\xff\xff\x7f' <class 'bytes'>"""

    @staticmethod
    def convert_int_to_VarInt(value: int, byteorder="big"):
        logging.debug(f"Converting int: '{value}' to VarInt.")

        value_bytes = convert_int_to_int_bytes(value)

        logging.debug(f"Bytes: {value_bytes}")

        VarInt_value = VarInt.convert_int_bytes_to_VarInt(value_bytes)

        if VarInt_value is None:
            logging.warning("Didn't found end of int")
            return None
        logging.debug(f"VarInt value: {VarInt_value}")
        return VarInt_value

    @staticmethod
    def convert_int_bytes_to_VarInt(int_bytes: bytes):
        result = 0
        num_read = 0
        for byte in int_bytes:
            value = byte & 0b01111111
            result |= (value << (7 * num_read))
            num_read += 1
            if num_read > 5:
                raise ValueError("VarInt is too big")
            if byte & 0b10000000 == 0:  # Last byte
                if result > 0x7ffffff:  # 2**31
                    return result - 0x10000000  # 2**32
                return result
        return None

    @staticmethod
    def convert_VarInt_to_int_bytes(value: int):
        if value < -0x80000000 or value > 0x7fffffff:
            raise ValueError("Invalid value, VarInt out of range")

        decimal_bytes = bytearray()

        if value < 0:
            value += 0x100000000  # 2**32
        while True:

            temp = value & 0b01111111
            value = value >> 7

            if value != 0:
                temp |= 0b10000000

            decimal_bytes.append(temp)
            if value == 0:
                return decimal_bytes


class VarLong:
    def __init__(self):
        pass

    @staticmethod
    def convert_long_to_VarLong(value: int, byteorder="big"):
        logging.debug(f"Converting int: '{value}' to VarLong.")

        value_bytes = convert_int_to_int_bytes(value)

        logging.debug(f"Bytes: {value_bytes}")

        VarLong_value = VarLong.convert_long_bytes_to_VarLong(value_bytes)

        if VarLong_value is None:
            logging.warning("Didn't found end of int")
            return None
        logging.debug(f"VarLong value: {VarLong_value}")
        return VarLong_value

    @staticmethod
    def convert_VarLong_to_int_bytes(value: int):
        if value < -0x8000000000000000 or value > 0x7fffffffffffffff:
            raise ValueError("Invalid value, VarInt out of range")

        decimal_bytes = bytearray()

        if value < 0:
            value += 0x10000000000000000  # 2**64
        while True:

            temp = value & 0b01111111
            value = value >> 7

            if value != 0:
                temp |= 0b10000000

            decimal_bytes.append(temp)
            if value == 0:
                return decimal_bytes

    @staticmethod
    def convert_long_bytes_to_VarLong(int_bytes: bytes):
        result = 0
        num_read = 0
        for byte in int_bytes:
            value = byte & 0b01111111
            result |= (value << (7 * num_read))

            num_read += 1
            if num_read > 10:
                raise ValueError("VarLong is too big")
            if byte & 0b10000000 == 0:
                if result > 0x7fffffffffffffff:  # 2**63
                    return result - 0x10000000000000000  # 2**64
                return result

        return None
