HEX_BYTES_TO_DEC = {
    b'': None, b'\x00': 0, b'\x01': 1, b'\x02': 2, b'\x03': 3, b'\x04': 4, b'\x05': 5,
    b'\x06': 6, b'\x07': 7, b'\x08': 8, b'\t': 9, b'\n': 10, b'\x0b': 11,
    b'\x0c': 12, b'\r': 13, b'\x0e': 14, b'\x0f': 15, b'\x10': 16, b'\x11': 17,
    b'\x12': 18, b'\x13': 19, b'\x14': 20, b'\x15': 21, b'\x16': 22, b'\x17': 23,
    b'\x18': 24, b'\x19': 25, b'\x1a': 26, b'\x1b': 27, b'\x1c': 28, b'\x1d': 29,
    b'\x1e': 30, b'\x1f': 31, b' ': 32, b'!': 33, b'"': 34, b'#': 35, b'$': 36,
    b'%': 37, b'&': 38, b"'": 39, b'(': 40, b')': 41, b'*': 42, b'+': 43,
    b',': 44, b'-': 45, b'.': 46, b'/': 47, b'0': 48, b'1': 49, b'2': 50,
    b'3': 51, b'4': 52, b'5': 53, b'6': 54, b'7': 55, b'8': 56, b'9': 57,
    b':': 58, b';': 59, b'<': 60, b'=': 61, b'>': 62, b'?': 63, b'@': 64,
    b'A': 65, b'B': 66, b'C': 67, b'D': 68, b'E': 69, b'F': 70, b'G': 71,
    b'H': 72, b'I': 73, b'J': 74, b'K': 75, b'L': 76, b'M': 77, b'N': 78,
    b'O': 79, b'P': 80, b'Q': 81, b'R': 82, b'S': 83, b'T': 84, b'U': 85,
    b'V': 86, b'W': 87, b'X': 88, b'Y': 89, b'Z': 90, b'[': 91, b'\\': 92,
    b']': 93, b'^': 94, b'_': 95, b'`': 96, b'a': 97, b'b': 98, b'c': 99,
    b'd': 100, b'e': 101, b'f': 102, b'g': 103, b'h': 104, b'i': 105, b'j': 106,
    b'k': 107, b'l': 108, b'm': 109, b'n': 110, b'o': 111, b'p': 112, b'q': 113,
    b'r': 114, b's': 115, b't': 116, b'u': 117, b'v': 118, b'w': 119, b'x': 120,
    b'y': 121, b'z': 122, b'{': 123, b'|': 124, b'}': 125, b'~': 126,
    b'\x7f': 127, b'\x80': 128, b'\x81': 129, b'\x82': 130, b'\x83': 131,
    b'\x84': 132, b'\x85': 133, b'\x86': 134, b'\x87': 135, b'\x88': 136,
    b'\x89': 137, b'\x8a': 138, b'\x8b': 139, b'\x8c': 140, b'\x8d': 141,
    b'\x8e': 142, b'\x8f': 143, b'\x90': 144, b'\x91': 145, b'\x92': 146,
    b'\x93': 147, b'\x94': 148, b'\x95': 149, b'\x96': 150, b'\x97': 151,
    b'\x98': 152, b'\x99': 153, b'\x9a': 154, b'\x9b': 155, b'\x9c': 156,
    b'\x9d': 157, b'\x9e': 158, b'\x9f': 159, b'\xa0': 160, b'\xa1': 161,
    b'\xa2': 162, b'\xa3': 163, b'\xa4': 164, b'\xa5': 165, b'\xa6': 166,
    b'\xa7': 167, b'\xa8': 168, b'\xa9': 169, b'\xaa': 170, b'\xab': 171,
    b'\xac': 172, b'\xad': 173, b'\xae': 174, b'\xaf': 175, b'\xb0': 176,
    b'\xb1': 177, b'\xb2': 178, b'\xb3': 179, b'\xb4': 180, b'\xb5': 181,
    b'\xb6': 182, b'\xb7': 183, b'\xb8': 184, b'\xb9': 185, b'\xba': 186,
    b'\xbb': 187, b'\xbc': 188, b'\xbd': 189, b'\xbe': 190, b'\xbf': 191,
    b'\xc0': 192, b'\xc1': 193, b'\xc2': 194, b'\xc3': 195, b'\xc4': 196,
    b'\xc5': 197, b'\xc6': 198, b'\xc7': 199, b'\xc8': 200, b'\xc9': 201,
    b'\xca': 202, b'\xcb': 203, b'\xcc': 204, b'\xcd': 205, b'\xce': 206,
    b'\xcf': 207, b'\xd0': 208, b'\xd1': 209, b'\xd2': 210, b'\xd3': 211,
    b'\xd4': 212, b'\xd5': 213, b'\xd6': 214, b'\xd7': 215, b'\xd8': 216,
    b'\xd9': 217, b'\xda': 218, b'\xdb': 219, b'\xdc': 220, b'\xdd': 221,
    b'\xde': 222, b'\xdf': 223, b'\xe0': 224, b'\xe1': 225, b'\xe2': 226,
    b'\xe3': 227, b'\xe4': 228, b'\xe5': 229, b'\xe6': 230, b'\xe7': 231,
    b'\xe8': 232, b'\xe9': 233, b'\xea': 234, b'\xeb': 235, b'\xec': 236,
    b'\xed': 237, b'\xee': 238, b'\xef': 239, b'\xf0': 240, b'\xf1': 241,
    b'\xf2': 242, b'\xf3': 243, b'\xf4': 244, b'\xf5': 245, b'\xf6': 246,
    b'\xf7': 247, b'\xf8': 248, b'\xf9': 249, b'\xfa': 250, b'\xfb': 251,
    b'\xfc': 252, b'\xfd': 253, b'\xfe': 254, b'\xff': 255
    }