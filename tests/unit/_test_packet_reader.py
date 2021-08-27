import struct
from fractions import Fraction
from random import uniform, randint
from unittest import TestCase

import pytest as pytest

from MinecraftConsoleClient.data_structures.packet_data_reader import PacketDataReader
from MinecraftConsoleClient.misc.consts import *
from MinecraftConsoleClient.misc.converters import pack_bool, pack_byte, pack_long, pack_float, pack_double


def to_fraction(data):
    return Fraction(struct.unpack('f', struct.pack('f', data))[0])


class TestPacketReader(TestCase):
    def test_bool(self):
        raw_test_data = (True, False, True, True, False, False)
        test_data = b''.join([pack_bool(value=val) for val in raw_test_data])
        data_reader = PacketDataReader(test_data)

        for test_val in raw_test_data:
            assert test_val == data_reader.extract_bool()

        assert len(data_reader._data) == data_reader._data_start_idx

    def test_byte(self):
        raw_test_data = [i for i in range(MIN_BYTE, MAX_BYTE + 1)]
        test_data = b''.join([pack_byte(val) for val in raw_test_data])
        data_reader = PacketDataReader(test_data)

        for test_val in raw_test_data:
            assert test_val == data_reader.extract_byte()

        assert len(data_reader._data) == data_reader._data_start_idx

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
        raw_test_data = (*[i for i in range(MIN_LONG, MIN_LONG + 200000)],
                         *[i for i in range(MAX_LONG - 200000, MAX_LONG)],
                         *[randint(MIN_LONG, MAX_LONG) for i in range(100000)],
                         *(-1, 0, 1))

        test_data = b''.join([pack_long(val) for val in raw_test_data])
        data_reader = PacketDataReader(test_data)

        for test_val in raw_test_data:
            assert test_val == data_reader.extract_long()

        assert len(data_reader._data) == data_reader._data_start_idx

    @pytest.mark.skip(reason="There is no method to pack unsigned_long")
    def test_unsigned_long(self):
        pass

    def test_float(self):
        raw_test_data = (*[uniform(MIN_FLOAT, MAX_FLOAT) for _ in range(100000)],
                         *(MIN_FLOAT, MIN_FLOAT + 1, 0., MAX_FLOAT - 1, MAX_FLOAT))

        test_data = b''.join([pack_float(val) for val in raw_test_data])
        data_reader = PacketDataReader(test_data)

        for test_val in raw_test_data:
            assert to_fraction(test_val) == to_fraction(data_reader.extract_float())

        assert len(data_reader._data) == data_reader._data_start_idx

    def test_double(self):
        raw_test_data = (*[uniform(MIN_DOUBLE, MAX_DOUBLE) for _ in range(50000)],
                         *(MIN_DOUBLE, MIN_DOUBLE + 1, 0., MAX_DOUBLE - 1, MAX_DOUBLE))

        test_data = b''.join([pack_double(val) for val in raw_test_data])
        data_reader = PacketDataReader(test_data)

        for idx, test_val in enumerate(raw_test_data):
            assert test_val == data_reader.extract_double()

        assert len(data_reader._data) == data_reader._data_start_idx

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
