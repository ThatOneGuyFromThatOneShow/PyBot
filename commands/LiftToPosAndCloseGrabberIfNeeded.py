from wpilib.command.commandgroup import CommandGroup

from commands.CloseGrabber import CloseGrabber
from commands.GrabberGoToPosition import GrabberGoToPosition
from commands.SetLiftSetpoint import SetLiftSetpoint
from subsystems.Grabber import Grabber
from subsystems.GrabberPosition import GrabberPosition
from subsystems.Lift import Lift
from subsystems.LiftHeight import LiftHeight


class LiftToPosAndCloseGrabberIfNeed(CommandGroup):
    def __init__(self, lift_height: LiftHeight, lift: Lift, grabber: Grabber):
        super().__init__()

        cur_grabber_pos = grabber.get_current_grabber_position()
        cur_lift_pos = lift.get_lift_height()

        if cur_grabber_pos == GrabberPosition.HIGH:
            self.addParallel(GrabberGoToPosition(grabber, GrabberPosition.SHOOT))

        if (cur_lift_pos == LiftHeight.SCALE_TOP or cur_lift_pos == LiftHeight.SCALE_MID) and lift_height.value < LiftHeight.SCALE_MID.value:
            self.addParallel(CloseGrabber(grabber))
        elif (lift_height == LiftHeight.SCALE_MID or lift_height == LiftHeight.SCALE_TOP) and cur_lift_pos.value < LiftHeight.SCALE_MID.value:
            self.addParallel(CloseGrabber(grabber))

        self.addParallel(SetLiftSetpoint(lift_height))
