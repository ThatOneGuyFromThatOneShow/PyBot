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

    def bind_driver(self, drive: Drivetrain, climber: Climber):
        stick = self.driver

        # stick.shift_low_gear.whenPressed()
        # stick.shift_high_gear.whenPressed()
        # stick.climb.whenPressed()
        # stick.reverse_climb.whenPressed()

    def bind_operator(self, lift: Lift, grabber: Grabber):
        stick = self.operator

        stick.grabber_open.whenPressed(OpenGrabber(grabber))
        stick.grabber_close.whenPressed(CloseGrabber(grabber))
        stick.grabber_low.whenPressed(GrabberGoToPosition(grabber, GrabberPosition.LOW))
        stick.grabber_exchange.whenPressed(GrabberGoToPosition(grabber, GrabberPosition.EXCHANGE))
        stick.grabber_shoot.whenPressed(GrabberGoToPosition(grabber, GrabberPosition.SHOOT))
        stick.grabber_high.whenPressed(GrabberGoToPosition(grabber, GrabberPosition.HIGH))

        # TODO bind lift
        # stick.lift_floor.whenPressed()
        # stick.lift_exchange.whenPressed()
        # stick.lift_switch.whenPressed()
        # stick.lift_scale_mid.whenPressed()
        # stick.lift_scale_high.whenPressed()


