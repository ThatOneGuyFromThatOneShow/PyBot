from pyfrc.physics import drivetrains
import math
import sys
import json
import marshal


class PhysicsEngine:
    def __init__(self, physics_controller):
        self.physics_controller = physics_controller
        self.drivetrain = drivetrains.FourMotorDrivetrain(speed=12, deadzone=drivetrains.linear_deadzone(0.1))

        self.encoder_cnst = 120 * 4 / (6 * math.pi)

        self.l_encoder = 0
        self.r_encoder = 0

        self.first = True

    def update_sim(self, hal_data, now, tm_diff):

        self.drivetrain.speed = 12 if hal_data['solenoid'][1]['value'] else 8

        lf_motor = -hal_data['CAN'][3]['value']
        lr_motor = -hal_data['CAN'][4]['value']
        rf_motor = -hal_data['CAN'][1]['value']
        rr_motor = -hal_data['CAN'][2]['value']

        speed, rotation = self.drivetrain.get_vector(lr_motor, rr_motor, lf_motor, rf_motor)
        self.physics_controller.drive(speed, rotation, tm_diff)

        # if speed > 0 and self.first:
        #     with open("jsondump.json", "w+") as f:
        #         f.write(str(hal_data))
        #         self.first = False

        # compute encoder
        left_v = int(self.drivetrain.l_speed * tm_diff * 12 / (6*math.pi) * (120*4))
        right_v = int(self.drivetrain.r_speed * tm_diff * 12 / (6*math.pi) * (120*4))

        self.l_encoder += left_v
        self.r_encoder += right_v

        hal_data['CAN'][2]["quad_position"] = self.l_encoder
        hal_data['CAN'][4]["quad_position"] = self.r_encoder
        hal_data['CAN'][2]["quad_velocity"] = int(self.drivetrain.l_speed)
        hal_data['CAN'][4]["quad_velocity"] = int(self.drivetrain.r_speed)
