import numpy.testing as npt
from ADR.Components.Component import Component


def test_Component():

    component_parameters = {"x": 1, "y": 2, "z": 3}

    component_test = Component(component_parameters)

    if component_test.x == 1 and component_test.y == 2 and component_test.z == 3:
        check_test = 1

    npt.assert_almost_equal(check_test, 1)
