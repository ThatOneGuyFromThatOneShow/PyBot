import wpilib
from commandbased import CommandBasedRobot

from OperatorInput import OperatorInput
from commands.DriveWIthJoystick import DriveWithJoystick
from subsystems.Drivetrain import Drivetrain
from subsystems.Grabber import Grabber
from subsystems.Lift import Lift
from subsystems.LiftHeight import LiftHeight
from subsystems.Climber import Climber


class Robot(CommandBasedRobot):
    operator_input = OperatorInput
    drivetrain = Drivetrain
    grabber = Grabber
    lift = Lift
    climber = Climber

    def robotInit(self):
        super().robotInit()

        self.drivetrain = Drivetrain()
        self.grabber = Grabber()
        self.lift = Lift()
        self.climber = Climber()
        self.operator_input = OperatorInput()
        self.operator_input.bind_driver(self.drivetrain, self.climber)
        self.operator_input.bind_operator(self.lift, self.grabber)

        # Set default commands
        self.drivetrain.setDefaultCommand(DriveWithJoystick(self.drivetrain, self.operator_input.get_driver()))
        # self.grabber.setDefaultCommand()
        # self.lift.setDefaultCommand()

        # Init subsystem
        self.grabber.release_cube()
        self.lift.set_lift_height(LiftHeight.FLOOR)

    def robotPeriodic(self):
        super().robotPeriodic()

        self.drivetrain.log()
        self.grabber.log()
        self.lift.log()

    def autonomousInit(self):
        super().autonomousInit()

    def autonomousPeriodic(self):
        super().autonomousPeriodic()

    def teleopInit(self):
        super().teleopInit()

        self.drivetrain.switch_high_gear()

    def teleopPeriodic(self):
        super().teleopPeriodic()

        self.grabber.calculate()

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
