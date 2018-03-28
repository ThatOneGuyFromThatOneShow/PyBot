from wpilib.command.subsystem import Subsystem
from ctre.wpi_talonsrx import WPI_TalonSRX
from wpilib.doublesolenoid import DoubleSolenoid
from robot_map import Climber as ClimberMap, Compressor as CompressorMap


class Climber(Subsystem):
    climber_motor: WPI_TalonSRX
    motor_lock: DoubleSolenoid

    def __init__(self):
        super().__init__("Climber")

        self.climber_motor = WPI_TalonSRX(ClimberMap.climber_motor_port)
        self.climber_motor.setInverted(ClimberMap.climber_motor_inverted)
        self.climber_motor.setNeutralMode(WPI_TalonSRX.NeutralMode.Brake)

        self.motor_lock = DoubleSolenoid(CompressorMap.compressor_port, ClimberMap.climber_brake[0],
                                         ClimberMap.climber_brake[1])

    def climb(self):
        self.climber_motor.set(1)

    def reverse(self):
        self.climber_motor.set(-1)

    def stop(self):
        self.climber_motor.set(0)

    def lock(self):
        self.motor_lock.set(DoubleSolenoid.Value.kReverse)

    def release(self):
        self.motor_lock.set(DoubleSolenoid.Value.kForward)
