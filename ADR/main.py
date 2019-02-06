# Example of plane instantiation and data utilization

# Import Plane module. It will take care of most imports (wing, hs, vs, motor, etc)
from ADR.Components.Plane import Plane


# Generate dictionary with plane data
# Ideally you should give all data (like on
# this example). If you don't use some of it, just give
# dummy data (zeros or anything).

plane_data = {
    "wing_x": 1,
    "wing_y": 2,
    "wing_z": 3,
    "wing_airfoil1": "s1223",
    "wing_airfoil2": "s1223",
    "wing_span1": 0.8,
    "wing_span2": 0.4,
    "wing_chord1": 0.45,
    "wing_chord2": 0.35,
    "wing_chord3": 0.20,
    "wing_twist1": 0,
    "wing_twist2": 0,
    "wing_twist3": -5,
    "wing_incidence": 3,

    "hs_x": 1,
    "hs_y": 2,
    "hs_z": 3,
    "hs_airfoil1": "s1223",
    "hs_airfoil2": "s1223",
    "hs_span1": 0.2,
    "hs_span2": 0.1,
    "hs_chord1": 0.15,
    "hs_chord2": 0.15,
    "hs_chord3": 0.10,
    "hs_twist1": 0,
    "hs_twist2": 0,
    "hs_twist3": -5,
    "hs_incidence": 0,

    "vs_x": 1,
    "vs_y": 2,
    "vs_z": 3,
    "vs_airfoil1": "s1223",
    "vs_airfoil2": "s1223",
    "vs_span1": 0.1,
    "vs_span2": 0.1,
    "vs_chord1": 0.2,
    "vs_chord2": 0.2,
    "vs_chord3": 0.1,
    "vs_twist1": 0,
    "vs_twist2": 0,
    "vs_twist3": 0,
    "vs_incidence": 0,

    "static_thrust": 45,
    "linear_decay_coefficient": 1.28
}

# Instantiate plane object using plane_data
plane = Plane(plane_data)

# Print wing area
print(plane.wing.area)

# Print motor thrust at 13m/s
print("Motor thrust at 13m/s: {}".format(plane.motor.thrust(13)))

# Print drag of the vertical stabilizer at rho=1.225kg/m³, velocity=13m/s and alpha=6deg
print(plane.hs.drag(1.225, 13, 6))
