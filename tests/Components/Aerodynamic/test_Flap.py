import pytest
import math
from vec import Vector2

from adr.Components.Aerodynamic import Flap


@pytest.fixture
def flap():
    flap = Flap(
        name='flap',
        mass=0.05,
        relative_position=Vector2(-0.34, 0),
        relative_angle=math.radians(0),
        width=0.25,
        height=0.06
    )
    return flap


def test_instantiation(flap):
    assert(flap.type == 'flap')
    assert(flap.width == 0.25)
    assert(flap.height == 0.06)
