from typing import Union

from misc import converters
from versions.defaults.data_structures.world.palette import IndirectPalette, DirectPalette, extract_palette


class ChunkSection:
    """
    Chunk section data container and parser.

    Use parse to create."""

    def __init__(self, palette: Union[IndirectPalette, DirectPalette]):
        self.palette: Union[IndirectPalette, DirectPalette] = palette
        self.blocks: [(int, int), ] = []  # [(id, metadata),]

    @classmethod
    def parse_data(cls, data: bytes) -> ("ChunkSection", bytes):
        """
        Parse chunk section (16x16x16).

        :param data: bytes of chunk section (from chunk packet)
        :return ChunkSection object, data leftover
        """

        # Determines how many bits are used to encode a block.
        bits_per_block, data = converters.extract_unsigned_byte(data)

        palette, data = extract_palette(bits_per_block, data)

        chunk_section = cls(palette)

        """Parse:
            Data Array Length
            Data Array
            Block Light
            Sky Light
        """
        data = chunk_section._parse_block_data(bits_per_block, data)

        return chunk_section, data

    def _parse_block_data(self, bits_per_block: int, data: bytes) -> bytes:
        """
        Parse: Data Array Length, Data Array, Block Light, Sky Light

        Docs: https://wiki.vg/index.php?title=Chunk_Format&oldid=14135#Chunk_Section_structure

        To use this, self.palette needs to be set correctly (by palette._parse_palette).
        """
        # 4096 indices are coded into data_array_length made of longs.
        # Number of longs in the following array.
        data_array_length, data = converters.extract_varint_as_int(data)

        """Extract longs from packet."""
        # Compacted list of 4096 indices pointing to state IDs in the Palette
        array_of_longs = [-1, ] * data_array_length
        extract_long = converters.extract_long
        for idx in range(data_array_length):
            # TODO: Optimize (maybe create: extract_longs(n_of_longs, data)?)
            array_of_longs[idx], data = extract_long(data)

        # The number of longs needed for the data array can be calculated as
        # (blocks     * bits_per_block) / bits per long, which equals:
        # ((16×16×16) * bits_per_block) / 64
        # so bits_per_block = number_of_longs / 64
        bits_per_block = len(array_of_longs) // 64

        # TODO:
        self.blocks = self.palette.parse_block_data(array_of_longs=array_of_longs)
        return data

    def _read_bits_of_data(self, number_of_bits: int):
        pass
