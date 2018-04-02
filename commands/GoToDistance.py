import math
import time

from wpilib.command.command import Command

from subsystems.Drivetrain import Drivetrain


class GoToDistance(Command):
    FEET_TO_ENCODER_COUNTS = 12 / (math.pi*6) * 480
    RAMP_UP_THRESHOLD_DISTANCE = 5 * FEET_TO_ENCODER_COUNTS
    RAMP_DOWN_THRESHOLD_DISTANCE = 5 * FEET_TO_ENCODER_COUNTS
    START_SPEED = 0.35
    END_SPEED = 0.2

    def __init__(self, speed, distance, drivetrain: Drivetrain):
        super().__init__()

        self.drivetrain = drivetrain
        self.requires(drivetrain)

        self.speed = speed
        self.distance = distance * GoToDistance.FEET_TO_ENCODER_COUNTS
        self.left_start = None
        self.right_start = None
        self.start_angle = None
        self.last_move = None

        print("Distance: " + distance)

    def initialize(self):
        self.start_angle = self.drivetrain.gyro_read_yaw_angle()
        self.left_start = self.drivetrain.get_left_encoder()
        self.right_start = self.drivetrain.get_right_encoder()
        self.last_move = time.time()

    def execute(self):
        angle_dif = self.start_angle - self.drivetrain.gyro_read_yaw_angle()
        correction = angle_dif / 50
        cur_distance = (self.drivetrain.get_left_encoder() - self.left_start +
                        self.drivetrain.get_right_encoder() - self.right_start) / 2
        calc_speed = max(self.ramp(abs(cur_distance)), 0)

        self.drivetrain.drive_tank(calc_speed - correction, calc_speed + correction)

        if abs((self.drivetrain.get_left_velocity() + self.drivetrain.get_right_velocity()) / 2) > 20:
            self.last_move = time.time()

        print("Speed: " + calc_speed + "\nCurrent Distance: " + cur_distance)

    def isFinished(self):
        cur_distance = (self.drivetrain.get_left_encoder() - self.left_start +
                        self.drivetrain.get_right_encoder() - self.right_start) / 2
        return (abs(cur_distance) >= self.distance) or (time.time() - self.last_move > 1000)

    def end(self):
        self.drivetrain.drive_tank(0, 0)

    def ramp(self, cur_distance):
        return self.calculate_speed(cur_distance, self.distance, GoToDistance.RAMP_UP_THRESHOLD_DISTANCE,
                                    GoToDistance.RAMP_DOWN_THRESHOLD_DISTANCE, abs(self.speed), GoToDistance.START_SPEED,
                                    GoToDistance.END_SPEED)

    @staticmethod
    def calculate_speed(current, target, ramp_up_threshold, ramp_down_threshold, max_speed, start_speed, end_speed):
        return min(min(pow(current / ramp_up_threshold, 0.75), 1) * (max_speed - start_speed) + start_speed, min(pow(
            max((target - current) / ramp_down_threshold, 0), 1.5), 1) * (max_speed - end_speed) + end_speed)
