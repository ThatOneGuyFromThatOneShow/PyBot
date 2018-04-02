from wpilib.command.command import Command

from subsystems.Drivetrain import Drivetrain


class ShiftToHighGear(Command):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__()

        self.drivetrain = drivetrain

    def initialize(self):
        self.drivetrain.switch_high_gear()

    def isFinished(self):
        return True
