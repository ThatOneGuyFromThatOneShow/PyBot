from wpilib.command.command import Command
from subsystems.drivetrain import Drivetrain
from wpilib.joystick import Joystick


class DriveWithJoystick(Command):
    drive: Drivetrain
    stick: Joystick

    def __init__(self, drivetrain: Drivetrain, joystick: Joystick):
        super().__init__("DriveWithJoystick")

        self.drive = drivetrain
        self.stick = joystick

        self.requires(drivetrain)
        self.setInterruptible(True)

    def execute(self):
        self.drive.drive_arcade(self.stick.getY(), self.stick.getZ())

    def isFinished(self):
        return False
