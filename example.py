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
