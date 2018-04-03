import math

from wpilib.command.commandgroup import CommandGroup

from commands.CloseGrabber import CloseGrabber
from commands.GoToDistance import GoToDistance
from commands.GrabberGoToPosition import GrabberGoToPosition
from commands.OpenGrabber import OpenGrabber
from commands.SetLiftSetpoint import SetLiftSetpoint
from commands.TurnToAngle import TurnToAngle
from commands.Wait import Wait
from field.Strategy import Strategy
from field.Waypoint import Waypoint
from subsystems.Drivetrain import Drivetrain
from subsystems.Grabber import Grabber
from subsystems.GrabberPosition import GrabberPosition
from subsystems.Lift import Lift
from subsystems.LiftHeight import LiftHeight

METERS_TO_FEET = 3.28084
MOVE_SPEED = 1
TURN_SPEED = 1


class AutoCommand(CommandGroup):
    def __init__(self, points: [Waypoint], strategy: Strategy, drivetrain: Drivetrain, lift: Lift, grabber: Grabber):
        super().__init__()

        self.drivetrain = drivetrain

        self.cur_absolute_angle = 0
        self.cur_absolute_x = 1
        self.cur_absolute_y = 0
        is_first = False

        drivetrain.switch_low_gear()
        self.addSequential(Wait(350))
        self.addSequential(GoToDistance(1, 1, drivetrain))
        last_point = points[len(points) - 1]

        for point in points:
            x = (point.x * METERS_TO_FEET - 1 if is_first else point.x * METERS_TO_FEET) - self.cur_absolute_x
            y = self.cur_absolute_y - (point.y * METERS_TO_FEET)
            distance = math.sqrt(x*x + y*y)
            is_first = False

            if x == 0 and y > 0:
                self.turn(90)
            elif x == 0 and y < 0:
                self.turn(-90)
            elif x > 0 and y == 0:
                self.turn(0)
            elif x < 0 and y == 0:
                self.turn(180)
            elif x > 0 and y > 0:
                self.turn(math.degrees(math.atan(y/x)))
            elif x > 0 and y < 0:
                self.turn(math.degrees(math.atan(-y/x)))
            elif x < 0 and y > 0:
                self.turn(math.degrees(math.atan(y/-x)))
            elif x < 0 and y < 0:
                self.turn(math.degrees(math.atan(-y/-x)))

            self.cur_absolute_x += x
            self.cur_absolute_y -= y
            self.addSequential(Wait(200))
            self.addSequential(GoToDistance(MOVE_SPEED, distance, drivetrain))

        self.addSequential(Wait(200))
        self.turn(math.degrees(-last_point.angle))

        self.addSequential(SetLiftSetpoint(self.calcLiftHeight(strategy), lift))
        self.addSequential(GoToDistance(1, 1, drivetrain))
        self.addSequential(GrabberGoToPosition(grabber, GrabberPosition.SHOOT))
        self.addSequential(OpenGrabber(grabber) if self.calcOpenGrabber(strategy) else CloseGrabber(grabber))

    def calcLiftHeight(self, strategy: Strategy) -> LiftHeight:
        if strategy == Strategy.SWITCH_SAME or Strategy.SWITCH_OPPOSITE:
            return LiftHeight.SWITCH
        elif strategy == Strategy.SCALE_SAME or Strategy.SCALE_OPPOSITE:
            return LiftHeight.SCALE_TOP
        else:
            return LiftHeight.FLOOR

    def clacGrabberPosition(self, strategy: Strategy) -> GrabberPosition:
        if strategy == Strategy.SWITCH_SAME or Strategy.SWITCH_OPPOSITE:
            return GrabberPosition.EXCHANGE
        elif strategy == Strategy.SCALE_SAME or Strategy.SCALE_OPPOSITE:
            return GrabberPosition.SHOOT
        else:
            return GrabberPosition.HIGH
        
    def calcOpenGrabber(self, strategy: Strategy) -> bool:
        if strategy == Strategy.DRIVE_FORWARD:
            return False
        else:
            return True
        
    def addAngle(self, angle):
        self.cur_absolute_angle += angle
    
    def getTurnAngle(self, angle):
        angle = angle % 360
        return angle - 360 if angle > 180 else angle
    
    def turnFromAbsolute(self, angle):
        return self.getTurnAngle(angle - self.cur_absolute_angle)
    
    def turn(self, angle):
        angle = self.turnFromAbsolute(angle)
        self.addAngle(angle)
        self.addSequential(TurnToAngle(math.copysign(TURN_SPEED, angle), abs(angle), self.drivetrain))
