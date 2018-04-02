from wpilib.smartdashboard import SmartDashboard

from commands.AutoCommand import AutoCommand
from field.StartingPos import StartingPos
from field.Strategy import Strategy
from field.Waypoints import Waypoints
from robot_map import DashboardKeys
from subsystems.Drivetrain import Drivetrain
from subsystems.Grabber import Grabber
from subsystems.Lift import Lift


class FieldAnalyzer:
    def __init__(self, drivetrain: Drivetrain, lift: Lift, grabber: Grabber):
        self.drivetrain = drivetrain
        self.lift = lift
        self.grabber = grabber

        self.field_pos: [] = None
        self.strategy_options = {}
        self.robot_starting_pos: StartingPos = None
        self.strategy_picked_chars: [] = None
        self.picked_auto: AutoCommand = None
        self.picked_strategy: Strategy = None

    def set_field_position(self, field_position):
        self.field_pos = field_position

    def predetermine_strategy(self, auto_chooser_pos: StartingPos):
        self.robot_starting_pos = auto_chooser_pos
        strategy_string = SmartDashboard.getString(DashboardKeys.STRATEGY_FIELD, "nnnnn").lower()
        self.strategy_picked_chars = [i for i in strategy_string]
        print(strategy_string + "\n" + self.robot_starting_pos.name)

        for s in Strategy:
            if self.strategy_picked_chars[s.value] == 'y':
                points = Waypoints.WAYPOINTS[self.robot_starting_pos][s]

                auto = AutoCommand(points, s, self.drivetrain, self.lift, self.grabber)
                self.strategy_options[s] = auto
                print(s.name)

    def calculate_strategy(self):
        if self.robot_starting_pos == StartingPos.LEFT:
            self.pick_strategy('l', 'r')
        elif self.robot_starting_pos == StartingPos.RIGHT:
            self.pick_strategy('r', 'l')
        else:
            self.pick_strategy('l', 'r')
        self.picked_auto = self.strategy_options[self.picked_strategy]

    def pick_strategy(self, sameChar, oppositeChar):
        if self.field_pos[0] == sameChar and Strategy.SWITCH_SAME in self.strategy_options:
            self.picked_strategy = Strategy.SWITCH_SAME
        elif self.field_pos[1] == sameChar and Strategy.SCALE_SAME in self.strategy_options:
            self.picked_strategy = Strategy.SCALE_SAME
        elif self.field_pos[0] == oppositeChar and Strategy.SWITCH_OPPOSITE in self.strategy_options:
            self.picked_strategy = Strategy.SWITCH_OPPOSITE
        elif self.field_pos[1] == oppositeChar and Strategy.SCALE_OPPOSITE in self.strategy_options:
            self.picked_strategy = Strategy.SCALE_OPPOSITE
        else:
            self.picked_strategy = Strategy.DRIVE_FORWARD

    def get_picked_strategy(self) -> Strategy:
        return self.picked_strategy

    def run_auto(self):
        if self.picked_auto is not None:
            self.picked_auto.start()

    def stop_auto(self):
        if self.picked_auto is not None:
            self.picked_auto.cancel()
