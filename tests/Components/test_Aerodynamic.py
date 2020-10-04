import attr
from vec import Vector2
import math
import numpy.testing as npt
import pytest
from adr.Components.Aerodynamic import RectangularHorizontalStabilizer


@pytest.fixture
def rectangular_horizontal_stabilizer():
    rectangular_horizontal_stabilizer = RectangularHorizontalStabilizer(
        name='rectangular_horizontal_stabilizer',
        relative_position=Vector2(x=-0.7, y=0.2),
        relative_angle=math.radians(0),
        mass=0.15,
        span=0.15,
        chord=0.20
    )
    return rectangular_horizontal_stabilizer


def test_rectangular_aerodynamic_stabilizer(rectangular_horizontal_stabilizer):
    assert (rectangular_horizontal_stabilizer.type == 'horizontal_stabilizer')
    assert (rectangular_horizontal_stabilizer.name ==
            'rectangular_horizontal_stabilizer')
    assert (rectangular_horizontal_stabilizer.span == 0.15)
    assert (rectangular_horizontal_stabilizer.chord == 0.20)
    assert (rectangular_horizontal_stabilizer.mass == 0.15)
