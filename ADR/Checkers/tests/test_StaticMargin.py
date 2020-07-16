from ADR.Checkers.StaticMargin import StaticMarginChecker
from ADR.Analysis.Stability.FlightStability.FlightStability import FlightStability
from ADR.parameters import get_plane_parameters
from ADR.Components.Plane import Plane
import numpy.testing as npt


def test_check():
    plane_parameters = get_plane_parameters()
    plane = Plane(plane_parameters)

    stability_analisys = FlightStability(plane)
    stability_analisys.static_margin()

    plane_SMChecker = StaticMarginChecker(plane)
    plane_SMChecker.check()

    npt.assert_almost_equal(plane_SMChecker.plane.positive_sm_for_positive_alphas, True)
