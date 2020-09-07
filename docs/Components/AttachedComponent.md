# AttachedComponent

AttachedComponent is the class where all the other components on ADR inherit from.
Together with the FreeBody class it allows one to create a complex network of components that interact to calculate their states.

An AttachedComponent will have properties that identify its parent component and its position and angle relative to this parent.

By definition an AttachedComponent should always have a parent component, as its states will be calculated using it (eg.: ```self.angle = self.parent.angle + self.relative_angle```). This parent component can be another AttachedComponent or a FreeBody. On the top of the component's network there should always be a FreeBody, where the main states (*position*, *angle*, *velocity* and *ambient*) will be set.

The AttachedComponent class implements three properties and a state, being those *parent*, *relative_position*, *relative_angle*, *velocity* and *actuation_angle*.

## Instantiation
To instantiate a AttacheComponent one needs to pass the arguments of its parent class (*name*, *type* and *mass*) and also its own (*relative_position* and *relative_angle*). The *parent* property is set with the special method *set_parent* afterwards.

The *relative_position* property should be a 2D vector (using vec.Vector2 class) that represents the position of the component's origin relative to its parent origin (both origins being arbitrary and defined by the user).

The *relative_angle* property should be a float representing the angle of the component relative to its parent, in radians and clockwise.

``` python
from adr.Components import FreeBody, AttachedComponent
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

wing = AttachedComponent(
    name='wing',
    type='wing',
    mass=0.3,
    relative_position=Vector2(x=-0.15, y=0.2),
    relative_angle=math.radians(6),
)

aileron = AttachedComponent(
    name='left_aileron',
    type='aileron',
    mass=0.02,
    relative_position=Vector2(x=-0.3, y=0),
    relative_angle=math.radians(4),
)

wing.set_parent(plane)
aileron.set_parent(wing)

print(math.degrees(wing.angle))
>>> 6.0
print(math.degrees(aileron.angle))
>>> 10.0

plane.angle = math.radians(5)
print(math.degrees(aileron.angle))
>>> 14.99999999999
```
## ambient property
This property returns the environment in which the component is located
```python
print(wing.ambient)
>>> adr.World.Ambient.Ambient object at 0x000001E4F70128E0
```

## velocity property
This property returns the speed of the component based on the speed of the parent component
```python
wing.set_parent(plane)
plane.velocity = Vector2(10, 20)

print(wing.velocity)
>>> Vector2 (10, 20)
```

## *reset_state* method
The *reset_state* method will reset all the component state variables (actuation_angle), and call BaseComponent's *reset_state* after, which will reset the state of all child components.
``` python
plane.angle = math.radians(8)
print(math.degrees(plane.angle))
>>> 8.0
plane.reset_state()
print(math.degrees(plane.angle))
>>> 0.0
```##Angle:
The property angle will return to you the angle that the given component is set.

Let's say we have a component 'Wing' attached to the body of the plane, that is set as a FreeBody Component called 'Plane'. The property angle will take in count the plane angle and the relative angle of the wing, just as shown in the example below:

``` python
env = Ambient()
plane = FreeBody(
    name='plane',
    type='vehicle',
    mass=2.0,
    angle = math.radians(3.2),
    position_cg=Vector2(x=-0.05, y=0),
    pitch_rot_inertia=30.0,
    ambient=env
)

wing = AttachedComponent(
    name='wing',
    type='wing',
    mass=0.3,
    relative_position=Vector2(x=-0.15, y=0.2),
    relative_angle = math.radians(1)
)

print(math.degrees(wing.angle))
>>> 4.2
```

If the given component has an actuation angle, the property will return the angle with the maximum actuation angle as well. 

Let's use another example to demonstrate that: an aileron is attached to the wing, with an actuation angle of 15 degrees and a relative angle of 0 degrees.

``` python
aileron = AttachedComponent(
    name='left_aileron',
    type='aileron',
    mass=0.02,
    relative_position=Vector2(x=-0.3, y=0),
    relative_angle=math.radians(0),
)

aileron.actuation_angle(math.radians(15))
aileron.set_parent(wing)
print(math.degrees(aileron.angle))
>>> 19.2
```

## Set_parent
The *set_parent* has already been used in the example above, but to give a further explanation, what the function does is to set a parent to the current component.

Note that if we try to set a parent to a component that has already a parent assigned it will return an error. In the example above, the aileron parent is the wing, see what happens if we try to set the plane as the aileron parent:

``` python 

aileron.set_parent(plane)
>>> raise Exception('Component already has a parent: wing')
```
