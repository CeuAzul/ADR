import attr
import math
from vec import Vector2

from adr.Components.Aerodynamic import RectangularAerodynamicSurface


@attr.s(auto_attribs=True)
class RectangularWing(RectangularAerodynamicSurface):
    type: str = 'wing'
