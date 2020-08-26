from adr.Components import AttachedComponent, FreeBody
from adr.World import Ambient
from vec import Vector2
import math
import pytest


@pytest.fixture
def freebody_component():
    freebody_component = FreeBody(
        name='component',
        type='generic_component',
        mass=3.4,
        position_cg=Vector2(-0.7, 0.2),
        pitch_rot_inertia=30.0,
        ambient=Ambient()
    )
    return freebody_component


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


def test_instantiation(attached_component):
    assert(attached_component.relative_position.x == -0.4)
    assert(attached_component.relative_position.y == 0.1)
    assert(attached_component.relative_angle == math.radians(9))


def test_states(attached_component):
    attached_component.actuation_angle = math.radians(3)
    assert(attached_component.actuation_angle == math.radians(3))


def test_position(freebody_component, attached_component):
    attached_component.set_parent(freebody_component)
    assert(attached_component.position == Vector2(-0.4, 0.1))
    freebody_component.angle = math.radians(10)
    freebody_component.position = Vector2(-0.5, 0.2)
    assert(attached_component.position ==
           Vector2(-0.894, 0.2985))
    #freebody_component.angle = -10
    #freebody_component.position = Vector2(0.3, -0.5)
    # assert(attached_component.position == Vector2(
    #    0.5812265005416439, -0.8015155972633932))
