from ADR.Components.Aerodynamic_components.Airfoil import *
import numpy.testing as npt


def test_get_Cl():
    aircraft_airfoil_data = {"airfoil_name": "s1223"}
    aircraft_Coefficients = Airfoil(aircraft_airfoil_data)
    npt.assert_almost_equal(aircraft_Coefficients.get_Cl(3), 1.5503, decimal=4)


def test_get_Cd():
    aircraft_airfoil_data = {"airfoil_name": "s1223"}
    aircraft_Coefficients = Airfoil(aircraft_airfoil_data)
    npt.assert_almost_equal(aircraft_Coefficients.get_Cd(3), 0.0214, decimal=4)


def test_get_Cm():
    aircraft_airfoil_data = {"airfoil_name": "s1223"}
    aircraft_Coefficients = Airfoil(aircraft_airfoil_data)
    npt.assert_almost_equal(aircraft_Coefficients.get_Cm(3), -0.2761, decimal=4)
