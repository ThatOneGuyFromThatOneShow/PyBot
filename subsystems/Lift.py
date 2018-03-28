from wpilib.command.subsystem import Subsystem
from wpilib.doublesolenoid import DoubleSolenoid
from ctre.wpi_talonsrx import WPI_TalonSRX
from wpilib.digitalinput import DigitalInput
from subsystems.LiftHeight import LiftHeight
from robot_map import Lift as LiftMap, Compressor as CompressorMap
from wpilib.smartdashboard import SmartDashboard


class Lift(Subsystem):
    lift_motor: WPI_TalonSRX
    set_point: int
    lift_height: LiftHeight
    top_limit_switch: DigitalInput
    bottom_limit_switch: DigitalInput

    def __init__(self):
        super().__init__("Lift")

        self.lift_motor = WPI_TalonSRX(LiftMap.lift_motor_port)
        self.lift_motor.setInverted(LiftMap.lift_motor_inverted)
        self.lift_motor.configSelectedFeedbackSensor(WPI_TalonSRX.FeedbackDevice.CTRE_MagEncoder_Absolute, 0, 0)
        self.lift_motor.setSelectedSensorPosition(0, 0, 0)
        self.lift_motor.setSensorPhase(LiftMap.lift_encoder_inverted)
        self.lift_motor.setNeutralMode(WPI_TalonSRX.NeutralMode.Brake)
        self.pidf(1, 0.000002, 300, 0.025)

        self.lift_height = LiftHeight.FLOOR

        self.top_limit_switch = DigitalInput(LiftMap.lift_top_limit_port)
        self.bottom_limit_switch = DigitalInput(LiftMap.lift_bottom_limit_port)

    def get_position(self):
        return self.lift_motor.getSelectedSensorPosition(0)

    def get_top(self):
        return self.top_limit_switch.get()

    def get_bottom(self):
        return self.bottom_limit_switch.get()

    def get_set_point(self):
        return self.set_point

    def pidf(self, p, i, d, f):
        self.lift_motor.config_kP(0, p, 0)
        self.lift_motor.config_kI(0, i, 0)
        self.lift_motor.config_kD(0, d, 0)
        self.lift_motor.config_kF(0, f, 0)

    @staticmethod
    def fuzzy_equal(a, b):
        return abs(a - b) < 125

    def at_target(self):
        return self.fuzzy_equal(self.get_position(), self.get_set_point())

    def set_lift_height(self, lift_height: int or LiftHeight):
        if isinstance(lift_height, LiftHeight):
            self.lift_height = lift_height
            lift_height = lift_height.value
        self.set_point = lift_height

        if not self.get_top() and not self.get_bottom():
            self.lift_motor.set(WPI_TalonSRX.ControlMode.Position, lift_height)
        elif self.get_top() and lift_height < self.get_position():
            self.lift_motor.set(WPI_TalonSRX.ControlMode.Position, lift_height)
        elif self.get_bottom() and lift_height > self.get_position():
            self.lift_motor.set(WPI_TalonSRX.ControlMode.Position, lift_height)

    def get_lift_height(self):
        return self.lift_height

    def set_speed(self, speed):
        self.lift_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, speed)

    def check_limit_switches(self):
        if self.get_top() and self.lift_motor.get() > 0.05:
            self.set_lift_height(LiftHeight.SCALE_TOP)
        elif self.get_bottom():
            self.lift_motor.setSelectedSensorPosition(0, 0, 0)
            if self.lift_motor.get() < 0.05:
                self.set_lift_height(LiftHeight.FLOOR)

    def log(self):
        SmartDashboard.putString("Lift Height", self.lift_height.name)
        SmartDashboard.putNumber("Lift Position", self.get_position())
        SmartDashboard.putNumber("Lift Motor Speed", self.lift_motor.get())
        SmartDashboard.putBoolean("Lift Top", self.get_top())
        SmartDashboard.putBoolean("Lift Bottom", self.get_bottom())
