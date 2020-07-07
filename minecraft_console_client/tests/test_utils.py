import time
from random import randint
from unittest import TestCase

from misc.utils import convert_to_varint, extract_varint
from misc.consts import MAX_INT
from misc.consts import MIN_INT


class Test(TestCase):

    def test_convert_extract_varint(self):
        times = []
        n_of_numbers = 100000
        for i in range(n_of_numbers):
            rand = randint(MIN_INT, MAX_INT)
            with self.subTest(i=i):
                start = time.perf_counter_ns()
                v1 = convert_to_varint(rand)
                v2, _ = extract_varint(v1)
                self.assertEqual(rand, v2)
                times.append(time.perf_counter_ns() - start)
        total_time = sum(times)
        print(f"Total time: {total_time}ns, "
              f"average per test: {total_time // n_of_numbers}ns,"
              f"best: {min(times)}ns")
