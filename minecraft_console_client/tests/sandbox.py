from collections import Counter

from misc import converters
from versions.defaults.data_structures.world.palette import extract_palette


def read_from_file(filename="chunk_data.txt"):
    with open("chunk_data.txt", "rb") as f:
        return f.read()


data = read_from_file()

# Read top of the packet.
chunk_x, data = converters.extract_int(data)
chunk_z, data = converters.extract_int(data)
create_new_aka_ground_up_continuous, data = converters.extract_boolean(data)
mask, data = converters.extract_varint_as_int(data)
size, data = converters.extract_varint_as_int(data)
data = data[:size]

for section_idx in range(0, 16):
    if mask & (1 << section_idx):
        # ChunkSection.parse_data(data)
        bits_per_block, data = converters.extract_unsigned_byte(data)

        palette, data = extract_palette(bits_per_block, data)

        # 12551
        data_array_length, data = converters.extract_varint_as_int(data)

        def extract():
            global data
            # 12549
            longs = [-1] * data_array_length
            extract_unsigned_long = converters.extract_unsigned_long
            for idx in range(data_array_length):
                # TODO: Optimize (maybe create: extract_longs(n_of_longs, data)?)
                longs[idx], data = extract_unsigned_long(data)

            # bits_per_block = 4
            # longs = (72084535294427168, 144343914412032032)

            # 10501
            # self.palette.parse_block_data(longs=longs)
            # extract_blocks_from_compacted_data_array
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


        extracted_indices = extract()
        print(sorted(extracted_indices, reverse=True))

        z = [palette.palette[zz] / 16 for zz in extracted_indices]
        print(Counter(z).most_common())
        print(len(Counter(z).most_common()))
        print(sorted(z, reverse=True))
        x = 1
