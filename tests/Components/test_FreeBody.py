from adr.Components import FreeBody
from adr.World import Ambient
from vec import Vector2
import math
import pytest
import numpy.testing as npt


@pytest.fixture
def freebody():
    env = Ambient()
    freebody = FreeBody(
        name='freebody',
        type='generic_freebody',
        mass=23.4,
        position_cg=Vector2(-0.2, 0.02),
        pitch_rot_inertia=5.2,
        ambient=env,
    )
    return freebody


def test_instantiation(freebody):
    assert(freebody.position_cg.x == -0.2)
    assert(freebody.position_cg.y == 0.02)
    assert(freebody.pitch_rot_inertia == 5.2)
    assert(freebody.ambient.temperature == 273.15)


def test_reset_state(freebody):
    freebody.position = Vector2(2, 4)
    freebody.angle = 3
    freebody.velocity = Vector2(7, 2)
    freebody.rot_velocity = 6

    freebody.reset_state()

    assert (freebody.position == Vector2(0, 0))
    assert (freebody.angle == 0)
    assert (freebody.velocity == Vector2(0.00001, 0.00001))
    assert (freebody.rot_velocity == 0)


def test_states(freebody):
    freebody.position = Vector2(15.1, 1.2)
    freebody.angle = math.radians(15)
    freebody.velocity = Vector2(12.1, 0.7)
    freebody.rot_velocity = 14
    assert(freebody.position == Vector2(15.1, 1.2))
    assert(freebody.angle == math.radians(15))
    assert(freebody.velocity == Vector2(12.1, 0.7))
    assert(freebody.rot_velocity == 14)


def test_gravitational_center(freebody):
    assert(freebody.gravitational_center == Vector2(-0.2, 0.02))


def test_get_total_weight(freebody):
    freebody.angle = math.radians(15)
    weight, weight_point = freebody.get_total_weight()
    npt.assert_almost_equal(weight.r, 229.47, decimal=2)
    npt.assert_almost_equal(weight.theta, math.radians(-105), decimal=2)
    assert weight_point == Vector2(-0.2, 0.02)
