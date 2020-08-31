from adr.Components import AttachedComponent, FreeBody, BaseComponent
from adr.World import Ambient
from vec import Vector2
import math
import numpy.testing as npt
import pytest


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

@pytest.fixture
def freebody_component():
    freebody_component = FreeBody(
        name='component',
        type='generic_component',
        mass=3.4,
        angle=math.radians(5),
        position_cg=Vector2(-0.7, 0.2),
        pitch_rot_inertia=30.0,
        ambient=Ambient()
    )
    return freebody_component

@pytest.fixture
def base_component():
    base_component = BaseComponent(
        name='component',
        type='generic_component',
        mass=3.4,
    )
    return base_component

@pytest.fixture
def extra_base_component():
    base_component = BaseComponent(
        name='component',
        type='generic_component',
        mass=3.4,
    )
    return extra_base_component

def test_instantiation(attached_component):
    assert(attached_component.relative_position.x == -0.4)
    assert(attached_component.relative_position.y == 0.1)
    assert(attached_component.relative_angle == math.radians(9))


def test_reset_state(attached_component):
    attached_component.actuation_angle = math.radians(-7)
    attached_component.reset_state()
    assert (attached_component.actuation_angle == 0)


def test_states(attached_component):
    attached_component.actuation_angle = math.radians(3)
    assert(attached_component.actuation_angle == math.radians(3))

def test_angle(attached_component, freebody_component):
    attached_component.set_parent(freebody_component)
    angle = math.degrees(attached_component.angle)
    assert(angle == 14)
    attached_component.actuation_angle = math.radians(10)
    angle = math.degrees(attached_component.angle)
    npt.assert_almost_equal(angle, 24, decimal = 0)

def test_set_parent(attached_component, base_component, extra_base_component):
    attached_component.set_parent(base_component)
    assert(attached_component.parent == base_component)
    with pytest.raises(Exception):
        assert attached_component.set_parent(extra_base_component)


def test_ambient(attached_component, freebody_component):
    attached_component.set_parent(freebody_component)
    assert(attached_component.ambient == freebody_component.ambient)
