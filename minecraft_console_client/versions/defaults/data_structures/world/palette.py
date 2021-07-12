import math
from typing import Union
from misc.converters import extract_varint_as_int
from versions.defaults.consts import BLOCK


"""     PALETTE DIFFER FROM VERSION TO VERSION!    """


def decode_blocks(bits_per_block: int, data: bytes) -> (BLOCK,) * 4096:
    """Decodes block """
    if bits_per_block < 5:
        palette = IndirectPalette(4)
    elif bits_per_block < 9:
        palette = IndirectPalette(bits_per_block)
    else:
        palette = DirectPalette()


def extract_palette(bits_per_block: int, data: bytes) -> (Union['DirectPalette', 'IndirectPalette'], bytes):
    """Parse chunk section palette."""

    if bits_per_block < 9:
        if bits_per_block < 5:
            bits_per_block = 4
        palette = IndirectPalette(bits_per_block)
    else:
        palette = DirectPalette()

    leftover_data = palette.extract_palette_data(data)
    return palette, leftover_data


def calculate_bits_per_block(number_of_block_states: int):
    """
    Calculate amount of bits used to represent one enrty.

    :param number_of_block_states: total number of all possible block and their states.
    """
    return int(math.ceil(math.log(number_of_block_states, 2)))


class GlobalPalette:
    """
    Palette maps numeric IDs to block states.

    Global palette in 1.12.2:
    13 bits per entry: ((blockId << 4) | metadata)"""

    # Specific to 1.12.2
    bits_per_block: int = 13
    bits_for_id: int = 9
    bits_for_metadata: int = 4

    @staticmethod
    def parse_block_data(compacted_data_array: (int, )) -> [(int, int), ]:
        """
        Parse WHOLE array containing compacted data.

        compacted_data are by default justified to multiply of 8 bits
        :return ((id1, metadata), (id2, metadata), ...)
        """
        bits_per_block = GlobalPalette.bits_per_block
        bits_for_id = GlobalPalette.bits_for_id
        bits_for_metadata = GlobalPalette.bits_for_metadata

        id_mask: int = (1 << bits_for_id) - 1
        metadata_mask: int = (1 << bits_for_metadata) - 1

        decoded_blocks: [(int, int), ] = []

        # Amount of extractions before load next long.
        reads_before_load_next: int = 64 // bits_per_block  # 64(8 longs)

        # Amount of bits that will left after read
        # 'reads_before_load_next' number of data.
        bits_left: int = 64 - (reads_before_load_next * bits_per_block)

        number: int = 0
        for long in compacted_data_array:
            number <<= 8
            number |= long
            for _ in range(reads_before_load_next):
                metadata: int = number & metadata_mask
                number >>= bits_for_metadata

                block_id: int = number & id_mask
                number >>= bits_for_id

                decoded_blocks.append((block_id, metadata))
            n_of_bits: int = bits_left + 64  # Number of bits in number.
            reads_before_load_next = n_of_bits // bits_per_block
            bits_left = n_of_bits - (reads_before_load_next * bits_per_block)
        return decoded_blocks


class DirectPalette:
    """
    The number of bits used to represent a block are
    the base 2 logarithm of the number of block states, rounded up.
    For the V1.12.2 release, this is 13 bits per block.
    """
    @staticmethod
    def init(data: bytes) -> ("DirectPalette", bytes):
        # dummy_palette_length should always be 0. Only exists to mirror the format used elsewhere.
        _, data = extract_varint_as_int(data)
        return data


class IndirectPalette:
    """
    For bits per block <= 4, 4 bits are used to represent a block.
    For bits per block between 5 and 8, the given value is used.
    """
    bits_per_block: int
    bits_per_block: int = None
    palette: [bytes, ]

    def __init__(self, bits_per_block: int):
        self.bits_per_block = bits_per_block
        self.palette = []

    def extract_palette_data(self, data: bytes):
        palette_length, data = extract_varint_as_int(data)

        self.palette = [None] * palette_length
        for idx in range(palette_length):
            self.palette[idx], data = extract_varint_as_int(data)

        print(f"PALETTE: {[hex(i) for i in self.palette]}")
        return data
