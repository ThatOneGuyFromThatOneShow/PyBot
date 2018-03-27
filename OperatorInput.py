from wpilib.joystick import Joystick
from wpilib.buttons import JoystickButton


class OperatorInput:
    driver: Joystick
    operator: Joystick

    def __init__(self):
        self.driver = self._create_driver_controller()
        self.operator = self._create_operator_controller()

    @staticmethod
    def _create_operator_controller():
        joystick = Joystick(1)

        grabber_open = JoystickButton(joystick, 1)  # Trigger
        grabber_close = JoystickButton(joystick, 2)  # Thumb
        grabber_low = JoystickButton(joystick, 3)  # Bottom Left
        grabber_exchange = JoystickButton(joystick, 4)  # Bottom Right
        grabber_shoot = JoystickButton(joystick, 5)  # Top Left
        grabber_high = JoystickButton(joystick, 6)  # Top Right

        lift_floor = JoystickButton(joystick, 7)
        lift_excahnge = JoystickButton(joystick, 8)
        lift_switch = JoystickButton(joystick, 9)
        lift_scale_mid = JoystickButton(joystick, 10)
        lift_scale_high = JoystickButton(joystick, 11)

        return joystick

    @staticmethod
    def _create_driver_controller():
        joystick = Joystick(0)

        shift_low_gear = JoystickButton(joystick, 1)
        shift_high_gear = JoystickButton(joystick, 2)
        climb = JoystickButton(joystick, 3)
        reverse_climb = JoystickButton(joystick, 4)

        return joystick

    def get_driver(self):
        return self.driver

    def get_operator(self):
        return self.operator


