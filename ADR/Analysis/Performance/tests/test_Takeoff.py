from ADR.Components.Plane import Plane
from ADR.Analysis.Performance.Takeoff import Takeoff
from ADR.parameters import get_plane_parameters, get_performance_parameters
import numpy.testing as npt
import pytest


@pytest.fixture
def plane():
    plane_parameters = get_plane_parameters()
    plane = Plane(plane_parameters)
    return plane


@pytest.fixture
def takeoff_analysis(plane):
    performance_parameters = get_performance_parameters()
    takeoff_analysis = Takeoff(plane, performance_parameters)
    return takeoff_analysis


def test_get_mtow(takeoff_analysis):
    mtow = takeoff_analysis.get_mtow()
    npt.assert_array_almost_equal(mtow, 15.5)
