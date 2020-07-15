from ADR.Components.Plane import Plane
from ADR.Checkers.Dimensions import Ruler
from ADR.parameters import get_plane_parameters
import numpy.testing as npt


def test_measure():
    plane_parameters = get_plane_parameters()
    plane = Plane(plane_parameters)

    plane_dimensions = Ruler(plane)
    plane_dimensions.measure()

    dimensions_check = 3.602

    npt.assert_almost_equal(
        plane_dimensions.plane.total_dimensions, dimensions_check, decimal=3
    )
    npt.assert_equal(plane_dimensions.plane.dimensions_are_good, True)
