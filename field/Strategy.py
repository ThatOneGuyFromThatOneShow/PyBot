from enum import Enum, auto


class Strategy(Enum):
    SWITCH_SAME = auto()
    SCALE_SAME = auto()
    SWITCH_OPPOSITE = auto()
    SCALE_OPPOSITE = auto()
    DRIVE_FORWARD = auto()
