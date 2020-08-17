from adr.Components import AttachedComponent
from vec import Vector2
import math
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


def test_instantiation(attached_component):
    assert(attached_component.relative_position.x == -0.4)
    assert(attached_component.relative_position.y == 0.1)
    assert(attached_component.relative_angle == math.radians(9))


def test_states(attached_component):
    attached_component.actuation_angle = math.radians(3)
    assert(attached_component.actuation_angle == math.radians(3))
