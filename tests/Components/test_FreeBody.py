from adr.Components import FreeBody, AttachedComponent
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


@pytest.fixture
def attached_component():
    attached_component = AttachedComponent(
        name='attached_component',
        type='generic_attached_component',
        mass=1.4,
        relative_position=Vector2(-0.4, 0.1),
        relative_angle=math.radians(9)
    )
    return attached_component


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


def test_force_and_moment_at_cg(freebody, attached_component):
    def ext_force_function1():
        return Vector2(-0.9, 0.5), Vector2(0.6, 2.0)

    def ext_force_function2():
        return Vector2(1, 1.4), Vector2(-0.5, -0.1)

    attached_component.set_parent(freebody)
    freebody.external_forces.pop('weight')
    freebody.external_forces['force1'] = ext_force_function1
    freebody.external_moments['moment1'] = lambda: 10.0
    attached_component.external_forces['force2'] = ext_force_function2
    attached_component.external_moments['moment2'] = lambda: 20.0
    force, moment = freebody.force_and_moment_at_cg()
    npt.assert_almost_equal(force.x, -0.131, decimal=3)
    npt.assert_almost_equal(force.y, 2.04, decimal=3)
    npt.assert_almost_equal(moment, 31.212, decimal=3)


def test_move(monkeypatch, freebody):
    freebody.mass = 2
    freebody.pitch_rot_inertia = 3
    freebody.rot_velocity = 2
    freebody.angle = 1
    freebody.velocity = Vector2(12, 3)
    freebody.position = Vector2(5, 1)

    def force_and_moment_at_cg_mock():
        return Vector2(50, 10), 1.5

    freebody.force_and_moment_at_cg = force_and_moment_at_cg_mock

    total_force, moment_z = freebody.move(0.1)

    npt.assert_almost_equal(freebody.rot_velocity, 2.05)
    npt.assert_almost_equal(freebody.angle, 1.205)
    npt.assert_almost_equal(freebody.velocity.x, 14.5)
    npt.assert_almost_equal(freebody.velocity.y, 3.5)
    npt.assert_almost_equal(freebody.position.x, 6.45)
    npt.assert_almost_equal(freebody.position.y, 1.35)

    npt.assert_almost_equal(total_force.x, 50)
    npt.assert_almost_equal(total_force.y, 10)
    npt.assert_almost_equal(moment_z, 1.5)
