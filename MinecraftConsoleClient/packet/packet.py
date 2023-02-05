class PacketType:
    SetCompression = 1

class PacketData:
    def __init__(self, data: memoryview, packet_type: PacketType):
        self.data: memoryview = data
        self.packet_type: PacketType = packet_type