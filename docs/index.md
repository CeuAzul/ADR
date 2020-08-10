# Home

## What is **ADR**?
ADR is a python library to analyse aircraft conceptual designs. ADR has 
several tools that allows one to create different aircraft designs and analyse 
those from different points os view. 

## What can it do?
From 2.0, users can specify a free-body with any number of attached (and nested) 
componentes, in any position. Because of its generalist object-oriented
structure, ADR allows components to be attached in any way imaginable, by only
specifing to which other component it is attached, its relative position and 
angle, like so:

``` python
import math
from vec import Vector2
from adr.World import Ambient
from adr.Components import FreeBody, AttachedComponent

ambient = Ambient()

plane = FreeBody(
    name='plane',
    mass=0.0,
    position_cg=Vector2(x=-0.05, y=0),
    pitch_rot_inertia=30.0,
    ambient=ambient
)

wing = AttachedComponent(
    name='wing',
    relative_position=Vector2(x=-0.10, y=0),
    relative_angle=math.radians(+5),
    mass=0.370,
)

wing.set_parent(plane)

print(plane.wing.mass)
>>> 0.37
```