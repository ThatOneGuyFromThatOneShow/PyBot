from wpilib.command.command import Command
from wpilib.joystick import Joystick

from subsystems.Lift import Lift


class LiftWithJoystick(Command):
    def __init__(self, joystick: Joystick, lift: Lift):
        super().__init__()

        self.lock_to_pos = False
        self.lift = lift
        self.joystick = joystick

        self.requires(lift)

    def execute(self):
        speed = self.calculate_speed()
        if abs(speed) > 0.05:
            if self.lift.get_top() and speed > 0:
                speed = 0
            elif self.lift.get_bottom() and speed < 0:
                speed = 0
            self.lift.set_speed(speed)
            self.lock_to_pos = True
        elif self.lock_to_pos:
            self.lift.set_lift_height(self.lift.get_position())
            self.lock_to_pos = False

    def isFinished(self):
        return False

    def calculate_speed(self):
        controller = self.joystick
        controllerY = controller.getY()
        speed = controllerY * abs(controllerY)
        throttle = 1 - (controller.getThrottle() + 1) / 2
        return -speed * throttle
