import attr
from typing import Dict, Callable
from vec import Vector2
import math

from adr.Components import BaseComponent
from adr.World import gravitational_acceleration, Ambient


@attr.s(auto_attribs=True)
class FreeBody(BaseComponent):
    position_cg: Vector2 = None
    pitch_rot_inertia: float = None
    ambient: Ambient = None

    # State attributes
    position: Vector2 = Vector2(0, 0)
    angle: float = 0
    velocity: Vector2 = Vector2(0.00001, 0.00001)
    rot_velocity: float = 0

    def __attrs_post_init__(self):
        self.add_external_force_function('weight', self.get_total_weight)

    def reset_state(self):
        self.position = Vector2(0, 0)
        self.angle = 0
        self.velocity = Vector2(0.00001, 0.00001)
        self.rot_velocity = 0
        super().reset_state()

    @property
    def gravitational_center(self) -> Vector2:
        return self.position_cg

    def force_and_moment_at_cg(self):
        force_at_cg = Vector2(0, 0)
        moment_at_cg = 0

        force_at_origin, moment_at_origin = self.force_and_moment_at_component_origin()

        force_at_cg += force_at_origin
        moment_at_cg += moment_at_origin
        moment_at_cg += (Vector2(0, 0) -
                         self.gravitational_center).cross(force_at_origin)
        return force_at_cg, moment_at_cg

    def get_total_weight(self):
        weight_mag = gravitational_acceleration*self.total_mass
        weight_angle = math.radians(-90) - self.angle
        weight = Vector2(r=weight_mag, theta=weight_angle)
        return weight, self.gravitational_center

    def move(self, time_step):
        total_force, moment_z = self.force_and_moment_at_cg()

        acc = total_force/self.total_mass
        ang_acc_z = moment_z/self.pitch_rot_inertia

        self.rot_velocity = self.rot_velocity + ang_acc_z * time_step
        self.angle = self.angle + self.rot_velocity * time_step

        self.velocity = self.velocity + acc * time_step
        self.position = self.position + self.velocity * time_step

        return total_force, moment_z
