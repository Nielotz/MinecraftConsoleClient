import logging

from versions.base.data_structures.world.chunk_section import ChunkSection

logger = logging.getLogger('chunkParser')


class Chunk:
    """Chunk data container and parser. (column 16x256x16)"""

    sections: [[ChunkSection] * 16] * 16 = None
    biomes: bytes = None

    def __init__(self):
        self.sections = [[ChunkSection, ] * 16] * 16

    @staticmethod
    def new(section_data: bytes,
            mask: int) -> 'Chunk':
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

    def update(self, section_data: bytes,
               primary_bit_mask: int,
               contain_biomes: bool = False):
        """
        Parse data and fill chunk using that data.

        :param primary_bit_mask: see World().parse_chunk()
        :param section_data: bytes from which extract data.
        :param contain_biomes: yup definitely needs description
        """
        self._load_chunk_sections(section_data=section_data, primary_bit_mask=primary_bit_mask)
        if contain_biomes:
            pass
        #     self._load_biomes(section_data=section_data)
        # self._load_entities(section_data=section_data)

    def _load_chunk_sections(self, section_data: bytes,
                             primary_bit_mask: int):
        """
        Bitmask (0-15) with bits set to 1 for every sent chunk section.
        Block: 16×16×16, from y=0 to y=15.
        """
        for section_idx in range(0, 16):
            if primary_bit_mask & (1 << section_idx):
                self.sections[section_idx], section_data = ChunkSection.parse_data(section_data)

    # def _load_biomes(self, section_data: bytes):
    #     # TODO: Biomes.
    #     pass
    #
    # def _load_entities(self, section_data: bytes):
    #     # TODO: Entities.
    #     pass
