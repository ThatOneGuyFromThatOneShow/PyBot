from enum import Enum, auto


class Strategy(Enum):
    SWITCH_SAME = 0
    SCALE_SAME = 1
    SWITCH_OPPOSITE = 2
    SCALE_OPPOSITE = 3
    DRIVE_FORWARD = 4
