from enum import Enum


class State(Enum):
    REQUEST = b'\x01'
    PING = b'\x01'
    LOGIN = b'\x02'
