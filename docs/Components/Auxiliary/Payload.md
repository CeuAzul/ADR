# Payload

Payload is a class created to act as a variable-mass container. Currently it is simple an AttachedComponent with the type 'payload'. 

## Instantiation
To instantiate a Payload one can pass the same arguments used to instantiate an AttachedComponent:

``` python
import math
from vec import Vector2

from adr.Components.Auxiliary import Payload

main_payload = Payload(
    name='main_payload',
    mass=9.2,
    relative_position=Vector2(-0.2, 0),
    relative_angle=math.radians(0)
)

print(main_payload.type)
>>> payload
```
