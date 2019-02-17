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

plane_data = {
    "plane_type": 'monoplane',

    "wing1_x": 0,
    "wing1_y": 0,
    "wing1_z": 0,
    "wing1_airfoil1_name": "s1223",
    "wing1_airfoil2_name": "s1223",
    "wing1_span1": 0.45,
    "wing1_span2": 0.45,
    "wing1_chord1": 0.25,
    "wing1_chord2": 0.25,
    "wing1_chord3": 0.25,
    "wing1_twist1": 0,
    "wing1_twist2": 0,
    "wing1_twist3": 0,
    "wing1_incidence": 0,
    "wing1_CM_ca": wing1_CM_ca,

    "wing2_x": 0,
    "wing2_y": 0,
    "wing2_z": 0.3,
    "wing2_airfoil1_name": "s1223",
    "wing2_airfoil2_name": "s1223",
    "wing2_span1": 0.45,
    "wing2_span2": 0.45,
    "wing2_chord1": 0.25,
    "wing2_chord2": 0.25,
    "wing2_chord3": 0.25,
    "wing2_twist1": 0,
    "wing2_twist2": 0,
    "wing2_twist3": 0,
    "wing2_incidence": 0,
    "wing2_CM_ca": wing2_CM_ca,

    "hs_x": -0.7,
    "hs_y": 0,
    "hs_z": 0,
    "hs_airfoil1_name": "s1223",
    "hs_airfoil2_name": "s1223",
    "hs_span1": 0.12,
    "hs_span2": 0.12,
    "hs_chord1": 0.2,
    "hs_chord2": 0.15,
    "hs_chord3": 0.10,
    "hs_twist1": 0,
    "hs_twist2": 0,
    "hs_twist3": 0,
    "hs_incidence": 0,
    "hs_CM_ca": hs_CM_ca,


    "vs_x": -0.7,
    "vs_y": 0,
    "vs_z": 0,
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

    "motor_x": 0.25,
    "motor_z": -0.05,
    "static_thrust": 45,
    "linear_decay_coefficient": 1.28,

    "Iyy_TPR": 0.114,
    "CD_tp": 0.02,
    "CD_fus": 0.02,
    "u_k": 0.05
}

plane = Plane(plane_data)

# Print wing area
print(plane.wing1.area)
print(plane.wing2.area)

# Print motor thrust at 13m/s
print("Motor thrust at 13m/s: {}".format(plane.motor.thrust(13)))

# Print drag of the vertical stabilizer at rho=1.225kg/m³, velocity=13m/s and alpha=6deg
# print(plane.hs.drag(1.225, 13, 6))
