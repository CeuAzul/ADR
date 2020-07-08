from ADR.Components.Plane import Plane
import numpy.testing as npt
import pytest
import pandas as pd


# @pytest.fixture
def plane():
    plane_data = {"plane_type": "biplane", "wing1_x": 0, "wing1_y": 0, "wing1_z": 0,
                  "wing1_clmax_airfoil": 2.5, "wing1_airfoil1_name": "s1223", "wing1_airfoil2_name": "s1223",
                  "wing1_airfoil3_name": "s1223", "wing1_span1": 1, "wing1_span2": 1, "wing1_chord1": 0.35,
                  "wing1_chord2": 0.33, "wing1_chord3": 0.30, "wing1_twist1": 10, "wing1_twist2": 5,
                  "wing1_twist3": 3, "wing1_incidence": 1, "wing1_CM_ca": 0.08, "wing2_x": 0, "wing2_y": 0, "wing2_z": 0,
                  "wing2_clmax_airfoil": 2.8, "wing2_airfoil1_name": "s1223", "wing2_airfoil2_name": "s1223",
                  "wing2_airfoil3_name": "s1223", "wing2_span1": 1.10, "wing2_span2": 1.10, "wing2_chord1": 0.40,
                  "wing2_chord2": 0.35, "wing2_chord3": 0.33, "wing2_twist1": 5, "wing2_twist2": 3,
                  "wing2_twist3": 0, "wing2_incidence": 1, "wing2_CM_ca": 0.10, "hs_x": 0.9, "hs_y": 0, "hs_z": 0,
                  "hs_clmax_airfoil": 2.1, "hs_airfoil1_name": "SD7037", "hs_airfoil2_name": "SD7037", "hs_airfoil3_name": "SD7037",
                  "hs_span1": 0.30, "hs_span2": 0.30, "hs_chord1": 0.24, "hs_chord2": 0.24, "hs_chord3": 0.24,
                  "hs_twist1": 0, "hs_twist2": 0, "hs_twist3": 0, "hs_incidence": 0, "hs_CM_ca": 0.06,
                  "vs_x": 0.9, "vs_y": 0, "vs_z": 0.02, "vs_clmax_airfoil": 2.0, "vs_airfoil1_name": "NACA0012",
                  "vs_airfoil2_name": "NACA0012", "vs_airfoil3_name": "NACA0012", "vs_span1": 0.10, "vs_span2": 0.10,
                  "vs_chord1": 0.21, "vs_chord2": 0.18, "vs_chord3": 0.15, "vs_twist1": 0,
                  "vs_twist2": 0, "vs_twist3": 0, "vs_incidence": 0, "vs_CM_ca": 0.045, "motor_x": 0, "motor_y": 0,
                  "motor_z": 0, "static_thrust": 0, "linear_decay_coefficient": -0.15, "cg_x": 0.11, "cg_z": 0.01,
                  "tpr_x": 0.13, "tpr_z": -0.08, "Iyy_TPR": 1, "CD_tp": 1, "S_tp": 1, "CD_fus": 1, "S_fus": 1, "u_k": 1}
    plane = Plane(plane_data)
    pd.set_option('display.max_rows', None)
    print(plane.get_CL_alpha_plane())


plane()

#    return plane

# def test_get_CL_alpha_plane(plane):

#  npt.assert_almost_equal(x[0], 2.136428, decimal=6)

# def test_get_V_stall(plane):
npt.assert_almost_equal(plane.get_V_stall(1.2), 3.625, decimal=3)


# def test_get_V_CLmin(plane):
npt.assert_almost_equal(plane.get_V_CLmin(1.2), 5.405, decimal=3)
