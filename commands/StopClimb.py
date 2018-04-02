from wpilib.command.command import Command

from subsystems.Climber import Climber


class StopClimb(Command):
    def __init__(self, climber: Climber):
        super().__init__()

        self.climber = climber
        self.requires(climber)

    def initialize(self):
        self.climber.stop()
        self.climber.lock()

    def isFinished(self):
        return True
