## RectangularHorizontalStabilizer
This class is responsible for creating a rectangular horizontal stabilizer type component. For this, it is necessary to pass as parameters the position and the angle in relation to the parent component, as well as the chord and span of the rectangular horizontal stabilizer.
```python
from vec import Vector2
import math
import pytest
from adr.Components.Aerodynamic import RectangularHorizontalStabilizer

rectangular_horizontal_stabilizer = RectangularHorizontalStabilizer(
    name='rectangular_horizontal_stabilizer',
    relative_position=Vector2(x=-0.7, y=0.2),
    relative_angle=math.radians(0),
    mass=0.14,
    span=0.15,
    chord=0.20
)

print(rectangular_horizontal_stabilizer.name)
>>> rectangular_horizontal_stabilizer

print(rectangular_horizontal_stabilizer.type)
>>> horizontal_stabilizer

print(rectangular_horizontal_stabilizer.mass)
>>> 0.14

print(rectangular_horizontal_stabilizer.span)
>>> 0.15

print(rectangular_horizontal_stabilizer.chord)
>>> 0.2
```