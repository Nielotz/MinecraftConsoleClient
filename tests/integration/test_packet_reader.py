import random
import struct
from fractions import Fraction
from random import randint, uniform

from MinecraftConsoleClient.data_structures.packet_data_reader import PacketDataReader, TypeToExtract
from MinecraftConsoleClient.misc.consts import *
from MinecraftConsoleClient.misc.converters import pack_bool, pack_long, pack_byte, pack_float, pack_double


def to_fraction(data):
    return Fraction(struct.unpack('f', struct.pack('f', data))[0])


class TestPacketReader:
    def test(self):
        bool_ = TypeToExtract.BOOL
        byte_ = TypeToExtract.BYTE
        long_ = TypeToExtract.LONG
        float_ = TypeToExtract.FLOAT
        double_ = TypeToExtract.DOUBLE

        raw_test_data_with_type = [
            *[(i, pack_bool(i), bool_) for i in (True, False, True, True, False, False)],

            *[(i, pack_byte(i), byte_) for i in range(MIN_BYTE, MAX_BYTE + 1)],

            *[(i, pack_long(i), long_) for i in range(MIN_LONG, MIN_LONG + 500)],
            *[(i, pack_long(i), long_) for i in range(MAX_LONG - 500, MAX_LONG)],
            *[((val := randint(MIN_LONG, MAX_LONG)), pack_long(val), long_) for _ in range(5000)],
            *[(i, pack_long(i), long_) for i in (-1, 0, 1)],

            *[((val := uniform(MIN_FLOAT, MAX_FLOAT)), pack_float(val), float_) for _ in range(5000)],
            *[(i, pack_float(i), float_) for i in (MIN_FLOAT, MIN_FLOAT + 1, 0., MAX_FLOAT - 1, MAX_FLOAT)],

            *[((val := uniform(MIN_DOUBLE, MAX_DOUBLE)), pack_double(val), double_) for _ in range(5000)],
            *[(i, pack_double(i), double_) for i in (MIN_DOUBLE, MIN_DOUBLE + 1, 0., MAX_DOUBLE - 1, MAX_DOUBLE)]
        ]

        random.shuffle(raw_test_data_with_type)

        test_data = b''.join([val[1] for val in raw_test_data_with_type])
        data_reader = PacketDataReader(test_data)
        data_reader_extract = data_reader.extract

        for test_val, _packed_val, extract_method in raw_test_data_with_type:
            if extract_method is float_:
                assert to_fraction(test_val) == to_fraction(data_reader_extract(extract_method))
            else:
                assert test_val == data_reader_extract(extract_method)
        assert len(data_reader._data) == data_reader._data_start_idx
