

# ####### # Drive motor / Encoder # ####### #
class Drive:
    left_front_motor_port = 3
    left_back_motor_port = 4
    right_front_motor_port = 1
    right_back_motor_port = 2
    left_front_motor_inverted = False
    left_back_motor_inverted = False
    right_front_motor_inverted = False
    right_back_motor_inverted = False
    left_encoder_inverted = False
    right_encoder_inverted = True

    encoder_pulses_per_rev = 120 * 4  # Multiplied for 4x encoding
    gear_box_ports = [1, 0]

