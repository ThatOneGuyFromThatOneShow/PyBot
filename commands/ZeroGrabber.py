from subsystems.GrabberPosition import GrabberPosition
from wpilib.command.commandgroup import CommandGroup
from commands.GrabberMoveSpeed import GrabberMoveSpeed
from commands.Wait import Wait
from commands.ResetGrabber import ResetGrabber
from commands.GrabberGoToPosition import GrabberGoToPosition
from subsystems.Grabber import Grabber


class ZeroGrabber(CommandGroup):
    def __init__(self, grabber: Grabber):
        super().__init__()
        self.addSequential(GrabberMoveSpeed(grabber, -0.5))
        self.addSequential(Wait(1000))
        self.addSequential(ResetGrabber(grabber))
        self.addSequential(GrabberGoToPosition(grabber, GrabberPosition.HIGH))
