from ADR.Components.Aerodynamic_components.Aerodynamic_surface import (
    Aerodynamic_surface,
)
from ADR.Components.Points.CG import CG
import numpy.testing as npt
import pytest


def test_moment_on_CG():
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

    aerodynamic_surface = Aerodynamic_surface(aerodynamic_surface_parameters)

    plane_alpha = 3.0
    aerodynamic_surface.update_alpha(plane_alpha)

    cg_parameters = {"x": 0.15, "y": 0.7, "z": 0.2}
    cg = CG(cg_parameters)

    npt.assert_almost_equal(
        aerodynamic_surface.moment_on_CG(aerodynamic_surface, cg, plane_alpha),
        -0.37,
        decimal=2,
    )
