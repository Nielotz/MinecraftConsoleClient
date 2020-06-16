from typing import Union


class Position:
    pos = {'x': None, 'y': None, 'z': None}

    def __init__(self, pos: (float, float, float)):
        """ pos = (x, y, z)"""
        self.pos['x'] = pos[0]
        self.pos['y'] = pos[1]
        self.pos['z'] = pos[2]

    def get_list(self):
        pos = self.pos
        return pos['x'], pos['y'], pos['z']

    def __repr__(self):
        return f"[x: {self.pos['x']}, y: {self.pos['y']}, z: {self.pos['z']}]"
