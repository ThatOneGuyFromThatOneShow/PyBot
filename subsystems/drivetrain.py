from wpilib.command.subsystem import Subsystem
from wpilib.speedcontrollergroup import SpeedControllerGroup
from ctre.pigeonimu import PigeonIMU
from ctre.wpi_talonsrx import WPI_TalonSRX
from robot_map import Drive as DriveMap
from wpilib.drive.differentialdrive import DifferentialDrive
import commands.DriveWIthJoystick


class Drivetrain(Subsystem):
    pigeon: PigeonIMU
    left_front_motor: WPI_TalonSRX
    left_back_motor: WPI_TalonSRX
    right_front_motor: WPI_TalonSRX
    right_back_motor: WPI_TalonSRX
    left_motors: SpeedControllerGroup
    right_motors: SpeedControllerGroup
    drivetrain: DifferentialDrive

    def __init__(self):
        super().__init__('Drivetrain')

        self.left_front_motor = WPI_TalonSRX(DriveMap.left_front_motor_port)
        self.left_back_motor = WPI_TalonSRX(DriveMap.left_back_motor_port)
        self.right_front_motor = WPI_TalonSRX(DriveMap.right_front_motor_port)
        self.right_back_motor = WPI_TalonSRX(DriveMap.right_back_motor_port)

        self.left_front_motor.setSensorPhase(DriveMap.left_front_motor_inverted)
        self.left_back_motor.setSensorPhase(DriveMap.left_back_motor_inverted)
        self.right_front_motor.setSensorPhase(DriveMap.right_front_motor_inverted)
        self.right_back_motor.setSensorPhase(DriveMap.right_back_motor_inverted)

        self.left_motors = SpeedControllerGroup(self.left_front_motor, self.left_back_motor)
        self.right_motors = SpeedControllerGroup(self.right_front_motor, self.right_back_motor)

        self.drivetrain = DifferentialDrive(self.left_motors, self.right_motors)

        self.pigeon = PigeonIMU(self.left_front_motor)

    def initDefaultCommand(self):
        self.setDefaultCommand(Dri)

    def drive_arcade(self, speed, turn):
        self.drivetrain.arcadeDrive(speed, turn, False)

    def drive_tank(self, left_speed, right_speed):
        self.drivetrain.tankDrive(left_speed, right_speed, False)
