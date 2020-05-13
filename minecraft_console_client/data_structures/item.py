class Item:
    present = False
    item_id = None
    item_count = None
    NBT = None

    def __init__(self, data: bytes = None):
        if data is not None:
            present = (data[0] & 0x01) and True
            if present:
                self.item_id, data = unpack_varint(data[1::])
                self.item_count, data = extract_byte(data)
                x, data = extract_byte(data)
                if x != 0:
                    print(x, data)
                    print()
