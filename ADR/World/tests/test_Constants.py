from ADR.World.Constants.Constants import get_gravity_constant
import numpy.testing as npt

def test_get_gravity_constant():
    npt.assert_almost_equal(get_gravity_constant(), 9.7925, decimal=4)
