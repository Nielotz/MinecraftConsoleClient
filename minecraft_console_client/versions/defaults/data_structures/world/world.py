import misc.converters as converters
from versions.defaults.data_structures.world.chunk import Chunk
from versions.defaults.data_structures.world.chunk import ChunkSection
from versions.defaults.data_structures.entities import Entity


class World:
    """Hold and manages world data, eg. chunks, etc."""

    # Keys are generated like this: "chunk_x chunk_y"
    chunks: {str: Chunk, } = None
    entities: {str: Entity} = None

    def __init__(self):
        self.chunks: {str: Chunk, } = {}

    def parse_chunk(self, data: bytes):
        """Parse data as chunk data."""

        # Chunk position, any in-chunk block // 16
        chunk_x, data = converters.extract_int(data)
        chunk_y, data = converters.extract_int(data)

        # When ground-up continuous is set, the chunk data packet
        # is used to create a new chunk. This includes biome* data,
        # and all (non-empty) sections in the chunk.
        # Sections not specified in the primary bit mask are empty.
        #
        # When ground-up continuous is not set, then the chunk data
        # packet acts as a large Multi Block Change packet,
        # changing all of the blocks in the given section at once.
        # Sections not specified in the primary bit mask are
        # not changed and should be left as-is.
        ground_up_continuous, data = converters.extract_boolean(data)

        # Bitmask with bits set to 1 for every 16×16×16 chunk section
        # whose data is included in Data.
        # The least significant bit represents the chunk section
        # at the bottom of the chunk column (from y=0 to y=15).
        mask, data = converters.extract_varint_as_int(data)

        # Size of chunk data in bytes.
        size, data = converters.extract_varint_as_int(data)

        print("╔" + f" chunk_x: {chunk_x}, chunk_y: {chunk_y}, ground_up_continuous: {ground_up_continuous} ".center(150, "═") + "╗")

        chunk_key = " ".join((str(chunk_x), str(chunk_y)))
        if ground_up_continuous:
            # Create new chunk.
            self.chunks[chunk_key] = Chunk.new(data[:size], mask)
        else:
            # Alter old one.
            self.chunks[chunk_key].alter(data[:size], mask)

        # Parse entities.
        entities_data = data[size:]

