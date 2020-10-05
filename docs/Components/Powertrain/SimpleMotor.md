# Simple Motor

Simple Motor class is based on the class called "attatched component", and written over the Motor class. For the fact that it is an attatched component, it is needed to set a parent for it, and just like on attached component, all information from the parent will be taken in count on the children methods.

Besides that the class needs some inputs values from the user, such as:
* static_thrust
* linear_coefficient
* distance_origin_to_propeller

## *Thrust Center* _method_:

It's a property that returns a Vector2 with the values of the points where the thrust is applied.

As it is a Simple Motor, by default the force is applied on x in the distance from the origin to the propeller and in y, in 0 as it's seen in the example below:

```python
motor = SimpleMotor(
    name='attached_component',
    mass=1.4,
    relative_position=Vector2(-0.4, 0.1),
    relative_angle=math.radians(0),
    static_thrust = 78,
    linear_coefficient = -1,
    distance_origin_to_propeller = 0.3
)

env = Ambient()
plane = FreeBody(
    name='freebody',
    type='generic_freebody',
    mass=23.4,
    position_cg=Vector2(-0.2, 0.02),
    pitch_rot_inertia=5.2,
    ambient=env,
)

motor.set_parent(plane)

print(motor.thrust_center)
>>> Vector2(0.3, 0)
```
##*Get Thrust* method:

This methods is responsible for returning the magnitude value of the given thrust. To make the calculation, the method calls the function get_axial_thrust_from_linear_model, that takes into consideration the motor inputs, the environment variables, and the given velocity of the aircraft rotated to  the axial velocity, considering the angle of attack.

The method returns to vectors, one with the thrust magnitude and the other one with the thrust_center, that was calculated on the method before.

```python

thrust_magnitude, thrust_center = motor.get_thrust()

print(thrust_magnitude)
>>> Vector2(82.269378, 0)
print(thrust_center)
>>> Vector2(0.3, 0)
```

