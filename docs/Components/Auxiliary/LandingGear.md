# LandingGear

LandingGear is a component created to be used for ground simulation situations. It simulates a dumped oscillator, this is, a dumped string-mass system.
Imagine you want to perform a simulation of a plane takeoff or landing. You need a component that interacts with the ground, generating reaction forces oposing the total weight of the body (normal reaction) and its velocity (friction force). LandingGear does that.

## Instantiation
To instantiate a LandingGear one can pass the same arguments used to instantiate an AttachedComponent, plus the following:
- height: used to calculate for the displacement of the spring
- spring_coeff: used to calculate the spring reaction
- dump_coeff: used to calculate the dumpener friction
- friction_coeff: used to calculate the friction of the wheels to the ground


``` python
import math
from vec import Vector2

from adr.Components.Auxiliary import LandingGear

main_landing_gear = LandingGear(
    name='main_landing_gear',
    relative_position=Vector2(x=-0.2, y=0),
    relative_angle=math.radians(0),
    mass=0.3,
    height=0.1,
    spring_coeff=1000,
    dump_coeff=50,
    friction_coeff=0.05
)
print(main_landing_gear.type)
>>> landing_gear
```

To simulate the behaviour of the landing gear, one needs to attach it to a FreeBody instance. Let's to that:

``` python
from adr.World import Ambient
from adr.Components import FreeBody

env = Ambient()
plane = FreeBody(
    name='plane',
    type='plane',
    mass=23.4,
    position_cg=Vector2(-0.2, 0.02),
    pitch_rot_inertia=5.2,
    ambient=env,
)

main_landing_gear.set_parent(plane)
```

And finally let's impose some state to the plane so the landing gear reactions can be calculated:

``` python
plane.velocity = Vector2(6, 0.4)
plane.position = Vector2(10, 0)

reaction, contact_point = main_landing_gear.gear_reaction()
print(reaction)
print(contact_point)
>>> <Vector2 (0, 80.0)>
>>> <Vector2 (0, -0.1)>

friction, contact_point = main_landing_gear.gear_friction()
print(friction)
print(contact_point)
>>> <Vector2 (-4.0, 0)>
>>> <Vector2 (0, -0.1)>
```

So one can see that when the airplane is at 0 m to the ground (maximum spring displacement) and with a 10 m/s velocity on the forward direction, there's a 80 N normal force oposing the weight and a 4 N friction force oposing the movement.