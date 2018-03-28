from wpilib.command.subsystem import Subsystem
from wpilib.doublesolenoid import DoubleSolenoid
from ctre.wpi_talonsrx import WPI_TalonSRX
from wpilib.analoginput import AnalogInput
from subsystems.GrabberPosition import GrabberPosition
from robot_map import Grabber as GrabberMap, Compressor as CompressorMap
from wpilib.smartdashboard import SmartDashboard


class Grabber(Subsystem):
    NORMAL_MOVE_SPEED = 0.5
    open: bool
    pneumatic: DoubleSolenoid
    grabber_motor: WPI_TalonSRX
    distance: AnalogInput
    set_point: int
    auto_grab: bool
    grabber_position: GrabberPosition

    def __init__(self):
        super().__init__("Grabber")

        self.pneumatic = DoubleSolenoid(CompressorMap.compressor_port, GrabberMap.grabber_ports[0],
                                        GrabberMap.grabber_ports[1])
        self.grabber_motor = WPI_TalonSRX(GrabberMap.grabber_motor_port)
        self.grabber_motor.setInverted(GrabberMap.grabber_motor_inverted)
        self.grabber_motor.configSelectedFeedbackSensor(WPI_TalonSRX.FeedbackDevice.CTRE_MagEncoder_Relative, 0, 0)
        self.grabber_motor.setSensorPhase(GrabberMap.grabber_encoder_inverted)
        self.grabber_motor.setNeutralMode(WPI_TalonSRX.NeutralMode.Brake)
        self.grabber_motor.setSelectedSensorPosition(0, 0, 0)

        self.grabber_motor.configMaxIntegralAccumulator(0, 0, 0)
        self.pidf(0.6, 0.000003, 240, 0.025)

        self.distance = AnalogInput(GrabberMap.distance_sensor_port)

        self.auto_grab = True
        self.grabber_position = GrabberPosition.HIGH
        self.set_point = 0
        self.open = self.pneumatic.get() == DoubleSolenoid.Value.kForward

    def pidf(self, p, i, d, f):
        self.grabber_motor.config_kP(0, p, 0)
        self.grabber_motor.config_kI(0, i, 0)
        self.grabber_motor.config_kD(0, d, 0)
        self.grabber_motor.config_kF(0, f, 0)

    def get_distance(self):
        return (self.distance.getVoltage() * 60) + 50

    def calculate(self):
        if self.auto_grab and self.open and self.get_distance() < 75:
            self.capture_cube()
            self.auto_grab = False
        elif self.get_distance() > 180:
            self.auto_grab = True

    @staticmethod
    def fuzzy_equal(a, b) -> bool:
        return abs(a - b) < 250

    def reset(self):
        self.grabber_motor.setSelectedSensorPosition(0, 0, 0)

    def get_set_point(self):
        return self.set_point

    def capture_cube(self):
        self.pneumatic.set(DoubleSolenoid.Value.kReverse)
        self.open = False

    def release_cube(self):
        self.pneumatic.set(DoubleSolenoid.Value.kForward)
        self.open = True

    def go_to_set_point(self, set_point: int or GrabberPosition) -> None:
        if isinstance(set_point, GrabberPosition):
            self.grabber_position = set_point
            set_point = set_point.value
        self.grabber_motor.set(WPI_TalonSRX.ControlMode.Position, set_point)

    def set_speed(self, speed):
        self.grabber_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, speed)

    def get_current_grabber_position(self) -> GrabberPosition:
        return self.grabber_position

    def get_current_position(self) -> int:
        return self.grabber_motor.getSelectedSensorPosition(0)

    def at_target_position(self) -> bool:
        return self.fuzzy_equal(self.set_point, self.get_current_position())

    def log(self):
        SmartDashboard.putBoolean("Grabber Open", self.open)
        SmartDashboard.putNumber("Grabber Current Position", self.get_current_position())
        SmartDashboard.putNumber("Grabber Speed", self.grabber_motor.get())
        SmartDashboard.putString("Grabber Distance", str(self.get_distance()))
        SmartDashboard.putString("Grabber Position", self.get_current_grabber_position().name)
