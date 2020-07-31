from ADR.parameters import get_plane_parameters
from ADR.Components.Plane import Plane

from ADR.Analysis.Stability.FlightStability.FlightStability import FlightStability
from ADR.Checkers.TrimmRange import TrimmRangeChecker

import numpy.testing as npt


def test_check():
    plane_parameters = get_plane_parameters()
    plane = Plane(plane_parameters)

    stability_analisys = FlightStability(plane)
    stability_analisys.trimm()

    plane_TrimmRangeChecker = TrimmRangeChecker(plane)
    plane_TrimmRangeChecker.check()

    npt.assert_almost_equal(plane.trimm_for_high_angles, True)
    npt.assert_almost_equal(plane.trimm_for_low_angles, True)
