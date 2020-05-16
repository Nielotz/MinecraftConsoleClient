class Position:
    x = None
    y = None
    z = None
    yaw = None
    pitch = None

    def __init__(self, pos: (int, int, int), yaw=None, pitch=None):
        """ pos = (x, y, z)"""
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.yaw = yaw
        self.pitch = pitch

    def __repr__(self):
        return f"[x: {self.x}, y: {self.y}, z: {self.z}, " \
               f"yaw: {self.yaw}, pitch: {self.pitch}]"
