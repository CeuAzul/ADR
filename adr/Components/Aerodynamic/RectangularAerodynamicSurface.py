import attr
from vec import Vector2

from adr.Components.Aerodynamic import AerodynamicSurface


@attr.s(auto_attribs=True)
class RectangularAerodynamicSurface(AerodynamicSurface):
    type: str = 'rectangular_aerodynamic_surface'
    span: float = None
    chord: float = None

    @property
    def area(self):
        return self.span*self.chord

    @property
    def mean_aerodynamic_chord(self):
        return self.chord

    @property
    def aerodynamic_center(self):
        return Vector2(-0.25 * self.mean_aerodynamic_chord, 0)
