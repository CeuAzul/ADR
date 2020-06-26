from ADR.Components.Propulsion.Motor import *
import numpy.testing as npt


def test_Motor():
    mydict = {"static_thrust": 14, "linear_decay_coefficient": 2}
    npt.assert_almost_equal(Motor(mydict).thrust(35), -56, decimal=0)
