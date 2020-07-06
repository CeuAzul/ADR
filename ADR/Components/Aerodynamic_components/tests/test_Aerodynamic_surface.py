from ADR.Components.Aerodynamic_components.Aerodynamic_surface import Aerodynamic_surface
import numpy.testing as npt
import pytest


@pytest.fixture
def aerodynamic_surface():
    aerodynamic_surface_parameters = {"airfoil_clmax": 2.5, "airfoil1_name": "s1223", "airfoil2_name": "s1223",
                                      "airfoil3_name": "s1223", "span1": 2, "span2": 1.5, "chord1": 0.40, "chord2": 0.30,
                                      "chord3": 0.35, "twist1": 0, "twist2": 0, "twist3": 0, "incidence": 0, "x": 1, "z": 1}
    aerodynamic_surface = Aerodynamic_surface(aerodynamic_surface_parameters)
    return aerodynamic_surface


def test_update_alpha(aerodynamic_surface):
    aerodynamic_surface.update_alpha(20)
    new_alpha = aerodynamic_surface.attack_angle
    npt.assert_almost_equal(new_alpha, 20)


def test_get_alpha_range(aerodynamic_surface):
    x = list(range(-10, 11))
    npt.assert_array_almost_equal_nulp(
        aerodynamic_surface.get_alpha_range(), x, nulp=0)


def test_calc_MAC(aerodynamic_surface):
    npt.assert_almost_equal(aerodynamic_surface.calc_MAC(), 0.341, decimal=3)


def test_get_CL(aerodynamic_surface):
    npt.assert_almost_equal(aerodynamic_surface.get_CL(10), 2.2574, decimal=4)


def test_get_CD(aerodynamic_surface):
    npt.assert_almost_equal(aerodynamic_surface.get_CD(10), 0.0876, decimal=4)


def test_get_CM(aerodynamic_surface):
    npt.assert_almost_equal(aerodynamic_surface.get_CM(), -0.3706, decimal=4)


def test_lift(aerodynamic_surface):
    npt.assert_almost_equal(
        aerodynamic_surface.lift(1.25, 15, 10), 753.9363, decimal=4)


def test_drag(aerodynamic_surface):
    npt.assert_almost_equal(
        aerodynamic_surface.drag(1.25, 15, 10), 29.2570, decimal=4)


def test_moment(aerodynamic_surface):
    npt.assert_almost_equal(
        aerodynamic_surface.moment(1.25, 15, 10), -42.2571, decimal=4)
