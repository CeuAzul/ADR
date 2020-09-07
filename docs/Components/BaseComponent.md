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
