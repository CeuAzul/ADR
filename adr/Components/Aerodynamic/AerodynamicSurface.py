import attr
import math
from vec import Vector2

from adr.Components import AttachedComponent
from adr.Methods.Aerodynamic.aerodynamic_fundamental_equations import get_lift, get_drag, get_moment
from adr.World.Aerodynamic.coefficients_data import get_CL, get_CD, get_CM, get_CL_inv, get_CD_inv, get_CM_inv


@attr.s(auto_attribs=True)
class AerodynamicSurface(AttachedComponent):
    type: str = 'aerodynamic_surface'
    inverted: bool = False
    span: float = None
    chord: float = None

    def __attrs_post_init__(self):
        self.add_external_force_function('lift', self.get_lift)
        self.add_external_force_function('drag', self.get_drag)
        self.add_external_moment_function('moment', self.get_moment)

    @property
    def area(self):
        return -1

    @property
    def mean_aerodynamic_chord(self):
        return -1

    @property
    def aerodynamic_center(self):
        return -1

    def get_lift(self):
        if self.inverted:
            CL = get_CL_inv(self.angle_of_attack)
        else:
            CL = get_CL(self.angle_of_attack)
        lift_mag = get_lift(
            self.ambient.air_density,
            self.velocity.r,
            self.area,
            CL)
        lift_angle = math.radians(90) - self.angle_of_attack
        lift = Vector2(r=lift_mag, theta=lift_angle)
        return lift, self.aerodynamic_center

    def get_drag(self):
        if self.inverted:
            CD = get_CD_inv(self.angle_of_attack)
        else:
            CD = get_CD(self.angle_of_attack)
        drag_mag = get_drag(
            self.ambient.air_density,
            self.velocity.r,
            self.area,
            CD)
        drag_angle = math.radians(180) - self.angle_of_attack
        drag = Vector2(r=drag_mag, theta=drag_angle)
        return drag, self.aerodynamic_center

    def get_moment(self):
        if self.inverted:
            CM = get_CM_inv(self.angle_of_attack)
        else:
            CM = get_CM(self.angle_of_attack)
        moment_mag = get_moment(self.ambient.air_density,
                                self.velocity.r,
                                self.area,
                                CM,
                                self.mean_aerodynamic_chord)
        return moment_mag
