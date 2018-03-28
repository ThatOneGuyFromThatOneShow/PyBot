from wpilib.command.command import Command
from wpilib.joystick import Joystick
from subsystems.Grabber import Grabber


class GrabberMoveWithPOV(Command):
    GRABBER_SPEED_UP = 0.7
    GRABBER_SPEED_DOWN = -0.4
    first_stop = False
    grabber: Grabber
    joystick: Joystick

    def __init__(self, grabber: Grabber, joystick: Joystick):
        super().__init__("GrabberMoveWithPOV")

        self.grabber = grabber
        self.joystick = joystick

        self.requires(grabber)
        self.setInterruptible(True)

    def execute(self):
        pov = self.joystick.getPOV()
        if pov == 0:
            self.grabber.set_speed(self.GRABBER_SPEED_UP)
            self.first_stop = True
        elif pov == 180:
            self.grabber.set_speed(self.GRABBER_SPEED_DOWN)
            self.first_stop = True
        elif self.first_stop:
            self.first_stop = False
            self.grabber.set_speed(0.1)
            self.grabber.go_to_set_point(self.grabber.get_current_position())

    def isFinished(self):
        return False
