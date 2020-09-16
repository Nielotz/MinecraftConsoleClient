import time
from random import randint, uniform
from unittest import TestCase

from misc.consts import *
from misc.converters import *

from fractions import Fraction


class Test(TestCase):

    def _test(self, to_varint_converter, from_varint_converter,
              dataset=(), test_desc: str = "", is_float: bool = False,
              is_double: bool = False):
        # Config
        times = {"pack": [], "extract": []}
        for data in dataset:
            with self.subTest(test_desc):
                start = time.perf_counter_ns()
                varint = to_varint_converter(data)
                times["pack"].append(time.perf_counter_ns() - start)

                start = time.perf_counter_ns()
                decoded_varint, _ = from_varint_converter(varint)
                times["extract"].append(time.perf_counter_ns() - start)

                if is_float:
                    data = Fraction(struct.unpack('f', struct.pack('f', data))[0])
                    decoded_varint = Fraction(struct.unpack('f', struct.pack('f', decoded_varint))[0])
                    self.assertEqual(data, decoded_varint)
                elif is_double:
                    self.assertEqual(data, decoded_varint)
                else:
                    self.assertEqual(data, decoded_varint)
        total_pack_time = sum(times["pack"])
        total_extract_time = sum(times["extract"])
        print(f"""TEST: {test_desc}
    PACK:,
        Total time: {total_pack_time}ns, 
        average per test: {total_pack_time // len(dataset)}ns, best: {min(times["pack"])}ns
    EXTRACT:
        total extract time: {total_extract_time}ns, 
        average per test: {total_extract_time // len(dataset)}ns, best: {min(times["extract"])}ns
""")

    def test_converters(self):
        # Config.
        n_of_numbers: int = 10000
        numbers: [int, ] = [0] * n_of_numbers
        # Integers.
        for i in range(n_of_numbers):
            numbers[i] = randint(MIN_INT, MAX_INT)
        edge = [0, 1, 254, 255, 265, 2**16-1, 2**16, 2**16+1,
                -1, -254, -255, -265, -2**16+1, -2**16, -2**16-1,
                MAX_INT-1, MAX_INT, MIN_INT + 1, MIN_INT,
                ]
        self._test(convert_to_varint, extract_varint_as_int, numbers + edge,
                   "Converters - varint")
        # self._test(_, extract_int, numbers,
        #                    "Converters - varint")

        for i in range(n_of_numbers // 2, n_of_numbers, 2):
            numbers[i] = randint(MAX_INT, MAX_LONG)
            numbers[i + 1] = randint(MIN_LONG, MIN_INT)
        edge += [MAX_LONG, MAX_LONG - 1, MIN_LONG, MIN_LONG + 1]
        self._test(pack_long, extract_long, numbers+edge, "Converters - long")

        for i in range(n_of_numbers):
            numbers[i] = randint(MIN_BYTE, MAX_BYTE)
        edge = [MIN_BYTE, MIN_BYTE + 1, 0, MAX_BYTE - 1, MAX_BYTE]
        self._test(pack_byte, extract_byte, numbers+edge, "Converters - byte")
        # self._test(_, extract_unsigned_byte, numbers,
        #            "Converters - byte")
        # self._test(pack_unsigned_short, _, numbers,
        #            "Converters - byte")

        # Adjust strings based on real data.
        # for i in range(n_of_numbers):
        #     numbers[i] = randint(MIN_BYTE, MAX_BYTE)
        # self._test(pack_string, extract_string, numbers, "Converters - byte")

        # Float-points.
        numbers = [0.] * n_of_numbers
        mx = MAX_BYTE - 1  # Right limit for uniform.
        for i in range(n_of_numbers):
            numbers[i] = uniform(MIN_BYTE, mx)
        edge = [MIN_FLOAT, MIN_FLOAT+1, MAX_FLOAT-1, MAX_FLOAT]
        self._test(pack_float, extract_float, numbers+edge,
                   "Converters - float", is_float=True)

        mx = MAX_BYTE - 1  # Right limit for uniform.
        for i in range(n_of_numbers):
            numbers[i] = uniform(MIN_BYTE, mx)
        edge += [MIN_DOUBLE, MIN_DOUBLE+1, MAX_DOUBLE-1, MAX_DOUBLE]
        self._test(pack_double, extract_double, numbers+edge,
                   "Converters - double", is_double=True)

        # Exclusives.
        edge = [True, False]
        self._test(pack_bool, extract_boolean, edge, "Converters - bool")

        # extract_data()
        # extract_json_from_chat()
        # extract_position()
