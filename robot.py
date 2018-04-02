import wpilib
from commandbased import CommandBasedRobot
from wpilib.cameraserver import CameraServer
from wpilib.command.instantcommand import InstantCommand
from wpilib.compressor import Compressor
from wpilib.driverstation import DriverStation
from wpilib.sendablechooser import SendableChooser
from wpilib.smartdashboard import SmartDashboard

from OperatorInput import OperatorInput
from commands.CloseGrabber import CloseGrabber
from commands.DriveWIthJoystick import DriveWithJoystick
from commands.GrabberGoToPosition import GrabberGoToPosition
from commands.GrabberMoveWithPOV import GrabberMoveWithPOV
from commands.LiftWithJoystick import LiftWithJoystick
from commands.OpenGrabber import OpenGrabber
from commands.SetLiftSetpoint import SetLiftSetpoint
from commands.ZeroGrabber import ZeroGrabber
from field.FieldAnalyzer import FieldAnalyzer
from field.StartingPos import StartingPos
from robot_map import Compressor as CompressorMap
from robot_map import DashboardKeys
from subsystems.Climber import Climber
from subsystems.Drivetrain import Drivetrain
from subsystems.Grabber import Grabber
from subsystems.GrabberPosition import GrabberPosition
from subsystems.Lift import Lift
from subsystems.LiftHeight import LiftHeight


