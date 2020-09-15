import attr
import math
from vec import Vector2

from adr.Components.Aerodynamic import RectangularAerodynamicSurface


@attr.s(auto_attribs=True)
class RectangularHorizontalStabilizer(RectangularAerodynamicSurface):
    type: str = 'horizontal_stabilizer'
    inverted: bool = True
