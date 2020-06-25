from ADR.Methods.FundamentalEquations import lift, drag, moment
import numpy.testing as npt


def test_lift():
    npt.assert_almost_equal(lift(1.25, 14.3, 2.7, 0.9), 310.569, decimal=3)
