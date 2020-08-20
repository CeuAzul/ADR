from adr.World import constants
import numpy.testing as npt


def test_fixed_constants():
    assert constants.air_molar_mass == 0.02896
    assert constants.gravitational_acceleration == 9.80665


def test_air_gas_constant():
    npt.assert_almost_equal(constants.air_gas_constant, 287.101, decimal=3)
