from wpilib.command.command import Command
from subsystems.Grabber import Grabber


class GrabberMoveSpeed(Command):
    grabber: Grabber
    speed: float

    def __init__(self, grabber: Grabber, speed: float):
        super().__init__("GrabberMoveSpeed")

        self.grabber = grabber
        self.speed = speed

        self.requires(grabber)
        self.setInterruptible(True)

    def initialize(self):
        self.grabber.set_speed(self.speed)

    def isFinished(self):
        return True
