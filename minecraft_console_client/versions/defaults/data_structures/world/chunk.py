import math

from typing import Union
from misc import converters
from versions.defaults.data_structures.world.palette import extract_palette
from versions.defaults.data_structures.world.palette import IndirectPalette
from versions.defaults.data_structures.world.palette import DirectPalette
from versions.defaults.data_structures.world.palette import GlobalPalette


class ChunkSection:
    """Chunk section data container and parser."""

    def __init__(self):
        self.blocks: [(int, int), ] = []  # [(id, metadata),]
        self.palette: Union[IndirectPalette, DirectPalette]

    @staticmethod
    def parse(data: bytes) -> Union["ChunkSection()", bytes]:
        """
        Parse chunk section (16x16x16).

        :param data: bytes of chunk section (from chunk packet)
        :return ChunkSection object, data leftover
        """
        chunk_section = ChunkSection()

        # Determines how many bits are used to encode a block.
        bits_per_block, data = converters.extract_unsigned_byte(data)

        data = chunk_section._parse_palette(bits_per_block, data)

        chunk_section._parse_block_data(bits_per_block, data)
        # print(f"data_array_length: {data_array_length} {data}")

        return chunk_section, data

    def _parse_palette(self, bits_per_block: int, data: bytes) -> bytes:
        """Parse palette and return leftover bytes."""

        self.palette, data = extract_palette(bits_per_block, data)
        return data

    def _parse_block_data(self, bits_per_block: int, data: bytes):
        """
        Parse data from chunk section.
        Docs: https://wiki.vg/index.php?title=Chunk_Format&oldid=14135#Chunk_Section_structure

        To use this, self.palette needs to be set correctly (by self._parse_palette).
        """
        # 4096 indices are coded into data_array_length longs.
        # Number of longs in the following array.
        data_array_length, data = converters.extract_varint_as_int(data)

        # Compacted list of 4096 indices pointing to state IDs in the Palette
        array_of_longs = [int] * data_array_length
        extract_long = converters.extract_long
        for idx in range(data_array_length):
            # TODO: Optimize (create: extract_longs(n_of_longs, data))
            long_id, data = extract_long(data)
            array_of_longs[idx] = long_id

        # The number of longs needed for the data array can be
        # calculated as (blocks * bits_per_block) /  bits per long
        #           ((16×16×16) * bits_per_block) / 64
        # so bits_per_block = number_of_longs / 64
        bits_per_block = len(array_of_longs) // 64

        # TODO:

        self.blocks = GlobalPalette.parse_block_data(array_of_longs)
        # print(self.blocks)

    def _read_bits_of_data(self, number_of_bits: int):
        pass


class Chunk:
    """Chunk data container and parser. (column 16x256x16)"""

    sections: [[ChunkSection] * 16] * 16 = None
    biomes: bytes = None

    def __init__(self):
        self.sections = [[ChunkSection] * 16] * 16

    @staticmethod
    def new(section_data: bytes, mask: int) -> 'Chunk()':
        """
        Create new Chunk and insert data into it.

        :param mask: see World().parse_chunk()
        :param section_data: bytes from which extract data.
        :return Chunk object
        """
        chunk = Chunk()
        chunk.update(section_data=section_data,
                     primary_bit_mask=mask,
                     contain_biomes=True)
        return chunk

    def update(self,
               section_data: bytes,
               primary_bit_mask: int,
               contain_biomes: bool = False):
        """
        Parse data and fill chunk using that data.

        :param primary_bit_mask: see World().parse_chunk()
        :param section_data: bytes from which extract data.
        :param contain_biomes: yup definitely needs description
        """

        # Bitmask(0-15) with bits set to 1 for every sent block.
        # Block: 16×16×16, from y=0 to y=15.
        # primary_bit_mask: Union[int, bytes(int, int)]
        # if isinstance(primary_bit_mask, int):
        #     primary_bit_mask = [primary_bit_mask, ]

        # Number indicates that section has been sent. <0; 15>
        row: int = 0

        bit_of_section: int = 0x01
        while bit_of_section < 0x100:  # Mask range: <0x00:0xFF>
            # If section has been sent.
            if primary_bit_mask & bit_of_section:
                print("║" + f" SECTION: {int(math.log(bit_of_section, 2))} ".center(150, "═") + "║")

                self.sections[row], section_data = ChunkSection.parse(section_data)
            else:
                pass  # print("║" + f" SECTION: {int(math.log(bit_of_section, 2))} NOT PRESENT ".center(150, "═") + "║")
            row += 1
            bit_of_section <<= 1

        # TODO: Biomes.

        # section_data at this point contains leftover of data:
        # [Biomes] + Entity data
        if contain_biomes:
            self.parse_biomes(section_data[:256])
            self.parse_entities_data(section_data[256:])
        else:
            self.parse_entities_data(section_data)

        print("╚" + f"".center(150, "═") + "╝")

    def parse_entities_data(self, entitles_data: bytes):
        pass

    def parse_biomes(self, biomes_data: bytes):
        pass
