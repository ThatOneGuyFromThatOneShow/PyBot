

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


class Compressor:
    compressor_port = 0


class Climber:
    climber_motor_port = 9
    climber_motor_inverted = True
    climber_brake = [7, 6]


class Grabber:
    grabber_ports = [2, 3]
    grabber_motor_port = 7
    grabber_motor_inverted = True
    grabber_encoder_inverted = False
    distance_sensor_port = 1


class Lift:
    lift_motor_port = 5
    lift_motor_inverted = False
    lift_encoder_inverted = True
    lift_top_limit_port = 0
    lift_bottom_limit_port = 1


class Controllers:
    driver_controller_port = 0
    operator_controller_port = 1


class DashboardKeys:
    POSITION_SELECTION = "Position Selection"
    RESET_SUBSYSTEMS_IN_TELEOP = "TeleOp Reset"
    SET_LIFT_SWITCH = "Set - Lift Switch"
    SET_LIFT_EXCHANGE = "Set - Lift Exchange"
    SET_LIFT_SCALE_TOP = "Set - Lift Scale Top"
    SET_LIFT_SCALE_MID = "Set - Lift Scale Mid"
    SET_LIFT_FLOOR = "Set - Lift Floor"
    SET_GRABBER_POSITION_HIGH = "Set - Grabber Position High"
    SET_GRABBER_POSITION_SHOOT = "Set - Grabber Position Shoot"
    SET_GRABBER_POSITION_EXCHANGE = "Set - Grabber Position Exchange"
    SET_GRABBER_POSITION_LOW = "Set - Grabber Position Low"
    SET_GRABBER_CLOSE = "Set - Grabber Close"
    SUBMIT = "Submit"
    STRATEGY_FIELD = "Strategy Field"
    SET_GRABBER_OPEN = "Set - Grabber Open"
