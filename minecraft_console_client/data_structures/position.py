from typing import Union


class Position:
    pos = {'x': 0.0, 'y': 0.0, 'z': 0.0}

    def __init__(self, x: float, y: float, z: float):
        """ pos = (x, y, z)"""
        self.pos['x'] = x
        self.pos['y'] = y
        self.pos['z'] = z

    def get_list(self):
        pos = self.pos
        return pos['x'], pos['y'], pos['z']

    def __repr__(self):
        return f"[x: {self.pos['x']}, y: {self.pos['y']}, z: {self.pos['z']}]"
