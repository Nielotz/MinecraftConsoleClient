from collections import namedtuple
from enum import Enum
VersionNamedTuple = namedtuple("VersionNamedTuple", "release_name "
                                                    "version_number "
                                                    "version_number_bytes")

VERSION = {
    "1.15.2": VersionNamedTuple("1.15.2", 578, b'\xc2\x04'),
    "1.15.1": VersionNamedTuple("1.15.1", 575, b'\xbf\x04'),
    "1.15": VersionNamedTuple("1.15", 573, b'\xbd\x04'),
    "1.14.4": VersionNamedTuple("1.14.4", 498, b'\xf2\x03'),
    "1.14.3": VersionNamedTuple("1.14.3", 490, b'\xea\x03'),
    "1.14.2": VersionNamedTuple("1.14.2", 485, b'\xe5\x03'),
    "1.14.1": VersionNamedTuple("1.14.1", 480, b'\xe0\x03'),
    "1.14": VersionNamedTuple("1.14", 477, b'\xdd\x03'),
    "1.13.2": VersionNamedTuple("1.13.2", 404, b'\x94\x03'),
    "1.13.1": VersionNamedTuple("1.13.1", 401, b'\x91\x03'),
    "1.13": VersionNamedTuple("1.13", 393, b'\x89\x03'),
    "1.12.2": VersionNamedTuple("1.12.2", 340, b'\xd4\x02'),
    "1.12.1": VersionNamedTuple("1.12.1", 338, b'\xd2\x02'),
    "1.12": VersionNamedTuple("1.12", 335, b'\xcf\x02'),
    "1.11.2": VersionNamedTuple("1.11.2", 316, b'\xbc\x02'),
    "1.11.1": VersionNamedTuple("1.11.1", 316, b'\xbc\x02'),
    "1.11": VersionNamedTuple("1.11", 315, b'\xbb\x02'),
    "1.10.2": VersionNamedTuple("1.10.2", 210, b'\xd2\x01'),
    "1.10.1": VersionNamedTuple("1.10.1", 210, b'\xd2\x01'),
    "1.10": VersionNamedTuple("1.10", 210, b'\xd2\x01'),
    "1.9.4": VersionNamedTuple("1.9.4", 110, b'n'),
    "1.9.3": VersionNamedTuple("1.9.3", 110, b'n'),
    "1.9.2": VersionNamedTuple("1.9.2", 109, b'm'),
    "1.9.1": VersionNamedTuple("1.9.1", 108, b'l'),
    "1.9": VersionNamedTuple("1.9", 107, b'k'),
    "1.8.9": VersionNamedTuple("1.8.9", 47, b'/'),
    "1.8.8": VersionNamedTuple("1.8.8", 47, b'/'),
    "1.8.7": VersionNamedTuple("1.8.7", 47, b'/'),
    "1.8.6": VersionNamedTuple("1.8.6", 47, b'/'),
    "1.8.5": VersionNamedTuple("1.8.5", 47, b'/'),
    "1.8.4": VersionNamedTuple("1.8.4", 47, b'/'),
    "1.8.3": VersionNamedTuple("1.8.3", 47, b'/'),
    "1.8.2": VersionNamedTuple("1.8.2", 47, b'/'),
    "1.8.1": VersionNamedTuple("1.8.1", 47, b'/'),
    "1.8": VersionNamedTuple("1.8", 47, b'/'),
    "1.7.10": VersionNamedTuple("1.7.10", 5, b'\x05'),
    "1.7.9": VersionNamedTuple("1.7.9", 5, b'\x05'),
    "1.7.8": VersionNamedTuple("1.7.8", 5, b'\x05'),
    "1.7.7": VersionNamedTuple("1.7.7", 5, b'\x05'),
    "1.7.6": VersionNamedTuple("1.7.6", 5, b'\x05'),
    "1.7.5": VersionNamedTuple("1.7.5", 4, b'\x04'),
    "1.7.4": VersionNamedTuple("1.7.4", 4, b'\x04'),
}


class Version(Enum):
    V1_15_2 = VERSION["1.15.2"]
    V1_15_1 = VERSION["1.15.1"]
    V1_15 = VERSION["1.15"]
    V1_14_4 = VERSION["1.14.4"]
    V1_14_3 = VERSION["1.14.3"]
    V1_14_2 = VERSION["1.14.2"]
    V1_14_1 = VERSION["1.14.1"]
    V1_14 = VERSION["1.14"]
    V1_13_2 = VERSION["1.13.2"]
    V1_13_1 = VERSION["1.13.1"]
    V1_13 = VERSION["1.13"]
    V1_12_2 = VERSION["1.12.2"]
    V1_12_1 = VERSION["1.12.1"]
    V1_12 = VERSION["1.12"]
    V1_11_2 = VERSION["1.11.2"]
    V1_11_1 = VERSION["1.11.1"]
    V1_11 = VERSION["1.11"]
    V1_10_2 = VERSION["1.10.2"]
    V1_10_1 = VERSION["1.10.1"]
    V1_10 = VERSION["1.10"]
    V1_9_4 = VERSION["1.9.4"]
    V1_9_3 = VERSION["1.9.3"]
    V1_9_2 = VERSION["1.9.2"]
    V1_9_1 = VERSION["1.9.1"]
    V1_9 = VERSION["1.9"]
    V1_8_9 = VERSION["1.8.9"]
    V1_8_8 = VERSION["1.8.8"]
    V1_8_7 = VERSION["1.8.7"]
    V1_8_6 = VERSION["1.8.6"]
    V1_8_5 = VERSION["1.8.5"]
    V1_8_4 = VERSION["1.8.4"]
    V1_8_3 = VERSION["1.8.3"]
    V1_8_2 = VERSION["1.8.2"]
    V1_8_1 = VERSION["1.8.1"]
    V1_8 = VERSION["1.8"]
    V1_7_10 = VERSION["1.7.10"]
    V1_7_9 = VERSION["1.7.9"]
    V1_7_8 = VERSION["1.7.8"]
    V1_7_7 = VERSION["1.7.7"]
    V1_7_6 = VERSION["1.7.6"]
    V1_7_5 = VERSION["1.7.5"]
    V1_7_4 = VERSION["1.7.4"]