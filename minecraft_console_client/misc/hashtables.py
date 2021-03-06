"""Holder for hashtables."""

# key: bytes
# value: tuple made of: int extracted from byte, bool expect_next_byte
#        (int_from_bytes & 0x7F,            bool(int_from_bytes & 0x80))
#
# Generated using:
# z = {b'': (None, False),}
# for i in range(0, 256):
#     x = hex(i)[2:]
#     if len(x) & 1:
#         x = '0' + x
#     z[bytes.fromhex(x)] = (i & 0x7F, bool(i & 0x80))
VARINT_BYTES = {
    b'': (None, False), b'\x00': (0, False), b'\x01': (1, False),
    b'\x02': (2, False), b'\x03': (3, False), b'\x04': (4, False),
    b'\x05': (5, False), b'\x06': (6, False), b'\x07': (7, False),
    b'\x08': (8, False), b'\t': (9, False), b'\n': (10, False),
    b'\x0b': (11, False), b'\x0c': (12, False), b'\r': (13, False),
    b'\x0e': (14, False), b'\x0f': (15, False), b'\x10': (16, False),
    b'\x11': (17, False), b'\x12': (18, False), b'\x13': (19, False),
    b'\x14': (20, False), b'\x15': (21, False), b'\x16': (22, False),
    b'\x17': (23, False), b'\x18': (24, False), b'\x19': (25, False),
    b'\x1a': (26, False), b'\x1b': (27, False), b'\x1c': (28, False),
    b'\x1d': (29, False), b'\x1e': (30, False), b'\x1f': (31, False),
    b' ': (32, False), b'!': (33, False), b'"': (34, False), b'#': (35, False),
    b'$': (36, False), b'%': (37, False), b'&': (38, False), b"'": (39, False),
    b'(': (40, False), b')': (41, False), b'*': (42, False), b'+': (43, False),
    b',': (44, False), b'-': (45, False), b'.': (46, False), b'/': (47, False),
    b'0': (48, False), b'1': (49, False), b'2': (50, False), b'3': (51, False),
    b'4': (52, False), b'5': (53, False), b'6': (54, False), b'7': (55, False),
    b'8': (56, False), b'9': (57, False), b':': (58, False), b';': (59, False),
    b'<': (60, False), b'=': (61, False), b'>': (62, False), b'?': (63, False),
    b'@': (64, False), b'A': (65, False), b'B': (66, False), b'C': (67, False),
    b'D': (68, False), b'E': (69, False), b'F': (70, False), b'G': (71, False),
    b'H': (72, False), b'I': (73, False), b'J': (74, False), b'K': (75, False),
    b'L': (76, False), b'M': (77, False), b'N': (78, False), b'O': (79, False),
    b'P': (80, False), b'Q': (81, False), b'R': (82, False), b'S': (83, False),
    b'T': (84, False), b'U': (85, False), b'V': (86, False), b'W': (87, False),
    b'X': (88, False), b'Y': (89, False), b'Z': (90, False), b'[': (91, False),
    b'\\': (92, False), b']': (93, False), b'^': (94, False),
    b'_': (95, False), b'`': (96, False), b'a': (97, False), b'b': (98, False),
    b'c': (99, False), b'd': (100, False), b'e': (101, False),
    b'f': (102, False), b'g': (103, False), b'h': (104, False),
    b'i': (105, False), b'j': (106, False), b'k': (107, False),
    b'l': (108, False), b'm': (109, False), b'n': (110, False),
    b'o': (111, False), b'p': (112, False), b'q': (113, False),
    b'r': (114, False), b's': (115, False), b't': (116, False),
    b'u': (117, False), b'v': (118, False), b'w': (119, False),
    b'x': (120, False), b'y': (121, False), b'z': (122, False),
    b'{': (123, False), b'|': (124, False), b'}': (125, False),
    b'~': (126, False), b'\x7f': (127, False), b'\x80': (0, True),
    b'\x81': (1, True), b'\x82': (2, True), b'\x83': (3, True),
    b'\x84': (4, True), b'\x85': (5, True), b'\x86': (6, True),
    b'\x87': (7, True), b'\x88': (8, True), b'\x89': (9, True),
    b'\x8a': (10, True), b'\x8b': (11, True), b'\x8c': (12, True),
    b'\x8d': (13, True), b'\x8e': (14, True), b'\x8f': (15, True),
    b'\x90': (16, True), b'\x91': (17, True), b'\x92': (18, True),
    b'\x93': (19, True), b'\x94': (20, True), b'\x95': (21, True),
    b'\x96': (22, True), b'\x97': (23, True), b'\x98': (24, True),
    b'\x99': (25, True), b'\x9a': (26, True), b'\x9b': (27, True),
    b'\x9c': (28, True), b'\x9d': (29, True), b'\x9e': (30, True),
    b'\x9f': (31, True), b'\xa0': (32, True), b'\xa1': (33, True),
    b'\xa2': (34, True), b'\xa3': (35, True), b'\xa4': (36, True),
    b'\xa5': (37, True), b'\xa6': (38, True), b'\xa7': (39, True),
    b'\xa8': (40, True), b'\xa9': (41, True), b'\xaa': (42, True),
    b'\xab': (43, True), b'\xac': (44, True), b'\xad': (45, True),
    b'\xae': (46, True), b'\xaf': (47, True), b'\xb0': (48, True),
    b'\xb1': (49, True), b'\xb2': (50, True), b'\xb3': (51, True),
    b'\xb4': (52, True), b'\xb5': (53, True), b'\xb6': (54, True),
    b'\xb7': (55, True), b'\xb8': (56, True), b'\xb9': (57, True),
    b'\xba': (58, True), b'\xbb': (59, True), b'\xbc': (60, True),
    b'\xbd': (61, True), b'\xbe': (62, True), b'\xbf': (63, True),
    b'\xc0': (64, True), b'\xc1': (65, True), b'\xc2': (66, True),
    b'\xc3': (67, True), b'\xc4': (68, True), b'\xc5': (69, True),
    b'\xc6': (70, True), b'\xc7': (71, True), b'\xc8': (72, True),
    b'\xc9': (73, True), b'\xca': (74, True), b'\xcb': (75, True),
    b'\xcc': (76, True), b'\xcd': (77, True), b'\xce': (78, True),
    b'\xcf': (79, True), b'\xd0': (80, True), b'\xd1': (81, True),
    b'\xd2': (82, True), b'\xd3': (83, True), b'\xd4': (84, True),
    b'\xd5': (85, True), b'\xd6': (86, True), b'\xd7': (87, True),
    b'\xd8': (88, True), b'\xd9': (89, True), b'\xda': (90, True),
    b'\xdb': (91, True), b'\xdc': (92, True), b'\xdd': (93, True),
    b'\xde': (94, True), b'\xdf': (95, True), b'\xe0': (96, True),
    b'\xe1': (97, True), b'\xe2': (98, True), b'\xe3': (99, True),
    b'\xe4': (100, True), b'\xe5': (101, True), b'\xe6': (102, True),
    b'\xe7': (103, True), b'\xe8': (104, True), b'\xe9': (105, True),
    b'\xea': (106, True), b'\xeb': (107, True), b'\xec': (108, True),
    b'\xed': (109, True), b'\xee': (110, True), b'\xef': (111, True),
    b'\xf0': (112, True), b'\xf1': (113, True), b'\xf2': (114, True),
    b'\xf3': (115, True), b'\xf4': (116, True), b'\xf5': (117, True),
    b'\xf6': (118, True), b'\xf7': (119, True), b'\xf8': (120, True),
    b'\xf9': (121, True), b'\xfa': (122, True), b'\xfb': (123, True),
    b'\xfc': (124, True), b'\xfd': (125, True), b'\xfe': (126, True),
    b'\xff': (127, True)}

GAME_DIFFICULTY = {
    0: "peaceful",
    1: "easy",
    2: "normal",
    3: "hard"
}

GAMEMODE = {
    0: "survival",
    1: "creative",
    2: "adventure",
    3: "spectator",
}

# Sth related to change_game_state.
NOT_SURE_WHAT = {
    0: "invalid_bed",
    1: "end_raining",
    2: "begin_raining",
    3: "change_gamemode",
    4: "exit_end",
    5: "demo_message",
    6: "arrow_hitting_player",
    7: "fade_value",
    8: "fade_time",
    10: "play_elder_guardian_mob_appearance",
}
