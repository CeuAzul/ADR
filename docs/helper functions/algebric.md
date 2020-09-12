# Algebric helper functions
Some algebric helper functions are available so one can easily deal with
transformations of the vectors in 2D space.

## *rotate(vector2d, angle_radians)*:
Given a vec.Vector2 and an angle (in radians), returns a new vec.Vector2
instance equal to the original vector rotated by the angle.
``` python
from adr.helper_functions import rotate
from vec import Vector2
import math
v1 = Vector2(0.7, 0.2)
v1_rot_90 = rotate(v1, math.radians(90))
print(v1_rot_90)
>>> <Vector2 (-0.19999999999999996, 0.7)>
```
Notice the vec library doesn't always provide rounded coordinates because of
float point precision.

## *translate(vector2d, displacement_x, displacement_y)*:
Given a vec.Vector2 and displacements on x and y coordinates, returns a new
vec.Vector2 instance equal to the original vector translated by the displacements.
``` python
from adr.helper_functions import translate
from vec import Vector2
import math
v1 = Vector2(0.5, -0.1)
v1_trans = translate(v1, 0.5, 0.1)
print(v1_trans_90)
>>> <Vector2 (1.0, 0.0)>
```

## *transform(vector2d, angle_radians, displacement_x, displacement_y)*:
Given a vec.Vector2, an angle (in radians) and displacements on x and y
coordinates, returns a new vec.Vector2 instance equal to the original vector
rotated and translated by the given inputs.
``` python
from adr.helper_functions import transform
from vec import Vector2
import math
v1 = Vector2(0.5, -0.1)
v1_new = transform(v1, math.radians(45) 0.5, 0.1)
print(v1_new)
>>> <Vector2 (1.0, 0.0)>
```
Notice the rotating operation hapens before the translation, and they not commute.

## *component_vector_in_absolute_frame(vector, component)*:
This function is an abstraction of the transform function for components. One
can use it to get the absolute coordinates of a vector in the component
reference frame. I
``` python
from adr.helper_functions import component_vector_in_absolute_frame
from adr.Components import FreeBody
from adr.World import Ambient
from vec import Vector2
import math

env = Ambient()
plane = FreeBody(
    name='plane',
    type='vehicle',
    mass=2.0,
    position_cg=Vector2(x=-0.05, y=0),
    pitch_rot_inertia=30.0,
    ambient=env
)
plane.position = Vector2(20, 5)
plane.angle = math.radians(20)

v1_in_plane = Vector2(2.0, 0)
v1_in_absolute = component_vector_in_absolute_frame(v1_in_plane, plane)
print(v1_in_absolute)
>>> <Vector2 (21.879385241571818, 5.684040286651338)>
```

## *component_vector_coords_in_absolute_frame(vector_origin, vector, component)*:
This function is similar to component_vector_in_absolute_frame, but it's goal is
to return vectors in the component frame that have it's origin different from
the component's origin.
``` python
from adr.helper_functions import component_vector_coords_in_absolute_frame
from adr.Components import FreeBody
from adr.World import Ambient
from vec import Vector2
import math

env = Ambient()
plane = FreeBody(
    name='plane',
    type='vehicle',
    mass=2.0,
    position_cg=Vector2(x=-0.05, y=0),
    pitch_rot_inertia=30.0,
    ambient=env
)
plane.position = Vector2(20, 5)
plane.angle = math.radians(0)

v1_origin_in_plane = Vector2(0, 1.0)
v1 = Vector2(3, 0)
x0, y0, x, y = component_vector_coords_in_absolute_frame(v1_origin_in_plane, v1, plane)
print(x0, y0, x, y)
>>> 20.0 6.0 23.0 6.0
```
