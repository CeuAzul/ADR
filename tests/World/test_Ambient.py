from adr.World import Ambient
import numpy.testing as npt
import pytest


@pytest.fixture
def base_ambient():
    base_ambient = Ambient(temperature=288.15, pressure=101325, humidity=30)
    return base_ambient


def test_instantiation(base_ambient):
    assert base_ambient.temperature == 288.15
    assert base_ambient.pressure == 101325
    assert base_ambient.humidity == 30


def test_air_density(base_ambient):
    npt.assert_almost_equal(base_ambient.air_density, 1.224, decimal=3)


def test_instantiation_error():
    ambient = Ambient(temperature=0)
    with pytest.raises(ValueError) as e_info:
        air_density = ambient.air_density

    ambient = Ambient(humidity=104)
    with pytest.raises(ValueError) as e_info:
        air_density = ambient.air_density

    ambient = Ambient(pressure=-3)
    with pytest.raises(ValueError) as e_info:
        air_density = ambient.air_density

