# Example of plane instantiation and data utilization

# Import Plane module. It will take care of most imports (wing, hs, vs, motor, etc)
from ADR.Components.Plane import Plane
from ADR.Components.Aerodynamic_components.Airfoil import Airfoil

# Generate dictionary with plane data
# Ideally you should give all data (like on
# this example). If you don't use some of it, just give
# dummy data (zeros or anything).

wing1_CM_ca = -0.32
wing2_CM_ca = -0.32
hs_CM_ca = 0.092

plane_type = 'monoplane'

plane_data = {
    "wing1_x": 1,
    "wing1_y": 2,
    "wing1_z": 3,
    "wing1_airfoil1_name": "s1223",
    "wing1_airfoil2_name": "s1223",
    "wing1_span1": 0.7,
    "wing1_span2": 0.7,
    "wing1_chord1": 0.40,
    "wing1_chord2": 0.40,
    "wing1_chord3": 0.40,
    "wing1_twist1": 0,
    "wing1_twist2": 0,
    "wing1_twist3": 0,
    "wing1_incidence": 0,
    "wing1_CM_ca": wing1_CM_ca,

    "wing2_x": 1,
    "wing2_y": 2,
    "wing2_z": 3,
    "wing2_airfoil1_name": "s1223",
    "wing2_airfoil2_name": "s1223",
    "wing2_span1": 0.7,
    "wing2_span2": 0.7,
    "wing2_chord1": 0.40,
    "wing2_chord2": 0.40,
    "wing2_chord3": 0.40,
    "wing2_twist1": 0,
    "wing2_twist2": 0,
    "wing2_twist3": 0,
    "wing2_incidence": 0,
    "wing2_CM_ca": wing2_CM_ca,

    "hs_x": 1,
    "hs_y": 2,
    "hs_z": 3,
    "hs_airfoil1_name": "s1223",
    "hs_airfoil2_name": "s1223",
    "hs_span1": 0.2,
    "hs_span2": 0.1,
    "hs_chord1": 0.15,
    "hs_chord2": 0.15,
    "hs_chord3": 0.10,
    "hs_twist1": 0,
    "hs_twist2": 0,
    "hs_twist3": 0,
    "hs_incidence": 0,
    "hs_CM_ca": hs_CM_ca,


    "vs_x": 1,
    "vs_y": 2,
    "vs_z": 3,
    "vs_airfoil1_name": "s1223",
    "vs_airfoil2_name": "s1223",
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
print(plane.wing1.area)
print(plane.wing2.area)

# Print motor thrust at 13m/s
print("Motor thrust at 13m/s: {}".format(plane.motor.thrust(13)))

# Print drag of the vertical stabilizer at rho=1.225kg/m³, velocity=13m/s and alpha=6deg
# print(plane.hs.drag(1.225, 13, 6))
