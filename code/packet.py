import data_types


class Packet:
    packet_id_VarInt = None
    data = None
    length = None  # Length of Packet ID + Data

    def __init__(self, packet_id: int, data):
        pass


    def get_uncompressed_packet(self):
        return

