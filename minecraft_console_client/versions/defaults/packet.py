from collections import namedtuple

PacketIDNamedTuple = namedtuple("PacketIDNamedTuple", "int bytes")


class Packet:
    """ Translates packet name to packet_id varint"""

    class Login:
        pass

    class Status:
        pass

    class Play:
        pass
