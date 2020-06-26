from ADR.Components.Propulsion.Motor import *
import numpy.testing as npt


def test_Motor():
    motor_parameters = {"static_thrust": 14, "linear_decay_coefficient": 2}
    motor = Motor(motor_parameters)
    npt.assert_almost_equal(motor.thrust(5), 4, decimal=0)
