from typing import Union


class Position:

    def __init__(self, x: float, y: float, z: float):
        """ pos = (x, y, z)"""
        self.pos = {'x': x, 'y': y, 'z': z}

    def get_list(self):
        pos = self.pos
        return pos['x'], pos['y'], pos['z']

    def __repr__(self):
        return f"[x: {self.pos['x']}, y: {self.pos['y']}, z: {self.pos['z']}]"
