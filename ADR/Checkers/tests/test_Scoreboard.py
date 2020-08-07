from ADR.parameters import get_plane_parameters
from ADR.Components.Plane import Plane

from ADR.Analysis.Stability.FlightStability.FlightStability import FlightStability
from ADR.Checkers.Scoreboard import MaybeAnAssassin

import numpy.testing as npt


def test_score_or_kill():
    plane_parameters = get_plane_parameters()
    plane = Plane(plane_parameters)

    stability_analisys = FlightStability(plane)
    stability_analisys.trimm()

    plane_scoreboard = MaybeAnAssassin(plane)
    plane_scoreboard.score_or_kill()

    npt.assert_almost_equal(plane_scoreboard.plane.dead, True)
    npt.assert_almost_equal(plane_scoreboard.plane.payload, 0)
