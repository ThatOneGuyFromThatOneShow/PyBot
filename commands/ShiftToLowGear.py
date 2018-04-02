from subsystems.Climber import Climber
from subsystems.Lift import Lift
from subsystems.Grabber import Grabber
from subsystems.Drivetrain import Drivetrain
from subsystems.LiftHeight import LiftHeight
from subsystems.GrabberPosition import GrabberPosition
from wpilib.command.command import Command

class ShiftToLowGear(Command):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__()

        self.drivetrain = drivetrain

    def initialize(self):
        self.drivetrain.switch_low_gear()

    def isFinished(self):
        return True
