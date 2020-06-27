from ADR.Components.Aerodynamic_components.Aerodynamic_section import Aerodynamic_section
import numpy.testing as npt


def test_Aerodynamics_section():
    airfoil_parameters = {"airfoil1_name": "s1223", "airfoil2_name": "s1223",
                          "span": 2, "chord1": 0.40, "chord2": 0.35, "twist1": 0, "twist2": 0}
    aerodynamic_section = Aerodynamic_section(airfoil_parameters)
    npt.assert_almost_equal(aerodynamic_section.calc_area(), 0.75, decimal=2)
    npt.assert_almost_equal(aerodynamic_section.calc_MAC(), 0.376, decimal=3)
