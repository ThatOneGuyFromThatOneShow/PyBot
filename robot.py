import wpilib
from wpilib.driverstation import DriverStation
from commandbased import CommandBasedRobot

from OperatorInput import OperatorInput
from commands.DriveWIthJoystick import DriveWithJoystick
from subsystems.drivetrain import Drivetrain


class Robot(CommandBasedRobot):
    operator_input = OperatorInput
    drivetrain = Drivetrain

    def robotInit(self):
        super().robotInit()

        self.drivetrain = Drivetrain()
        self.operator_input = OperatorInput()

        # Set default commands
        self.drivetrain.setDefaultCommand(DriveWithJoystick(self.drivetrain, self.operator_input.get_driver()))

    def robotPeriodic(self):
        super().robotPeriodic()

    def autonomousInit(self):
        super().autonomousInit()

    def autonomousPeriodic(self):
        super().autonomousPeriodic()

    def teleopInit(self):
        super().teleopInit()

    def teleopPeriodic(self):
        super().teleopPeriodic()

    def disabledInit(self):
        super().disabledInit()

    def disabledPeriodic(self):
        super().disabledPeriodic()

    def testInit(self):
        super().testInit()

    def testPeriodic(self):
        super().testPeriodic()


if __name__ == "__main__":
    wpilib.run(Robot)
