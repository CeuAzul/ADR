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
