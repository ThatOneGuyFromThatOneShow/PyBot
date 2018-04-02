from subsystems.Climber import Climber
from subsystems.Lift import Lift
from subsystems.Grabber import Grabber
from subsystems.LiftHeight import LiftHeight
from subsystems.GrabberPosition import GrabberPosition
from wpilib.command.command import Command


class Climb(Command):
    def __init__(self, climber: Climber, lift: Lift, grabber: Grabber):
        super().__init__()

        self.climber = climber
        self.lift = lift
        self.grabber = grabber

        self.requires(climber)
        self.requires(lift)

    def initialize(self):
        self.climber.release()
        self.climber.climb()
        self.lift.set_lift_height(LiftHeight.EXCHANGE)
        self.grabber.go_to_set_point(GrabberPosition.SHOOT)

    def isFinished(self):
        return True
