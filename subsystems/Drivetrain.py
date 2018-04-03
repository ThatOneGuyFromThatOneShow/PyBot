from ctre.pigeonimu import PigeonIMU
from ctre.wpi_talonsrx import WPI_TalonSRX
from wpilib.command.subsystem import Subsystem
from wpilib.drive.differentialdrive import DifferentialDrive
from wpilib.speedcontrollergroup import SpeedControllerGroup
from wpilib.doublesolenoid import DoubleSolenoid
from wpilib.smartdashboard import SmartDashboard
from wpilib.analoggyro import AnalogGyro
import time
import hal

from robot_map import Drive as DriveMap, Compressor as CompressorMap


class Drivetrain(Subsystem):

    def __init__(self):
        super().__init__('Drivetrain')

        self.left_front_motor = WPI_TalonSRX(DriveMap.left_front_motor_port)
        self.left_back_motor = WPI_TalonSRX(DriveMap.left_back_motor_port)
        self.right_front_motor = WPI_TalonSRX(DriveMap.right_front_motor_port)
        self.right_back_motor = WPI_TalonSRX(DriveMap.right_back_motor_port)

        self.left_front_motor.setInverted(DriveMap.left_front_motor_inverted)
        self.left_back_motor.setInverted(DriveMap.left_back_motor_inverted)
        self.right_front_motor.setInverted(DriveMap.right_front_motor_inverted)
        self.right_back_motor.setInverted(DriveMap.right_back_motor_inverted)

        self.left_front_motor.setNeutralMode(WPI_TalonSRX.NeutralMode.Brake)
        self.left_back_motor.setNeutralMode(WPI_TalonSRX.NeutralMode.Brake)
        self.right_front_motor.setNeutralMode(WPI_TalonSRX.NeutralMode.Brake)
        self.right_back_motor.setNeutralMode(WPI_TalonSRX.NeutralMode.Brake)

        # Crazy people plugged the left encoder into the right side and vice versa
        self.left_back_motor.configSelectedFeedbackSensor(WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)
        self.right_back_motor.configSelectedFeedbackSensor(WPI_TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)
        self.left_back_motor.setSensorPhase(DriveMap.right_encoder_inverted)
        self.right_back_motor.setSensorPhase(DriveMap.left_encoder_inverted)

        self.left_motors = SpeedControllerGroup(self.left_front_motor, self.left_back_motor)
        self.right_motors = SpeedControllerGroup(self.right_front_motor, self.right_back_motor)

        self.drivetrain = DifferentialDrive(self.left_motors, self.right_motors)

        if not hal.isSimulation():
            self.pigeon = PigeonIMU(self.left_front_motor)
        else:
            self.pigeon = AnalogGyro(0)

        self.gear_box = DoubleSolenoid(CompressorMap.compressor_port, DriveMap.gear_box_ports[0],
                                       DriveMap.gear_box_ports[1])

        if not hal.isSimulation():
            self.gyro_reset()
        self.reset_left_encoder()
        self.reset_right_encoder()

    def drive_arcade(self, speed, turn):
        self.drivetrain.arcadeDrive(-speed, turn, False)

    def drive_tank(self, left_speed, right_speed):
        self.drivetrain.tankDrive(left_speed, right_speed, False)

    def stop(self):
        self.drivetrain.stopMotor()

    def get_left_encoder(self):
        return self.right_back_motor.getSelectedSensorPosition(0)

    def get_right_encoder(self):
        return self.left_back_motor.getSelectedSensorPosition(0)

    def get_left_velocity(self):
        return self.right_back_motor.getSelectedSensorVelocity(0)

    def get_right_velocity(self):
        return self.left_back_motor.getSelectedSensorVelocity(0)

    def reset_left_encoder(self):
        self.right_back_motor.setSelectedSensorPosition(0, 0, 0)

    def reset_right_encoder(self):
        self.left_back_motor.setSelectedSensorPosition(0, 0, 0)

    def switch_high_gear(self):
        self.gear_box.set(DoubleSolenoid.Value.kForward)

    def switch_low_gear(self):
        self.gear_box.set(DoubleSolenoid.Value.kReverse)

    def get_gear_state(self):
        return self.gear_box.get()

    def gyro_read_yaw_angle(self):
        if not hal.isSimulation():
            return self.pigeon.getYawPitchRoll()[0]
        else:
            return self.pigeon.getAngle()

    def gyro_read_yaw_rate(self):
        if not hal.isSimulation():
            return self.pigeon.getRawGyro()[0]
        else:
            return self.pigeon.getRate()

    def gyro_reset(self):
        if not hal.isSimulation():
            self.pigeon.setYaw(0, 0)
        else:
            self.pigeon.reset()

    lastTime = 0
    lastLeft, lastRight, maxLeftAcc, maxRightAcc, maxLeftJerk, maxRightJerk, maxLeftSpeed, maxRightSpeed =\
        0, 0, 0, 0, 0, 0, 0, 0

    def log(self):
        curTime = time.time() * 1000
        leftEnc = self.get_left_velocity()
        rightEnc = self.get_right_velocity()
        deltaLeft = leftEnc - self.lastLeft
        deltaRight = rightEnc - self.lastRight
        deltaTime = curTime - self.lastTime
        deltaTime = deltaTime if deltaTime != 0 else 1
        leftAcc = deltaLeft * 100 / deltaTime
        rightAcc = deltaRight * 100 / deltaTime
        leftJerk = leftAcc * 100 / deltaTime
        rightJerk = rightAcc * 100 / deltaTime
        self.lastTime = curTime
        self.lastLeft = leftEnc
        self.lastRight = rightEnc

        self.maxLeftAcc = self.maxLeftAcc if self.maxLeftAcc > leftAcc else leftAcc
        self.maxRightAcc = self.maxRightAcc if self.maxRightAcc > rightAcc else rightAcc
        self.maxLeftJerk = self.maxLeftJerk if self.maxLeftJerk > leftJerk else leftJerk
        self.maxRightJerk = self.maxRightJerk if self.maxRightJerk > rightJerk else rightJerk
        self.maxLeftSpeed = self.maxLeftSpeed if self.maxLeftSpeed > leftEnc else leftEnc
        self.maxRightSpeed = self.maxRightSpeed if self.maxRightSpeed > rightEnc else rightEnc

        SmartDashboard.putNumber("Left Acc", leftAcc)
        SmartDashboard.putNumber("Right Acc", rightAcc)
        SmartDashboard.putNumber("Left Jerk", leftJerk)
        SmartDashboard.putNumber("Right Jerk", rightJerk)
        SmartDashboard.putNumber("Left Max Acc", self.maxLeftAcc)
        SmartDashboard.putNumber("Right Max Acc", self.maxRightAcc)
        SmartDashboard.putNumber("Left Max Jerk", self.maxLeftJerk)
        SmartDashboard.putNumber("Right Max Jerk", self.maxRightJerk)
        SmartDashboard.putNumber("Max Left Speed", self.maxLeftSpeed)
        SmartDashboard.putNumber("Max Right Speed", self.maxRightSpeed)

        SmartDashboard.putNumber("Left Encoder", self.get_left_encoder())
        SmartDashboard.putNumber("Right Encoder", self.get_right_encoder())
        SmartDashboard.putNumber("Left Velocity", leftEnc)
        SmartDashboard.putNumber("Right Velocity", rightEnc)

        SmartDashboard.putNumber("Left Side Speed", self.left_motors.get())
        SmartDashboard.putNumber("Right Side Speed", self.right_motors.get())

        if not hal.isSimulation():
            SmartDashboard.putNumber("Gyro Angle", self.gyro_read_yaw_angle())
            SmartDashboard.putNumber("Gyro Rate", self.gyro_read_yaw_rate())

        SmartDashboard.putBoolean("Low Gear", self.get_gear_state() == DoubleSolenoid.Value.kReverse)
