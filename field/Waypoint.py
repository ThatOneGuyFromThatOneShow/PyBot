import math


FEET_TO_METERS = 0.3048


class Waypoint:
    def __init__(self, x, y, angle):
        self.x = x * FEET_TO_METERS
        self.y = y * FEET_TO_METERS
        self.angle = math.radians(angle)
