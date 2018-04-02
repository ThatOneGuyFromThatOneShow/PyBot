from field.Strategy import Strategy
from field.StartingPos import StartingPos
from field.Waypoint import Waypoint


class Waypoints:
    WAYPOINTS = {}

    # LEFT POSITION
    points = {}

    points[Strategy.SWITCH_SAME] = [Waypoint(12, 0.0, 0.0), Waypoint(12, 0, -90.0)]
    points[Strategy.SCALE_SAME] = [Waypoint(25, 0.0, 0.0), Waypoint(25, -1, -90.0)]
    points[Strategy.SWITCH_OPPOSITE] = [Waypoint(18.0, 0, 0), Waypoint(18.0, -15.0, -90.0)]
    points[Strategy.SCALE_OPPOSITE] = [Waypoint(17.0, 0.0, -90.0), Waypoint(17.0, -21.0, 0),
                                       Waypoint(21.0, -18.0, 90.0)]
    points[Strategy.DRIVE_FORWARD] = [Waypoint(15, 0.0, 0.0)]

    WAYPOINTS[StartingPos.LEFT] = points

    # MIDDLE POSITION
    points = {}

    points[Strategy.SWITCH_SAME] = [Waypoint(5.75, 4, 0), Waypoint(9.25, 4, 0.0)]
    points[Strategy.SCALE_SAME] = [Waypoint(6, 10.65, 0), Waypoint(25, 10.65, 0.0),
                                   Waypoint(25, 9.65, -90.0)]
    points[Strategy.SWITCH_OPPOSITE] = [Waypoint(5.75, -2, 0), Waypoint(9.25, -2, 0.0)]
    points[Strategy.SCALE_OPPOSITE] = [Waypoint(6, -8.65, 0), Waypoint(25, -8.65, 0.0),
                                       Waypoint(25, -7.65, 90.0)]
    points[Strategy.DRIVE_FORWARD] = [Waypoint(10, 0, 0)]

    WAYPOINTS[StartingPos.MIDDLE] = points

    # RIGHT POSITION
    points = {}

    points[Strategy.SWITCH_SAME] = [Waypoint(12, 0.0, 0.0), Waypoint(12, 0, 90.0)]
    points[Strategy.SCALE_SAME] = [Waypoint(25, -0.5, 0.0), Waypoint(25, -0.5, 90.0)]
    points[Strategy.SWITCH_OPPOSITE] = [Waypoint(18.0, 0, 0), Waypoint(18, 19.0, 90.0),
                                        Waypoint(13.0, 19.0, -90), Waypoint(13.0, 19.0, -90)]
    points[Strategy.SCALE_OPPOSITE] = [Waypoint(18.0, 0.0, 90.0), Waypoint(18.0, 21.0, 0),
                                       Waypoint(21.0, 18.0, -90.0)]
    points[Strategy.DRIVE_FORWARD] = [Waypoint(15, 0.0, 0.0)]

    WAYPOINTS[StartingPos.RIGHT] = points
