import zlib

from misc.converters import TypeToExtractFunction
from misc.exceptions import InvalidUncompressedPacketError


class PacketDataReader:
    """ Packet data reader.

    is_compression_enabled: bool
    data: memoryview - raw [uncompressed] packet data received from server
    """
    def __init__(self):
        self._compression_threshold: int = -1
        self._is_compression_enabled: bool = False
        self.data: memoryview = memoryview(b"-1")

    def set_compression_threshold(self, compression_threshold: int):
        self._compression_threshold = compression_threshold
        self._is_compression_enabled = not (compression_threshold < 0)

    def load(self, packet_data: memoryview):
        """ Load raw data to reader. """

        self.data = packet_data
        if self._is_compression_enabled:
            self._decompress()

    def get_not_parsed_data(self) -> memoryview:
        return self.data

    def _decompress(self):
        data_length = self.extract(TypeToExtractFunction.VARINT_AS_INT)
        if data_length == 0:
            return  # Compression disabled for packet

        self._data = self.data = memoryview(zlib.decompress(bytes(self.data)))

        if data_length != len(self.data) or data_length <= self._compression_threshold:
            raise InvalidUncompressedPacketError(
                "data_length != len(self.data) or data_length < self._compression_threshold")


    def extract(self, type_to_extract: TypeToExtractFunction.BOOL):
        value, self.data = type_to_extract(self.data)
        return value

    def extract_packet_id(self) -> int:
        return self.extract(TypeToExtractFunction.VARINT_AS_INT)

