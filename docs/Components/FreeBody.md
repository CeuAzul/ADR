# Free Body

Together with AttachedComponent, the FreeBody class is responsible for creating a network of nested components.

Any network of components should have a FreeBody object as its main parent, this is, all the other components should be instances of the AttachedComponent class (or a class that inherits from it) and nested under a FreeBody. This is necessary because when you ask for any state of a AttachedComponent that is dependent of its parent (eg.: angle), it will look at the value of its parent to calculate its own (eg.: ```self.angle = self.parent.angle + self.relative_angle```). If the parent is also an AttachedComponent, it will also look at its own parent and this will continue until it reaches the top component, that should be able to calculate its own value, not asking any parent. This component is the FreeBody.

The FreeBody class implements among other things the *position*, *angle*, *velocity* and *rot_velocity* states. The user can modify those directly, to represent a specific FreeBody state, or call the *move* method, which will calculate the forces and moments on the free body and modify the states accordingly.

## Instantiation
To instantiate a FreeBody one needs to pass the arguments of its parent class (*name*, *type* and *mass*) and also its own (*position_cg*, *pitch_rot_inertia* and *ambient*).

The *position_cg* property should be a 2D vector (using vec.Vector2 class) that represents the gravitational center position of the free body relative to its origin (arbitrary and defined by the user).

The *pitch_rot_inertia* property should be a float representing the rotating inertia of the free body along its pitch axis and will be used to calculate for pitch states (*rot_velocity* and *angle*).

The *ambient* property should be a instance of the Ambient class and which will be consulted for environment variables (eg.: air density and wind conditions). This ambient instance can be changed during analysis for variating environment conditions.

``` python
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

print(plane.ambient.air_density)
>>> 1.2920513674462337
```

## *reset_state* method
The *reset_state* method will reset all the component state variables (position, angle, velocity and rot_velocity), and call BaseComponent's *reset_state* after, which will reset the state of all child components.
``` python
plane.angle = math.radians(8)
print(math.degrees(plane.angle))
>>> 8.0
plane.reset_state()
print(math.degrees(plane.angle))
>>> 0.0
```

## *gravitational_center* property
This property returns the freebody gravitational center position
``` python
print(plane.gravitational_center)
>>> Vector2 (-0.05, 0)
```
## *move* method
This method moves the FreeBody instance according to free-body physical equations 
and the instance state, for a given time step.
``` python
def thrust_force():
    return Vector2(10, 0), Vector2(0.4, -0.1)

def lift_force():
    return Vector2(0, 50), Vector2(0.1, 0.2)

plane.add_external_force_function('thrust', thrust_force)
plane.add_external_force_function('lift', lift_force)

plane.mass = 4.0
plane.position = Vector2(10, 0)
plane.velocity = Vector2(2.5, 0)
plane.angle = math.radians(0)

plane.move(1.0)
print(plane.position)
>>> <Vector2 (15.0000025, 2.6933500000000006)>
print(plane.velocity)
>>> <Vector2 (5.000002500000001, 2.6933500000000006)>
print(math.degrees(plane.angle))
>>> 16.233804195373324

plane.move(1.0)
print(plane.position)
>>> <Vector2 (19.758483712364665, 8.471051772483769)>
print(plane.velocity)
>>> <Vector2 (4.7584812123646625, 5.777701772483768)>
print(math.degrees(plane.angle))
>>> 48.70141258611997
```

Notice that the quality of the output depends on the quality of the input. If
the force and moment functions are not representative, the moving method won't
deliver good results.