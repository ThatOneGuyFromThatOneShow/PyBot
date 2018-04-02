from wpilib.command.command import Command

from subsystems.Drivetrain import Drivetrain


class TurnToAngle(Command):
    RAMP_UP_THRESHOLD_DISTANCE = 20
    RAMP_DOWN_THRESHOLD_DISTANCE = 45
    START_SPEED = 0.4
    END_SPEED = 0.3
    MAX_SPEED = 0.6

    def __init__(self, speed, angle, drivetrain: Drivetrain):
        super().__init__()

        self.drivetrain = drivetrain
        self.requires(drivetrain)

        self.speed = min(speed, TurnToAngle.MAX_SPEED)
        self.angle = angle
        self.start_angle = None
        print("Starting Speed: " + str(self.speed))

    def initialize(self):
        self.start_angle = self.drivetrain.gyro_read_yaw_angle()

    def execute(self):
        current_angle = self.drivetrain.gyro_read_yaw_angle()
        calc_speed = self.ramp(abs(current_angle))

        if self.speed > 0:
            self.drivetrain.drive_tank(calc_speed, -calc_speed)
        else:
            self.drivetrain.drive_tank(-calc_speed, calc_speed)

        print("Angle: " + str(current_angle) + "\n" + "Speed: " + str(calc_speed))

    def end(self):
        self.drivetrain.drive_tank(0, 0)

    def ramp(self, cur_distance):
        return self.calculate_speed(cur_distance, self.angle, TurnToAngle.RAMP_UP_THRESHOLD_DISTANCE,
                                    TurnToAngle.RAMP_DOWN_THRESHOLD_DISTANCE, abs(self.speed), TurnToAngle.START_SPEED,
                                    TurnToAngle.END_SPEED)

    @staticmethod
    def calculate_speed(current, target, ramp_up_threshold, ramp_down_threshold, max_speed, start_speed, end_speed):
        return min(min(pow(current / ramp_up_threshold, 0.75), 1) * (max_speed - start_speed) + start_speed, min(pow(
            max((target - current) / ramp_down_threshold, 0), 1.5), 1) * (max_speed - end_speed) + end_speed)
