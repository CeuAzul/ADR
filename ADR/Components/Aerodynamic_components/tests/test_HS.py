from ADR.Components.Aerodynamic_components.HS import HS
import numpy.testing as npt
import numpy as np
import pytest


@pytest.fixture
def horizontal_stabilizer():
    aerodynamic_surface_parameters = {
        "airfoil_clmax": 2.5,
        "airfoil1_name": "s1223",
        "airfoil2_name": "s1223",
        "airfoil3_name": "s1223",
        "span1": 2,
        "span2": 1.5,
        "chord1": 0.40,
        "chord2": 0.30,
        "chord3": 0.35,
        "twist1": 0,
        "twist2": 0,
        "twist3": 0,
        "incidence": 0,
        "x": 1,
        "z": 1,
    }
    horizontal_stabilizer = HS(aerodynamic_surface_parameters)
    return horizontal_stabilizer


def test_calc_area(horizontal_stabilizer):
    horizontal_stabilizer.calc_area()
    new_area = horizontal_stabilizer.area
    npt.assert_almost_equal(new_area, 2.375, decimal=3)


def test_update_alpha(horizontal_stabilizer):
    horizontal_stabilizer.update_alpha(15)
    new_alpha = horizontal_stabilizer.attack_angle
    npt.assert_almost_equal(new_alpha, -15)


def test_set_incidence_range(horizontal_stabilizer):
    horizontal_stabilizer.set_incidence_range(-5, 15)
    incidence_range = horizontal_stabilizer.incidence_range
    x = np.arange(-15, 26, 1)
    npt.assert_almost_equal(incidence_range, x)
