import attr
import math
from vec import Vector2

from adr.World.constants import gravitational_acceleration
from adr.Components import AttachedComponent
from adr.Methods.Powertrain.thrust_equations import get_axial_thrust_from_linear_model


@attr.s(auto_attribs=True)
class LandingGear(AttachedComponent):
    type: str = 'landing_gear'
    height: float = None
    spring_coeff: float = None
    dump_coeff: float = None
    friction_coeff: float = None

    def __attrs_post_init__(self):
        self.add_external_force_function(
            'gear_reaction', self.gear_reaction)
        self.add_external_force_function(
            'gear_friction', self.gear_friction)

    @property
    def floor_contact_point(self):
        return Vector2(0, -self.height)

    def gear_reaction(self):
        displacement = self.height-self.position.y
        axial_velocity = self.velocity.y
        if displacement > 0:
            reaction_mag = self.spring_coeff*displacement - self.dump_coeff*axial_velocity
        else:
            reaction_mag = 0
        reaction = Vector2(0, reaction_mag)
        return reaction, self.floor_contact_point

    def gear_friction(self):
        normal_force, contact_point = self.gear_reaction()

        if self.velocity.x > 0:
            velocity_direction = 1
        else:
            velocity_direction = -1

        friction_mag = self.friction_coeff * normal_force.r * velocity_direction

        friction = Vector2(-friction_mag, 0)
        return friction, self.floor_contact_point
