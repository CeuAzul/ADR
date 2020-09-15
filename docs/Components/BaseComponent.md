# Base Component

The base component is the fountain where ADR drinks from. Its idea is to provide
several properties and methods that are necessary for both AttachedComponent and
FreeBody. Usually the final user of ADR won't use BaseComponent directly, using instead the other two.

BaseComponent implements the idea of child components (with the children dictionary), methods for dealing with its state and the state of its children, methods for calculating the forces and moments on any component based on the loads in the component itself and its children, among other things.

## Instantiation
One can instantiate a BaseComponent by passing three parameters: *name*, *type* and *mass*. Notice that all parameters should be passed as keyword arguments (eg.: name="plane").
``` python
from adr.Components import BaseComponent

base_component = BaseComponent(
    name='component',
    type='generic_component',
    mass=3.4)

print(base_component)
>>> BaseComponent(name='component', type='generic_component', mass=3.4, children={}, external_forces={}, external_moments={})
```

The other attributes (children, external_forces and external_moments) should not be passed during instantiation, but with specific methods.

## *reset_state* method
The *reset_state* method will call the *reset_children_state* method.
It exists so the classes inheriting from BaseComponent can always call it's superclass *reset_state* method, ultimately calling the *reset_children_state* method, which will reset all nested components.

## *reset_children_state* method
The *reset_children_state* method will call the *reset_state* method of all the components listed on the children dictionary.

## append_child method
This method is responsible for adding a child to a component
``` python
child_component = BaseComponent("wing1", "wing", 1.1)
base_component.append_child(child_component)

print(base_component.children)
>>> {'wing1': BaseComponent(name='wing1', type='wing', mass=1.1, children={}, external_forces={}, external_moments={})}

print(base_component.wing1)
>>> BaseComponent(name='wing1', type='wing', mass=1.1, children={}, external_forces={}, external_moments={})
```
## angle_of_attack property
This property calculates the angle of attack of the plane
```python
freebody_component = FreeBody(
    name='component',
    type='generic_component',
    mass=3.4,
    position_cg=Vector2(-0.7, 0.2),
    pitch_rot_inertia=30.0,
    ambient=Ambient()
)

attached_component = AttachedComponent(
    name='attached_component',
    type='generic_attached_component',
    mass=1.4,
    relative_position=Vector2(-0.4, 0.1),
    relative_angle=math.radians(9)
)

attached_component.set_parent(freebody_component)
freebody_component.velocity = Vector2(r=12, theta=math.radians(5))

print(math.degrees(freebody_component.angle_of_attack))
>>> -5.0

print(math.degrees(attached_component.angle_of_attack))
>>> 4.0
```

## empty_mass property
This property returns the total mass of the nested components, excluding payload components
```python
print(base_component.empty_mass)
>>> 4.5
```
## nested_components property
This property returns a dictionary with the hierarchical relationship of each component
```python
print(base_component.nested_components)
>>> {'component': BaseComponent(name='component', type='generic_component', mass=3.4, children={'wing1': BaseComponent(name='wing1', type='wing', mass=1.1, children={}, external_forces={}, external_moments={})}, external_forces={}, external_moments={}), 'wing1': BaseComponent(name='wing1', type='wing', mass=1.1, children={}, external_forces={}, external_moments={})}
```
## add_external_force_function
This method is responsible for appending an external force function to the component. The force function returns a force vector and an application point.
```python
def force1():
    mag = 10
    ang = math.radians(45)
    force_point = Vector2(-10, 0)
    force1 = Vector2(r=mag, theta=ang)
    return force1, force_point

base_component.add_external_force_function('force1', force1)

print(base_component.external_forces)
>>> {'force1': <function force1 at 0x0000025EBCAA8D30>}
```
## *add_external_moment_function*:
This method is responsible for appending an external moment function to the component. The appended function should return a float representing the magnitude of the moment.
```python
def moment1():
    moment1 = 13
    return moment1

base_component.add_external_moment_function('moment1', moment1)

print(base_component.external_moments)
>>> {'moment1': <function moment1 at 0x7ff87d8891f0>}
```

## *moment_from_external_moments* method:
Returns the resultant pitch moment from the moment functions appended to the
component. It does not include child's moments or moments from forces.
```python
def moment_from_drag():
    return 2

def moment_from_lift():
    return 5

freebody_component.add_external_moment_function('drag_moment', moment_from_drag)
freebody_component.add_external_moment_function('lift_moment', moment_from_lift)

print(freebody_component.external_moments)
>>> {'drag_moment': <function moment_from_drag at 0x7fe44b2861f0>, 
     'lift_moment': <function moment_from_lift at 0x7fe44af67550>}
print(freebody_component.moment_from_external_moments())
>>> 7.0
```

## *force_and_moment_from_external_forces* method:
Similar to moment_from_external_moments, but it returns both the resultant force
and the moment of the resultant force on a component (excluding children).
```python
def drag_force():
    return Vector2(-5, 0), Vector2(3, 2)

def lift_force():
    return Vector2(0, 50), Vector2(3, 2)

freebody_component.external_forces.pop('weight')
freebody_component.add_external_force_function('drag_force', drag_force)
freebody_component.add_external_force_function('lift_force', lift_force)

print(freebody_component.external_forces)
>>> {'drag_force': <function drag_force at 0x7f6fb6e561f0>,
     'lift_force': <function lift_force at 0x7f6f9f7d3310>}
print(freebody_component.force_and_moment_from_external_forces())
>>> (<Vector2 (-4.99999, 50)>, 160.0)
```
## *force_and_moment_from_children* method:
Returns the resultant force and moment from all the child components at its origin.

## *force_and_moment_at_component_origin* method:
Returns the resultant force and moment from itself and all the child components, at its origin.
