from ADR.Components.References.Static_margin import SM
from ADR.Components.Aerodynamic_components.Aerodynamic_surface import (
    Aerodynamic_surface,
)
import numpy.testing as npt


def test_Static_margin():
    wing1_parameters = {
        "airfoil_clmax": 2.5,
        "airfoil1_name": "s1223",
        "airfoil2_name": "s1223",
        "airfoil3_name": "s1223",
        "span1": 2,
        "span2": 1.5,
        "chord1": 0.40,
        "chord2": 0.40,
        "chord3": 0.4,
        "twist1": 0,
        "twist2": 0,
        "twist3": 0,
        "incidence": 0,
        "x": 1,
        "z": 1,
    }

    wing2_parameters = {
        "airfoil_clmax": 2.5,
        "airfoil1_name": "s1223",
        "airfoil2_name": "s1223",
        "airfoil3_name": "s1223",
        "span1": 2,
        "span2": 1.7,
        "chord1": 0.40,
        "chord2": 0.4,
        "chord3": 0.4,
        "twist1": 0,
        "twist2": 0,
        "twist3": 0,
        "incidence": 0,
        "x": 1,
        "z": 1,
    }

    hs_parameters = {
        "airfoil_clmax": 1.5,
        "airfoil1_name": "sd7037",
        "airfoil2_name": "sd7037",
        "airfoil3_name": "sd7037",
        "span1": 0.5,
        "span2": 0.7,
        "chord1": 0.2,
        "chord2": 0.2,
        "chord3": 0.2,
        "twist1": 0,
        "twist2": 0,
        "twist3": 0,
        "incidence": 0,
        "x": 1,
        "z": 1,
    }

    plane_type = "biplane"
    wing1 = Aerodynamic_surface(wing1_parameters)
    wing1.update_alpha(7.0)
    wing2 = Aerodynamic_surface(wing2_parameters)
    wing2.update_alpha(7.0)
    hs = Aerodynamic_surface(hs_parameters)
    hs.update_alpha(7.0)

    static_margin = SM(plane_type, wing1, wing2, hs, 7.0, 0.4)
    npt.assert_almost_equal(static_margin.SM, -2.0514, decimal=4)
