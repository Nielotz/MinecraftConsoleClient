import misc.converters as converters
from versions.base.data_structures.entities import Entity
from versions.base.data_structures.world.chunk import Chunk


class World:
    """Hold and manages world data, eg. chunks, etc."""

    def __init__(self):
        # Keys are generated like this: "chunk_x chunk_y"
        self.chunks: {str: Chunk, } = {}
        self.entities: {str: Entity, } = {}

    def parse_chunk_packet(self, data: memoryview):
        """Parse data as chunk data."""

        # Chunk coordinates (block coordinate divided by 16, rounded down)
        chunk_x, data = converters.extract_int(data)
        chunk_z, data = converters.extract_int(data)

        """When ground-up continuous is set - create a new chunk. 
        This includes z biomes data and all (non-empty) sections in the chunk.
        Sections not specified in the primary bit mask are empty.
        
        When ground-up continuous is not set, then the chunk data
        packet acts as a large Multi Block Change packet,
        changing all of the blocks in the given section at once.
        Sections not specified in the primary bit mask are
        not changed and should be left as-is."""
        create_new_aka_ground_up_continuous, data = converters.extract_bool(data)

        """Bitmask with bits set to 1 for every 16×16×16 chunk section
        whose data is included in Data.
        The least significant bit represents the chunk section
        at the bottom of the chunk column (from y=0 to y=15)."""
        mask, data = converters.extract_varint_as_int(data)

        # Size of chunk data in bytes.
        size, data = converters.extract_varint_as_int(data)

        # Extract and parse data structure array.
        chunk_key = " ".join((str(chunk_x), str(chunk_z)))
        if create_new_aka_ground_up_continuous:
            self.chunks[chunk_key] = Chunk.new(data[:size], mask)
        else:  # Alter old one.
            self.chunks[chunk_key].update(data[:size], mask)

        # self._load_entities(section_data=data[size:])

    def _load_entities(self, section_data: memoryview):
        # TODO: Entities.
        return
