from fractions import Fraction
from random import uniform, randint
from typing import Any

import pytest as pytest

from MinecraftConsoleClient.misc.consts import *
from MinecraftConsoleClient.misc.converters import *


def to_fraction(data):
    return Fraction.from_float(struct.unpack('f', struct.pack('f', data))[0])


class TestPacketReader:
    @staticmethod
    def _test(pack_method: callable,
              extract_method: callable,
              test_data: [Any, ],
              is_float: bool = False):
        prepared_test_data = [pack_method(value=test_value) for test_value in test_data]
        prepared_test_data_joined = b''.join(prepared_test_data)

        test_results = [extract_method(test_value)[0] for test_value in prepared_test_data]

        bytes_read = 0
        if not is_float:
            for test_data_, test_result in zip(test_data, test_results):
                assert test_data_ == test_result

                joined_data_result, bytes_read_ = extract_method(prepared_test_data_joined[bytes_read:])

                bytes_read += bytes_read_

                assert test_data_ == joined_data_result
        else:
            for test_data_, test_result in zip(test_data, test_results):
                assert to_fraction(test_data_) == to_fraction(test_result)

                joined_data_result, bytes_read_ = extract_method(prepared_test_data_joined[bytes_read:])

                bytes_read += bytes_read_

                assert to_fraction(test_data_) == to_fraction(joined_data_result)

    def test_bool(self):
        raw_test_data = (True, False, True, True, False, False)
        TestPacketReader._test(pack_method=pack_bool, extract_method=extract_bool, test_data=raw_test_data)

    def test_byte(self):
        raw_test_data = [i for i in range(MIN_BYTE, MAX_BYTE + 1)]
        TestPacketReader._test(pack_method=pack_byte, extract_method=extract_byte, test_data=raw_test_data)

    @pytest.mark.skip(reason="There is no method to pack unsigned_byte")
    def test_unsigned_byte(self):
        pass

    @pytest.mark.skip(reason="There is no method to pack short")
    def test_short(self):
        pass

    @pytest.mark.skip(reason="There is no method to pack int")
    def test_int(self):
        pass

    def test_long(self):
        raw_test_data = (*[i for i in range(MIN_LONG, MIN_LONG + 10000)],
                         *[i for i in range(MAX_LONG - 10000, MAX_LONG)],
                         *[randint(MIN_LONG, MAX_LONG) for i in range(10000)],
                         *(-1, 0, 1))

        TestPacketReader._test(pack_method=pack_long, extract_method=extract_long, test_data=raw_test_data)

    @pytest.mark.skip(reason="There is no method to pack unsigned_long")
    def test_unsigned_long(self):
        pass

    def test_float(self):
        raw_test_data = (*[uniform(MIN_FLOAT, MAX_FLOAT) for _ in range(100000)],
                         *(MIN_FLOAT, MIN_FLOAT + 1, 0., MAX_FLOAT - 1, MAX_FLOAT))

        TestPacketReader._test(pack_method=pack_float, extract_method=extract_float, test_data=raw_test_data,
                               is_float=True)

    def test_double(self):
        raw_test_data = (*[uniform(MIN_DOUBLE, MAX_DOUBLE) for _ in range(50000)],
                         *(MIN_DOUBLE, MIN_DOUBLE + 1, 0., MAX_DOUBLE - 1, MAX_DOUBLE))

        TestPacketReader._test(pack_method=pack_double, extract_method=extract_double, test_data=raw_test_data)

    @pytest.mark.skip(reason="There is no method to pack string_bytes")
    def test_string_bytes(self):
        pass

    @pytest.mark.skip(reason="There is no method to pack position")
    def test_position(self):
        pass

    @pytest.mark.skip(reason="There is no method to pack json_from_chat")
    def test_json_from_chat(self):
        pass

    @pytest.mark.skip(reason="There is no method to pack varint_as_int")
    def test_varint_as_int(self):
        pass

    @pytest.mark.skip(reason="There is no method to pack packet_id")
    def test_packet_id(self):
        pass
