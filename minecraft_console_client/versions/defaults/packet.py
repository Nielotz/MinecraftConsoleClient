from collections import namedtuple
from enum import Enum

PacketIDNamedTuple = namedtuple("PacketIDNamedTuple", "int bytes")


class Packet:
    """ Translates packet name to packet_id (int varint)"""

    class Login(Enum):
        pass

    class Status(Enum):
        pass

    class Play(Enum):
        pass
