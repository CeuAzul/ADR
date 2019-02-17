from matplotlib import pyplot as plt
from scipy import interpolate
from scipy.optimize import root_scalar

from ADR.Analysis.Stability.FlightStability import FlightStability
from ADR.Analysis.Stability.FlightStability.FlightStability import FlightStability
from ADR.Components.Plane import Plane
from ADR.Components.Points.CG import CG
import numpy as np


def find_root(x_axis, y_axis, extremes):
    intepolated = interpolate.interp1d(x_axis, y_axis['CM'])
    data = root_scalar(intepolated, bracket=extremes, method="bisect")
    return data.root


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

    "static_thrust": 45,
    "linear_decay_coefficient": 1.28,

    "Iyy_TPR": 0.114,
    "CD_tp": 0.02,
    "CD_fus": 0.02,
    "u_k": 0.05
}

plane = Plane(plane_data)

flight_stability = FlightStability(plane)

cg_x_range = [round(i, 3) for i in np.linspace(-0.05, -0.1, 10)]
cg_z_range = [round(i, 3) for i in np.linspace(-0.01, 0.01, 10)]
CM_plane_on_CG, SM_plane_on_CG = flight_stability.vary_CG(cg_x_range, cg_z_range)

#flight_stability.plane.show_plane()

# hs_incidence = 0
# CM_plane_root = find_root(flight_stability.alpha_plane_range,
#                         CM_plane_on_CG[hs_incidence],
#                         [flight_stability.plane_stall_min,
#                         flight_stability.plane_stall_max])

# print("With hs.incidence = {}, plane trims for alpha_plane = {} degrees".format(hs_incidence, round(CM_plane_root, 2)))

cg = CG({"x": -0.0725, "z": -0.1})
CM_plane_on_CG_fixed = flight_stability.CM_plane_CG(cg)

plt.figure(1)
plt.grid()
plt.xlabel("Alpha")
plt.ylabel("CM on CG")
plt.title("Momentum coeficients on CG")
plt.legend()

# plt.plot(flight_stability.wing1.CM_alpha_CG, label="Wing1")
# if plane_type == 'biplane':
#     plt.plot(flight_stability.wing2.CM_alpha_CG, label="Wing2")
# plt.plot(flight_stability.hs.CM_alpha_CG, label="Tail")

for hs_incidence in flight_stability.hs.get_alpha_range():
    plt.plot(CM_plane_on_CG_fixed[hs_incidence])   # Ploting for cg in first position(cg1)

plt.figure(2)
plt.grid()
plt.xlabel("Alpha")
plt.ylabel("SM")
plt.title("Static Margin")
plt.plot(SM_plane_on_CG["cg1"])     # Ploting for cg in first position(cg1)

plt.show()
