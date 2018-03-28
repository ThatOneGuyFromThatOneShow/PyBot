from wpilib.command.command import Command
from subsystems.Grabber import Grabber


class CloseGrabber(Command):
    grabber: Grabber

    def __init__(self, grabber: Grabber):
        super().__init__("CloseGrabber")

        self.grabber = grabber

    def initialize(self):
        self.grabber.capture_cube()

    def isFinished(self):
        return True
