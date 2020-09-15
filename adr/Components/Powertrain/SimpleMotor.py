import attr
from vec import Vector2

from adr.Components.Powertrain import Motor
from adr.Methods.Powertrain.thrust_equations import get_axial_thrust_from_linear_model


@attr.s(auto_attribs=True)
class SimpleMotor(Motor):
    static_thrust: float = None
    linear_coefficient: float = None
    distance_origin_to_propeller: float = None

    @property
    def thrust_center(self):
        return Vector2(self.distance_origin_to_propeller, 0)

    def get_thrust(self):
        angle_of_attack = self.angle_of_attack
        axial_velocity = self.velocity.rotated(angle_of_attack).x

        thrust_mag = get_axial_thrust_from_linear_model(
            self.ambient.air_density,
            axial_velocity,
            self.static_thrust,
            self.linear_coefficient
        )

        thrust = Vector2(thrust_mag, 0)
        return thrust, self.thrust_center
