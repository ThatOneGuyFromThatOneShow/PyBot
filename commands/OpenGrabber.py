from wpilib.command.command import Command
from subsystems.Grabber import Grabber


class OpenGrabber(Command):
    grabber: Grabber

    def __init__(self, grabber: Grabber):
        super().__init__("OpenGrabber")

        self.grabber = grabber

    def initialize(self):
        self.grabber.release_cube()

    def isFinished(self):
        return True
