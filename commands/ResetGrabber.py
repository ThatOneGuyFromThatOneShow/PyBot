from wpilib.command import Command
from subsystems.Grabber import Grabber


class ResetGrabber(Command):
    grabber: Grabber

    def __init__(self, grabber: Grabber):
        super().__init__()

        self.grabber = grabber

    def initialize(self):
        self.grabber.reset()

    def isFinished(self):
        return True
