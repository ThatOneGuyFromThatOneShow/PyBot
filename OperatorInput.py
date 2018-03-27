from wpilib.joystick import Joystick
from wpilib.buttons import JoystickButton


class DriverController(Joystick):
    def __init__(self, port):
        super().__init__(port)

        shift_low_gear = JoystickButton(self, 1)
        shift_high_gear = JoystickButton(self, 2)
        climb = JoystickButton(self, 3)
        reverse_climb = JoystickButton(self, 4)


class OperaterController(Joystick):
    def __init__(self, port):
        super().__init__(port)

        grabber_open = JoystickButton(self, 1)  # Trigger
        grabber_close = JoystickButton(self, 2)  # Thumb
        grabber_low = JoystickButton(self, 3)  # Bottom Left
        grabber_exchange = JoystickButton(self, 4)  # Bottom Right
        grabber_shoot = JoystickButton(self, 5)  # Top Left
        grabber_high = JoystickButton(self, 6)  # Top Right

        lift_floor = JoystickButton(self, 7)
        lift_excahnge = JoystickButton(self, 8)
        lift_switch = JoystickButton(self, 9)
        lift_scale_mid = JoystickButton(self, 10)
        lift_scale_high = JoystickButton(self, 11)


class OperatorInput:
    driver: DriverController
    operator: OperaterController

    def __init__(self):
        self.driver = DriverController(0)
        self.operator = OperaterController(1)

    def get_driver_joystick(self):
        return self.driver

    def get_operator_joystick(self):
        return self.operator


