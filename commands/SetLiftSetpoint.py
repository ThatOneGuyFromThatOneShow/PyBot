from wpilib.command.command import Command

from subsystems.Lift import Lift
from subsystems.LiftHeight import LiftHeight


class SetLiftSetpoint(Command):
    def __init__(self, lift_height: LiftHeight, lift: Lift):
        super().__init__()

        self.lift = lift
        self.lift_height = lift_height

        self.requires(lift)

    def initialize(self):
        self.lift.set_lift_height(self.lift_height)

    def isFinished(self):
        return self.lift.at_target()