class Robot(CommandBasedRobot):
    def __init__(self):
        super().__init__()

        self.operator_input: OperatorInput = None
        self.drivetrain: Drivetrain = None
        self.grabber: Grabber = None
        self.lift: Lift = None
        self.climber: Climber = None
        self.field_analyzer: FieldAnalyzer = None
        self.compressor: Compressor = None
        self.auto_chooser_pos = SendableChooser()

    def robotInit(self):
        super().robotInit()

        self.drivetrain = Drivetrain()
        self.grabber = Grabber()
        self.lift = Lift()
        self.climber = Climber()

        self.compressor = Compressor(CompressorMap.compressor_port)
        self.compressor.setClosedLoopControl(True)
        self.compressor.start()

        self.operator_input = OperatorInput()
        self.operator_input.bind_driver(self.drivetrain, self.climber, self.lift, self.grabber)
        self.operator_input.bind_operator(self.lift, self.grabber)

        self.field_analyzer = FieldAnalyzer(self.drivetrain, self.lift, self.grabber)

        # Set default commands
        self.drivetrain.setDefaultCommand(DriveWithJoystick(self.drivetrain, self.operator_input.get_driver()))
        self.grabber.setDefaultCommand(GrabberMoveWithPOV(self.grabber, self.operator_input.get_operator()))
        self.lift.setDefaultCommand(LiftWithJoystick(self.operator_input.get_operator(), self.lift))

        # Init subsystem
        self.grabber.go_to_set_point(GrabberPosition.HIGH)
        self.grabber.capture_cube()
        self.lift.set_lift_height(LiftHeight.FLOOR)

        # Start camera server
        CameraServer.launch()

        # Init Dashboard fields
        SmartDashboard.putString(DashboardKeys.STRATEGY_FIELD, "nnnnn")
        SmartDashboard.putBoolean(DashboardKeys.SUBMIT, False)

        SmartDashboard.putBoolean(DashboardKeys.RESET_SUBSYSTEMS_IN_TELEOP, False)

        # SmartDashboard.putNumber("Grabber Pro", 0)
        # SmartDashboard.putNumber("Grabber I", 0)
        # SmartDashboard.putNumber("Grabber D", 0)
        # SmartDashboard.putNumber("Grabber F", 0)

        # Create robot position selector
        self.auto_chooser_pos.addObject(StartingPos.LEFT.name, StartingPos.LEFT)
        self.auto_chooser_pos.addDefault(StartingPos.MIDDLE.name, StartingPos.MIDDLE)
        self.auto_chooser_pos.addObject(StartingPos.RIGHT.name, StartingPos.RIGHT)

        SmartDashboard.putData(DashboardKeys.POSITION_SELECTION, self.auto_chooser_pos)

        # Create Testing Commands
        SmartDashboard.putData(DashboardKeys.SET_GRABBER_OPEN, OpenGrabber(self.grabber))
        SmartDashboard.putData(DashboardKeys.SET_GRABBER_CLOSE, CloseGrabber(self.grabber))
        SmartDashboard.putData(DashboardKeys.SET_GRABBER_POSITION_LOW, GrabberGoToPosition(self.grabber, GrabberPosition.LOW))
        SmartDashboard.putData(DashboardKeys.SET_GRABBER_POSITION_EXCHANGE, GrabberGoToPosition(self.grabber, GrabberPosition.EXCHANGE))
        SmartDashboard.putData(DashboardKeys.SET_GRABBER_POSITION_SHOOT, GrabberGoToPosition(self.grabber, GrabberPosition.SHOOT))
        SmartDashboard.putData(DashboardKeys.SET_GRABBER_POSITION_HIGH, GrabberGoToPosition(self.grabber, GrabberPosition.HIGH))
        SmartDashboard.putData(DashboardKeys.SET_LIFT_FLOOR, SetLiftSetpoint(LiftHeight.FLOOR, self.lift))
        SmartDashboard.putData(DashboardKeys.SET_LIFT_SCALE_MID, SetLiftSetpoint(LiftHeight.SCALE_MID, self.lift))
        SmartDashboard.putData(DashboardKeys.SET_LIFT_SCALE_TOP, SetLiftSetpoint(LiftHeight.SCALE_TOP, self.lift))
        SmartDashboard.putData(DashboardKeys.SET_LIFT_EXCHANGE, SetLiftSetpoint(LiftHeight.EXCHANGE, self.lift))
        SmartDashboard.putData(DashboardKeys.SET_LIFT_SWITCH, SetLiftSetpoint(LiftHeight.SWITCH, self.lift))

        comm = InstantCommand()
        comm.initialize = lambda: self.grabber.reset()
        SmartDashboard.putData("Reset Grabber Enc", comm)

    def robotPeriodic(self):
        super().robotPeriodic()

        self.lift.check_limit_switches()

        # p = SmartDashboard.getNumber("Grabber Pro", 0)
        # i = SmartDashboard.getNumber("Grabber I", 0)
        # d = SmartDashboard.getNumber("Grabber D", 0)
        # f = SmartDashboard.getNumber("Grabber F", 0)
        # self.lift.pidf(p, i, d, f)

        self.log()

    def autonomousInit(self):
        super().autonomousInit()

        # Init subsystems for autonomous
        self.compressor.start()
        self.drivetrain.switch_low_gear()
        self.grabber.capture_cube()

        # Analyze the field and pick auto
        field_pos = [char for char in DriverStation.getInstance().getGameSpecificMessage().upper()]
        self.field_analyzer.set_field_position(field_pos)
        self.field_analyzer.calculate_strategy()
        self.field_analyzer.run_auto()

        # Print the auto to the Dashboard
        SmartDashboard.putString("Autonomous Strategy", self.field_analyzer.get_picked_strategy().name)

    def autonomousPeriodic(self):
        super().autonomousPeriodic()

    def teleopInit(self):
        super().teleopInit()

        # Stop any running autonomous commands
        self.field_analyzer.stop_auto()

        # Init subsystems for TeleOp
        self.drivetrain.switch_high_gear()
        self.compressor.start()

        # Reset grabber and lift
        if SmartDashboard.getBoolean(DashboardKeys.RESET_SUBSYSTEMS_IN_TELEOP, False):
            ZeroGrabber(self.grabber).start()
            SetLiftSetpoint(LiftHeight.FLOOR, self.lift).start()

    def teleopPeriodic(self):
        super().teleopPeriodic()

        self.grabber.calculate()

    def disabledInit(self):
        super().disabledInit()

    def disabledPeriodic(self):
        super().disabledPeriodic()

        if SmartDashboard.getBoolean(DashboardKeys.SUBMIT, False):
            self.field_analyzer.predetermine_strategy(self.auto_chooser_pos.getSelected())
            SmartDashboard.putBoolean(DashboardKeys.SUBMIT, False)

        self.log()

    def testInit(self):
        SmartDashboard.putNumber("Set - Left Speed", 0)
        SmartDashboard.putNumber("Set - Right Speed", 0)
        SmartDashboard.putNumber("Set - Lift Speed", 0)
        SmartDashboard.putNumber("Set - Climber Speed", 0)
        SmartDashboard.putNumber("Set - Grabber Rotation Speed", 0)
        SmartDashboard.putBoolean("Set - Grabber Lock", False)

    def testPeriodic(self):
        super().testPeriodic()

        lift_speed = SmartDashboard.getNumber("Set - Lift Speed", 0)
        self.lift.set_speed(lift_speed)

        grabber_speed = SmartDashboard.getNumber("Set - Grabber Rotation Speed", 0)
        self.grabber.set_speed(grabber_speed)

        climber_speed = SmartDashboard.getNumber("Set - Climber Speed", 0)
        if climber_speed > 0:
            self.climber.climb()
        elif climber_speed < 0:
            self.climber.reverse()
        else:
            self.climber.stop()

        grabber_lock = SmartDashboard.getBoolean("Set - Grabber Lock", false)
        if grabber_lock:
            self.climber.lock()
        else:
            self.climber.release()

        left_speed = SmartDashboard.getNumber("Set - Left Speed", 0)
        right_speed = SmartDashboard.getNumber("Set - Right Speed", 0)
        self.drivetrain.drive_tank(left_speed, right_speed)

    def log(self):
        # Log subsystem values
        self.drivetrain.log()
        self.grabber.log()
        self.lift.log()

        # Print compressor switch to the Dashboard
        SmartDashboard.putBoolean("Low Pressure", self.compressor.getPressureSwitchValue())


if __name__ == "__main__":
    wpilib.run(Robot)
