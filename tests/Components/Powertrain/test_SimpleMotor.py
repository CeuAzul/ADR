import attr
from vec import Vector2
from adr.World import Ambient
from adr.Components import FreeBody
from adr.Components.Powertrain import SimpleMotor
from adr.Methods.Powertrain.thrust_equations import get_axial_thrust_from_linear_model
import numpy.testing as npt
import math
import pytest

@pytest.fixture
def motor():
    motor = SimpleMotor(
       name='attached_component',
       mass=1.4,
       relative_position=Vector2(-0.4, 0.1),
       relative_angle=math.radians(0),
       static_thrust = 78,
       linear_coefficient = -1,
       distance_origin_to_propeller = 0.3
    )
    return motor

@pytest.fixture
def plane():
    env = Ambient()
    plane = FreeBody(
        name='freebody',
        type='generic_freebody',
        mass=23.4,
        position_cg=Vector2(-0.2, 0.02),
        pitch_rot_inertia=5.2,
        ambient=env,
    )
    return plane

def test_thrust_center(motor, plane):
   
    motor.set_parent(plane)
    
    check_thrust_center = Vector2(0.3, 0)

    assert(motor.thrust_center == check_thrust_center)

def test_get_thrust(motor, plane):
   
    motor.set_parent(plane)
    x,y = motor.get_thrust()

    check_thrust_center = Vector2(0.3, 0)
    check_thrust = Vector2(82.269378, 0)

    npt.assert_array_almost_equal(x, check_thrust)
    npt.assert_array_almost_equal(y, check_thrust_center)
    