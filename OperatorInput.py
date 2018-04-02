from wpilib.joystick import Joystick
from wpilib.buttons import JoystickButton
from subsystems.Drivetrain import Drivetrain
from subsystems.Grabber import Grabber
from subsystems.Lift import Lift
from subsystems.Climber import Climber
from commands.OpenGrabber import OpenGrabber
from commands.CloseGrabber import CloseGrabber
from commands.GrabberGoToPosition import GrabberGoToPosition
from subsystems.GrabberPosition import GrabberPosition
from subsystems.LiftHeight import LiftHeight
from commands.ShiftToLowGear import ShiftToLowGear
from commands.ShiftToHighGear import ShiftToHighGear
from commands.Climb import Climb
from commands.ReverseClimb import ReverseClimb
from commands.SetLiftSetpoint import SetLiftSetpoint
from commands.StopClimb import StopClimb


class DriverJoystick(Joystick):
    def __init__(self, port):
        super().__init__(port)

        self.shift_low_gear = JoystickButton(self, 1)
        self.shift_high_gear = JoystickButton(self, 2)
        self.climb = JoystickButton(self, 3)
        self.reverse_climb = JoystickButton(self, 4)


class OperatorJoystick(Joystick):
    def __init__(self, port):
        super().__init__(port)

        self.grabber_open = JoystickButton(self, 1)  # Trigger
        self.grabber_close = JoystickButton(self, 2)  # Thumb
        self.grabber_low = JoystickButton(self, 3)  # Bottom Left
        self.grabber_exchange = JoystickButton(self, 4)  # Bottom Right
        self.grabber_shoot = JoystickButton(self, 5)  # Top Left
        self.grabber_high = JoystickButton(self, 6)  # Top Right

        self.lift_floor = JoystickButton(self, 7)
        self.lift_exchange = JoystickButton(self, 8)
        self.lift_switch = JoystickButton(self, 9)
        self.lift_scale_mid = JoystickButton(self, 10)
        self.lift_scale_high = JoystickButton(self, 11)


class OperatorInput:
    driver: DriverJoystick
    operator: OperatorJoystick

    def __init__(self):
        self.driver = DriverJoystick(0)
        self.operator = OperatorJoystick(1)

    def get_driver(self):
        return self.driver

    def get_operator(self):
        return self.operator

    def bind_driver(self, drive: Drivetrain, climber: Climber, lift: Lift, grabber: Grabber):
        stick = self.driver

        stick.shift_low_gear.whenPressed(ShiftToLowGear(drive))
        stick.shift_high_gear.whenPressed(ShiftToHighGear(drive))
        stick.climb.whenPressed(Climb(climber, lift, grabber))
        stick.climb.whenReleased(StopClimb(climber))
        stick.reverse_climb.whenPressed(ReverseClimb(climber))
        stick.reverse_climb.whenReleased(StopClimb(climber))

    def bind_operator(self, lift: Lift, grabber: Grabber):
        stick = self.operator

        stick.grabber_open.whenPressed(OpenGrabber(grabber))
        stick.grabber_close.whenPressed(CloseGrabber(grabber))
        stick.grabber_low.whenPressed(GrabberGoToPosition(grabber, GrabberPosition.LOW))
        stick.grabber_exchange.whenPressed(GrabberGoToPosition(grabber, GrabberPosition.EXCHANGE))
        stick.grabber_shoot.whenPressed(GrabberGoToPosition(grabber, GrabberPosition.SHOOT))
        stick.grabber_high.whenPressed(GrabberGoToPosition(grabber, GrabberPosition.HIGH))

        stick.lift_floor.whenPressed(SetLiftSetpoint(LiftHeight.FLOOR, lift))
        stick.lift_exchange.whenPressed(SetLiftSetpoint(LiftHeight.EXCHANGE, lift))
        stick.lift_switch.whenPressed(SetLiftSetpoint(LiftHeight.SWITCH, lift))
        stick.lift_scale_mid.whenPressed(SetLiftSetpoint(LiftHeight.SCALE_MID, lift))
        stick.lift_scale_high.whenPressed(SetLiftSetpoint(LiftHeight.SCALE_TOP, lift))


