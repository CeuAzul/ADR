from ADR.Components.Plane import Plane
from ADR.Core.data_manipulation import dict_to_dataframe
import numpy.testing as npt
import pytest
import pandas as pd


@pytest.fixture
def plane():
    plane_data = {"plane_type": "biplane",
                  "wing1_x": 0,
                  "wing1_y": 0,
                  "wing1_z": 0,
                  "wing1_clmax_airfoil": 2.5,
                  "wing1_airfoil1_name": "s1223",
                  "wing1_airfoil2_name": "s1223",
                  "wing1_airfoil3_name": "s1223",
                  "wing1_span1": 1,
                  "wing1_span2": 1,
                  "wing1_chord1": 0.35,
                  "wing1_chord2": 0.33,
                  "wing1_chord3": 0.30,
                  "wing1_twist1": 10,
                  "wing1_twist2": 5,
                  "wing1_twist3": 3,
                  "wing1_incidence": 1,
                  "wing1_CM_ca": 0.08,
                  "wing2_x": 0,
                  "wing2_y": 0,
                  "wing2_z": 0,
                  "wing2_clmax_airfoil": 2.8,
                  "wing2_airfoil1_name": "s1223",
                  "wing2_airfoil2_name": "s1223",
                  "wing2_airfoil3_name": "s1223",
                  "wing2_span1": 1.10,
                  "wing2_span2": 1.10,
                  "wing2_chord1": 0.40,
                  "wing2_chord2": 0.35,
                  "wing2_chord3": 0.33,
                  "wing2_twist1": 5,
                  "wing2_twist2": 3,
                  "wing2_twist3": 0,
                  "wing2_incidence": 1,
                  "wing2_CM_ca": 0.10,
                  "hs_x": 0.9,
                  "hs_y": 0,
                  "hs_z": 0,
                  "hs_clmax_airfoil": 2.1,
                  "hs_airfoil1_name": "sd7037",
                  "hs_airfoil2_name": "sd7037",
                  "hs_airfoil3_name": "sd7037",
                  "hs_span1": 0.30,
                  "hs_span2": 0.30,
                  "hs_chord1": 0.24,
                  "hs_chord2": 0.24,
                  "hs_chord3": 0.24,
                  "hs_twist1": 0,
                  "hs_twist2": 0,
                  "hs_twist3": 0,
                  "hs_incidence": 0,
                  "hs_CM_ca": 0.06,
                  "motor_x": 0,
                  "motor_y": 0,
                  "motor_z": 0,
                  "static_thrust": 0,
                  "linear_decay_coefficient": -0.15,
                  "cg_x": 0.11,
                  "cg_z": 0.01,
                  "tpr_x": 0.13,
                  "tpr_z": -0.08,
                  "Iyy_TPR": 1,
                  "CD_tp": 1,
                  "S_tp": 1,
                  "CD_fus": 1,
                  "S_fus": 1,
                  "u_k": 1}
    plane = Plane(plane_data)
    return plane


def test_get_CL_alpha_plane(plane):
    cl = {-10.0: 0.8961720610687022,
          -9.0:  1.0828123664122136,
          -8.0:  1.2690087022900762,
          -7.0:  1.4544367938931297,
          -6.0:  1.6393807633587787,
          -5.0:  1.8236004580152672,
          -4.0:  2.00718,
          -3.0:  2.1898352671755723,
          -2.0:  2.3712140458015263,
          -1.0:  2.5516685496183205,
          0.0:   2.7310867175572517,
          1.0:   2.9091882442748087,
          2.0:   3.085813282442748,
          3.0:   3.260721679389313,
          4.0:   3.4343535877862594,
          5.0:   3.606312824427481,
          6.0:   3.7766433587786263,
          7.0:   3.945017099236641,
          8.0:   4.111562137404579,
          9.0:   4.276278473282442,
          10.0:  4.438685801526717,
          11.0:  4.59902427480916,
          12.0:  4.75733786259542,
          13.0:  4.836142442748091,
          14.0:  4.913922137404579,
          15.0:  4.99043679389313,
          16.0:  4.977114045801526,
          17.0:  4.9639671755725185,
          18.0:  4.950996183206107,
          19.0:  4.938289007633587,
          20.0:  4.925757709923665}

    df_cl_alpha = dict_to_dataframe(cl, "CL", "alpha")
    pd.testing.assert_frame_equal(
        plane.get_CL_alpha_plane(), df_cl_alpha, check_less_precise=3)


def test_get_CD_alpha_plane(plane):
    cd = {-10.0: 0.005704,
          - 9.0:  0.011138,
          - 8.0:  0.017323,
          - 7.0:  0.024453,
          - 6.0:  0.032331,
          - 5.0:  0.040958,
          - 4.0:  0.050333,
          - 3.0:  0.060700,
          - 2.0:  0.072012,
          - 1.0:  0.083633,
          0.0:  0.096442,
          1.0:  0.109715,
          2.0:  0.123580,
          3.0:  0.138194,
          4.0:  0.153556,
          5.0:  0.169427,
          6.0:  0.185846,
          7.0:  0.203057,
          8.0:  0.220337,
          9.0:  0.238164,
          10.0: 0.256300,
          11.0: 0.274833,
          12.0: 0.293873,
          13.0: 0.303226,
          14.0: 0.312970,
          15.0: 0.322387,
          16.0: 0.320189,
          17.0: 0.317946,
          18.0: 0.315616,
          19.0: 0.313242,
          20.0: 0.31082}

    df_cd_alpha = dict_to_dataframe(cd, "CD", "alpha")
    pd.testing.assert_frame_equal(
        plane.get_CD_alpha_plane(), df_cd_alpha, check_less_precise=3)


def test_get_V_stall(plane):
    npt.assert_almost_equal(plane.get_V_stall(1.2), 3.536, decimal=3)


def test_get_V_CLmin(plane):
    npt.assert_almost_equal(plane.get_V_CLmin(1.2), 8.345, decimal=3)


def test_set_alpha_range(plane):
    plane.set_alpha_range()
    new_alpha_range = plane.alpha_range
    x = list(range(-10, 13))
    npt.assert_array_almost_equal_nulp(new_alpha_range, x, nulp=0)
