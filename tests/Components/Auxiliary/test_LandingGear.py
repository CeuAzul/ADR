import pytest
import math
from vec import Vector2
import numpy.testing as npt

from adr.World import Ambient
from adr.Components import FreeBody
from adr.Components.Auxiliary import LandingGear


@pytest.fixture
def plane():
    env = Ambient()
    plane = FreeBody(
        name='plane',
        type='plane',
        mass=23.4,
        position_cg=Vector2(-0.2, 0.02),
        pitch_rot_inertia=5.2,
        ambient=env,
    )
    return plane


@pytest.fixture
def main_landing_gear():
    main_landing_gear = LandingGear(
        name='main_landing_gear',
        relative_position=Vector2(x=-0.2, y=0),
        relative_angle=math.radians(0),
        mass=0.3,
        height=0.1,
        spring_coeff=1000,
        dump_coeff=50,
        friction_coeff=0.05
    )
    return main_landing_gear


def test_instantiation(main_landing_gear):
    assert(main_landing_gear.type == 'landing_gear')
    assert(main_landing_gear.height == 0.1)
    assert(main_landing_gear.spring_coeff == 1000)
    assert(main_landing_gear.dump_coeff == 50)
    assert(main_landing_gear.friction_coeff == 0.05)


def test_floor_contact_point(main_landing_gear):
    contact_point = Vector2(0, -0.1)
    npt.assert_almost_equal(contact_point.x, 0)
    npt.assert_almost_equal(contact_point.y, -0.1)


def test_gear_reaction(plane, main_landing_gear):
    main_landing_gear.set_parent(plane)
    plane.velocity = Vector2(6, 0.4)

    # Plane on air (position.y = 2m), so no reaction on landing gear is expected
    plane.position = Vector2(10, 2)
    reaction, contact_point = main_landing_gear.gear_reaction()
    assert(type(contact_point) is Vector2)
    npt.assert_almost_equal(reaction.y, 0)

    # Plane on ground (position.y = 0m), so reaction on landing gear is expected
    plane.position = Vector2(10, 0)
    reaction, contact_point = main_landing_gear.gear_reaction()
    npt.assert_almost_equal(reaction.y, 80.0)


def test_gear_friction(plane, main_landing_gear):
    main_landing_gear.set_parent(plane)
    plane.velocity = Vector2(6, 0.4)

    # Plane on air (position.y = 2m), so no friction on landing gear is expected
    plane.position = Vector2(10, 2)
    friction, contact_point = main_landing_gear.gear_friction()
    assert(type(contact_point) is Vector2)
    npt.assert_almost_equal(friction.x, 0)

    # Plane on ground (position.y = 0m), going forward, expected friction on negative x direction
    plane.position = Vector2(10, 0)
    friction, contact_point = main_landing_gear.gear_friction()
    npt.assert_almost_equal(friction.x, -4.0)

    # Plane on ground (position.y = 0m), going backwards, expected friction on positive x direction
    plane.velocity = Vector2(-6, 0.4)
    plane.position = Vector2(10, 0)
    friction, contact_point = main_landing_gear.gear_friction()
    npt.assert_almost_equal(friction.x, 4.0)
