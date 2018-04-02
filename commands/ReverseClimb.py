from wpilib.command.command import Command

from subsystems.Climber import Climber


class ReverseClimb(Command):
    def __init__(self, climber: Climber):
        super().__init__()

        self.climber = climber
        self.requires(climber)

    def initialize(self):
        self.climber.release()
        self.climber.reverse()

    def isFinished(self):
        return True
