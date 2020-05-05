from enum import Enum


class State(Enum):
    STATUS = b'\x01'
    LOGIN = b'\x02'
