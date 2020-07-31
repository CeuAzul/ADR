from ADR.Analysis.Stability.FlightStability.FlightStability import FlightStability
from ADR.parameters import get_plane_parameters
from ADR.Core.data_manipulation import dict_to_dataframe
from ADR.Components.Plane import Plane
import numpy.testing as npt
import pandas as pd
import pytest


@pytest.fixture
def plane():
    plane_parameters = get_plane_parameters()
    plane = Plane(plane_parameters)
    return plane


@pytest.fixture
def flightStabilyty_analysis(plane):
    flightStabilyty_analysis = FlightStability(plane)
    return flightStabilyty_analysis


def test_CM_plane_CG(flightStabilyty_analysis):
    dict_of_CM_ALPHA_dataframes = flightStabilyty_analysis.CM_plane_CG(0.10)
    CM_ALPHA_dataframe_for_hs_at_theta_12 = dict_of_CM_ALPHA_dataframes[12.0]
    CM_ALPHA_dataframe_for_hs_at_theta_10_negative = dict_of_CM_ALPHA_dataframes[-10.0]
    CM_ALPHA_dataframe_for_hs_at_theta_3_negative = dict_of_CM_ALPHA_dataframes[-3.0]
    CM_ALPHA_dataframe_for_hs_at_theta_8 = dict_of_CM_ALPHA_dataframes[8.0]
    CM_at_hs_theta_12_alpha_7 = CM_ALPHA_dataframe_for_hs_at_theta_12.at[7.0, 'CM']
    CM_at_hs_theta_10_negative_alpha_ = CM_ALPHA_dataframe_for_hs_at_theta_10_negative.at[-8.0, 'CM']
    CM_at_hs_theta_3_negative_alpha_ = CM_ALPHA_dataframe_for_hs_at_theta_3_negative.at[
        0.0, 'CM']
    CM_at_hs_theta_8_alpha_ = CM_ALPHA_dataframe_for_hs_at_theta_8.at[-4.0, 'CM']
    npt.assert_almost_equal(CM_at_hs_theta_12_alpha_7, -0.264243, decimal=3)
    npt.assert_almost_equal(
        CM_at_hs_theta_10_negative_alpha_, -0.458495, decimal=3)
    npt.assert_almost_equal(
        CM_at_hs_theta_3_negative_alpha_, -0.503782, decimal=3)
    npt.assert_almost_equal(CM_at_hs_theta_8_alpha_, 0.436243, decimal=3)


def test_trimm(flightStabilyty_analysis):
    trimm = {-9.0: -2.0,
             -7.0: -1.0,
             -6.0: 0.0,
             -5.0: 1.0,
             -3.0: 2.0,
             -2.0: 4.0,
             -1.0: 5.0,
             0.0: 6.0,
             1.0: 7.0,
             2.0: 9.0,
             3.0: 10.0,
             4.0: 12.0,
             5.0: 14.0,
             6.0: 16.0,
             7.0: 18.0,
             8.0: 20.0,
             9.0: 21.0}
    df_trimm = dict_to_dataframe(trimm, "hs_incidence", "alpha")
    pd.testing.assert_frame_equal(
        flightStabilyty_analysis.trimm(), df_trimm, check_less_precise=0)


def test_staticMargin(flightStabilyty_analysis):
    static_margin = {-10.0:  0.095644,
                     -9.0:   0.095188,
                     -8.0:   0.128566,
                     -7.0:   0.162950,
                     -6.0:   0.193622,
                     -5.0:   0.226191,
                     -4.0:   0.260375,
                     -3.0:   0.290155,
                     -2.0:   0.324483,
                     -1.0:   0.355945,
                     0.0:   0.387831,
                     1.0:   0.421747,
                     2.0:   0.455880,
                     3.0:   0.487963,
                     4.0:   0.518558,
                     5.0:   0.555706,
                     6.0:   0.587471,
                     7.0:   0.623065,
                     8.0:   0.658152,
                     9.0:   0.691660,
                     10.0:  0.727988}
    df_staticMargin = dict_to_dataframe(static_margin, "SM", "alpha")
    pd.testing.assert_frame_equal(
        flightStabilyty_analysis.static_margin(), df_staticMargin, check_less_precise=0)
