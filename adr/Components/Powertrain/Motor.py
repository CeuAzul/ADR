import attr
import math
from vec import Vector2

from adr.Components import AttachedComponent
from adr.Methods.Powertrain.thrust_equations import get_axial_thrust_from_linear_model


@attr.s(auto_attribs=True)
class Motor(AttachedComponent):
    type: str = 'motor'

    def __attrs_post_init__(self):
        self.add_external_force_function('thrust', self.get_thrust)

    @property
    def thrust_center(self):
        return Vector2(0, 0)

    def get_thrust(self):
        thrust = Vector2(0, 0)
        return thrust, self.thrust_center
