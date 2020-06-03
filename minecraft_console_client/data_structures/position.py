from typing import Union


class Position:
    x = None
    y = None
    z = None

    def __init__(self, pos: (int, int, int)):
        """ pos = (x, y, z)"""
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]

    def get(self):
        """ Returns tuple (x, y, z)"""
        return self.x, self.y, self.z

    def __repr__(self):
        return f"[x: {self.x}, y: {self.y}, z: {self.z}]"
