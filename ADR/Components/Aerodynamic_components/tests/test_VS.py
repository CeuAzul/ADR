from ADR.Components.Aerodynamic_components.HS import HS
import numpy.testing as npt
import pytest


@pytest.fixture
def aerodynamic_surface():
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
    aerodynamic_surface = HS(aerodynamic_surface_parameters)
    return aerodynamic_surface


def test_calc_area(aerodynamic_surface):
    aerodynamic_surface.calc_area()
    new_area = aerodynamic_surface.area
    npt.assert_almost_equal(new_area, 2.375, decimal=3)
