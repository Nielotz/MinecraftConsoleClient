from unittest import TestCase
from utils import convert_to_varint, unpack_varint
from random import randint
import time


class Test(TestCase):

    def test_converting(self):
        MAX_INT = 2**31 - 1
        MIN_INT = -2**31
        total_time = 0
        n_of_numbers = 10000
        for i in range(n_of_numbers):
            rand = randint(MIN_INT, MAX_INT)
            with self.subTest(i=i):
                start = time.time_ns()
                v1 = convert_to_varint(rand)
                v2, _ = unpack_varint(v1)
                self.assertEqual(rand, v2)
                total_time += time.time_ns() - start

        print(f"Total time: {total_time}ns, per test: {total_time // n_of_numbers}")