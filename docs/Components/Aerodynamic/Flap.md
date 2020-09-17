# Flap

The Flap class is intended to be a modifier for the lift and drag calculation on wings. Currently it only has height and width properties that can afterwards be used to calculate its correct aerodynamic behaviour.

## Instantiation
To instantiate a Flap one can pass the same arguments used to instantiate an AttachedComponent plus its height and width:

``` python
import math
from vec import Vector2

from adr.Components.Aerodynamic import Flap

flap = Flap(
    name='flap',
    mass=0.05,
    relative_position=Vector2(-0.34, 0),
    relative_angle=math.radians(0),
    width=0.25,
    height=0.06
)

print(flap.type)
>>> flap
print(f'Flap dimensions are: {100*flap.width} x {100*flap.height} [cm].')
>>> Flap dimensions are: 25.0 x 6.0 [cm].
```

Remember that a Flap component represents only one physical flap, so one probably wants to always have at least two simetrically positioned flap instances on each aerodynamic surface.