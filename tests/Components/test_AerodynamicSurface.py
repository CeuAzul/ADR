import attr
from vec import Vector2
import math
import numpy.testing as npt
import pytest
from adr.World import Ambient
from adr.Components import FreeBody, AttachedComponent
from adr.Components.Aerodynamic import AerodynamicSurface


env = Ambient()
plane = FreeBody(
    name='freebody',
    type='generic_freebody',
    mass=23.4,
    angle=8.0,
    velocity=Vector2(5.0, 2.0),
    position_cg=Vector2(-0.2, 0.02),
    pitch_rot_inertia=5.2,
    ambient=env,
)


@pytest.fixture
def aerodynamic_surface():
    aerodynamic_surface = AerodynamicSurface(
        name='aerodynamic_surface',
        relative_position=Vector2(x=0.0, y=0.1),
        relative_angle=math.radians(0),
        mass=0.9,
        span=0.30,
        chord=0.4
    )
    aerodynamic_surface.set_parent(plane)
    return aerodynamic_surface


def test_aerodynamic_surface(aerodynamic_surface):
    assert (aerodynamic_surface.name ==
            'aerodynamic_surface')
    assert (aerodynamic_surface.span == 0.30)
    assert (aerodynamic_surface.chord == 0.4)
    assert (aerodynamic_surface.mass == 0.9)


def test_area(aerodynamic_surface):
    assert(aerodynamic_surface.area == -1)


def test_mean_aerodynamic_chord(aerodynamic_surface):
    assert(aerodynamic_surface.mean_aerodynamic_chord == -1)


def test_aerodynamic_center(aerodynamic_surface):
    assert(aerodynamic_surface.aerodynamic_center == -1)


def test_get_lift(aerodynamic_surface):
    assert(aerodynamic_surface.get_lift() ==)
