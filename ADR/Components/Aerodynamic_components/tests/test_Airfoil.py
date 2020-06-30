from ADR.Components.Aerodynamic_components.Airfoil import Airfoil
import numpy.testing as npt
import pytest


@pytest.fixture
def airfoil():
    airfoil_data = {"airfoil_name": "s1223"}
    airfoil = Airfoil(airfoil_data)
    return airfoil


def test_get_Cl(airfoil):
    npt.assert_almost_equal(airfoil.get_Cl(3), 1.5503, decimal=4)


def test_get_Cd(airfoil):
    npt.assert_almost_equal(airfoil.get_Cd(3), 0.0214, decimal=4)


def test_get_Cm(airfoil):
    npt.assert_almost_equal(airfoil.get_Cm(3), -0.2761, decimal=4)
