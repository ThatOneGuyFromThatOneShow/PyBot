import wpilib
from wpilib.command import Command
from commandbased import CommandBasedRobot


class Robot(CommandBasedRobot):

    def robotInit(self):
        super().robotInit()

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
    wpilib.run(Robot())
