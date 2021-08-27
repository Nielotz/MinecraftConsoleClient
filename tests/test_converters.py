import random
import string
import time
from fractions import Fraction
from random import randint, uniform
from unittest import TestCase

from MinecraftConsoleClient.misc.consts import *
from MinecraftConsoleClient.misc.converters import *


def to_fraction(data):
    return Fraction(struct.unpack('f', struct.pack('f', data))[0])


class Test(TestCase):
    def _test(self, converter,
              deconverter,
              dataset=(),
              test_desc: str = "",
              is_float: bool = False, is_double: bool = False,
              is_string: bool = False):
        # Config
        n_of_repeats = 10  # How many times test to get best time.

        time_ns = time.perf_counter_ns
        times = {"pack": [], "extract": []}
        for data in dataset:
            with self.subTest(test_desc):
                pack_time, unpack_time = 100000000, 1000000000
                for _ in range(n_of_repeats):
                    start = time_ns()
                    converted = converter(data)
                    if (_pack_time := (time_ns() - start)) < pack_time:
                        pack_time = _pack_time

                    start = time_ns()
                    deconverted, _ = deconverter(converted)
                    if (_unpack_time := (time_ns() - start)) < unpack_time:
                        unpack_time = _unpack_time

                    if is_float:
                        self.assertEqual(
                            to_fraction(data),
                            to_fraction(deconverted))
                    elif is_double:
                        self.assertEqual(data, deconverted)
                    elif is_string:
                        self.assertEqual(data.encode("utf-8"), deconverted)
                    else:
                        self.assertEqual(data, deconverted)
                times["pack"].append(pack_time)
                times["extract"].append(unpack_time)

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
        n_of_strings: int = 1000
        n_of_letters: int = 100
        n_of_numbers: int = 1000

        # bool
        edge = [True, False]
        self._test(pack_bool, extract_bool, edge, "Converters - bool")

        # byte
        numbers = [randint(MIN_BYTE, MAX_BYTE) for _ in range(n_of_numbers)]
        edge = [MIN_BYTE, MIN_BYTE + 1, 0, MAX_BYTE - 1, MAX_BYTE]
        self._test(pack_byte, extract_byte, numbers + edge, "Converters - byte")

        # unsigned byte

        # unsigned short

        # int

        # long
        numbers = [randint(MIN_LONG, MAX_LONG) for _ in range(n_of_numbers)]
        edge += [MAX_LONG, MAX_LONG - 1, MIN_LONG, MIN_LONG + 1]
        self._test(pack_long, extract_long, numbers + edge,
                   "Converters - long")

        # float
        numbers = [uniform(MIN_FLOAT, MAX_FLOAT) for _ in range(n_of_numbers)]
        edge = [MIN_FLOAT, MIN_FLOAT + 1, MAX_FLOAT - 1, MAX_FLOAT]
        self._test(pack_float, extract_float, numbers + edge,
                   "Converters - float", is_float=True)

        # double
        numbers = [uniform(MIN_DOUBLE, MAX_DOUBLE) for _ in range(n_of_numbers)]
        edge += [MIN_DOUBLE, MIN_DOUBLE + 1, MAX_DOUBLE - 1, MAX_DOUBLE]
        self._test(pack_double, extract_double, numbers + edge,
                   "Converters - double", is_double=True)

        # varint
        numbers = [randint(MIN_INT, MAX_INT) for _ in range(n_of_numbers)]
        edge = [0, 1, 254, 255, 265,
                -1, -254, -255, -265,
                2 ** 16 - 1, 2 ** 16, 2 ** 16 + 1,
                -2 ** 16 + 1, -2 ** 16, -2 ** 16 - 1,
                MAX_INT - 1, MAX_INT, MIN_INT + 1, MIN_INT,
                ]
        self._test(convert_to_varint, extract_varint_as_int, numbers + edge,
                   "Converters - varint")

        # string
        letters = string.printable
        strings = [''.join(random.choice(letters) for _ in range(n_of_letters))
                   for _ in range(n_of_strings)]
        edge = []
        self._test(pack_string, extract_string, strings + edge,
                   "Converters - string", is_string=True)
        # extract position

        # extract json from chat

        # extract packet data
