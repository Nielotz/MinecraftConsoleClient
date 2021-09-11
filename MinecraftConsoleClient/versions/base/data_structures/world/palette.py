from typing import Union

from misc.converters import extract_varint_as_int

"""     PALETTE DIFFER FROM VERSION TO VERSION!    """


class PaletteBase:
    def load(self, data: memoryview):
        raise NotImplementedError

    def parse_block_data(self, compacted_data_array: (int,)):
        raise NotImplementedError


def extract_palette(bits_per_block: int,
                    data: memoryview) -> (Union["DirectPalette", "IndirectPalette"], bytes):
    """Parse chunk section palette."""

    if bits_per_block < 9:
        if bits_per_block < 5:
            bits_per_block = 4
        palette = IndirectPalette(bits_per_block)
    else:
        palette = DirectPalette()

    leftover_data = palette.load(data)
    return palette, leftover_data


# TODO: Optimize A.F.F.
def extract_blocks_from_compacted_data_array(longs: (int,), bits_per_block: int) -> (int,) * 4096:
    extracted_indices: [int, ] = [-1, ] * 4096
    extracted_indices_idx: int = 0
    long_data_holder: int = 0
    long_data_holder_n_of_bits: int = 0
    mask: int = (1 << bits_per_block) - 1
    for long in longs:
        long_data_holder = (long << long_data_holder_n_of_bits) | long_data_holder
        long_data_holder_n_of_bits += 64
        while long_data_holder_n_of_bits >= bits_per_block:
            extracted_indices[extracted_indices_idx] = long_data_holder & mask
            long_data_holder >>= bits_per_block
            long_data_holder_n_of_bits -= bits_per_block
            extracted_indices_idx += 1
    return extracted_indices


class GlobalPalette:
    """
    Palette maps numeric IDs to block states.

    Global palette in 1.12.2:
    13 bits per entry: ((blockId << 4) | metadata)
    """
    bits_per_block: int = 13
    bits_for_id: int = 9
    bits_for_metadata: int = 4

    def parse_block_data(self, array_of_longs: (int,)) -> ((int, int),):
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
        for long in array_of_longs:
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


class DirectPalette(PaletteBase):
    """
    The number of bits used to represent a block are
    the base 2 logarithm of the number of block states, rounded up.
    For the V1.12.2 release, this is 13 bits per block.
    """

    def load(self, data: memoryview) -> bytes:
        # dummy_palette_length should always be 0. Only exists to mirror the format used elsewhere.
        _, data = extract_varint_as_int(data)
        return data

    def parse_block_data(self, array_of_longs: (int,)) -> (int,) * 4096:
        indices = extract_blocks_from_compacted_data_array(array_of_longs, 13)
        return indices


class IndirectPalette(PaletteBase):
    """
    For bits per block <= 4, 4 bits are used to represent a block.
    For bits per block between 5 and 8, the given value is used.
    """

    def __init__(self, bits_per_block: int):
        self.bits_per_block = bits_per_block
        self.palette = [bytes, ]

    def load(self, data: memoryview):
        palette_length, data = extract_varint_as_int(data)

        self.palette = [None] * palette_length
        for idx in range(palette_length):
            self.palette[idx], data = extract_varint_as_int(data)

        return data

    # TODO: Optimize A.F.F.
    def parse_block_data(self, array_of_longs: (int,)) -> (int,) * 4096:
        """
        Parse WHOLE array containing compacted data.

        compacted_data are by default justified to multiply of 8 bits
        :return ((id1, metadata), (id2, metadata), ...)
        """
        return extract_blocks_from_compacted_data_array(array_of_longs, self.bits_per_block)
