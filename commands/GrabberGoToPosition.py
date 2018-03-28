from wpilib.command.command import Command
from subsystems.Grabber import Grabber
from subsystems.GrabberPosition import GrabberPosition


class GrabberGoToPosition(Command):
    grabber: Grabber
    position: GrabberPosition

    def __init__(self, grabber: Grabber, position: GrabberPosition):
        super().__init__("GrabberGoToPosition")

        self.grabber = grabber
        self.position = position

        self.requires(grabber)
        self.setInterruptible(True)

    def initialize(self):
        self.grabber.go_to_set_point(self.position)

    def isFinished(self):
        self.grabber.at_target_position()
