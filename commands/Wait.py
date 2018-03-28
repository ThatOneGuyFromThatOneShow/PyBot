from wpilib.command import Command
import time


class Wait(Command):
    time: float
    start_time: float
    target_time: float

    def __init__(self, target_time: float):
        super().__init__()

        self.target_time = target_time / 1000

    def initialize(self):
        self.start_time = time.time()

    def isFinished(self):
        return time.time() - self.start_time >= self.target_time
