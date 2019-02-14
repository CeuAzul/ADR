from matplotlib import pyplot as plt
from scipy import interpolate
from scipy.optimize import root_scalar

from ADR.Analysis.Stability.FlightStability import FlightStability
from ADR.Analysis.Stability.FlightStability.FlightStability import FlightStability
from ADR.Components.Plane import Plane
from ADR.Core.import_functions import import_x5_aerodynamic_data


def find_root(x_axis, y_axis, extremes):
    intepolated = interpolate.interp1d(x_axis, y_axis['CM'])
    data = root_scalar(intepolated, bracket=extremes, method="bisect")
    return data.root


# wing 1
clw_wh, cdw_wh, cmw_wh = import_x5_aerodynamic_data('World/References/X5_Stability/', 'Asa.txt')
cmw = -0.32

# tail
clt_wh, cdt_wh, cmt_wh = import_x5_aerodynamic_data('World/References/X5_Stability/', 'Profundor.txt')
cmt = 0.092

# Aviao
clp_wh, cdp_wh, cmp_wh = import_x5_aerodynamic_data('World/References/X5_Stability/', 'Aviao.txt')

plane_type = 'biplane'

plane_data = {
    # wing1
    "wing1_x": 0,
    "wing1_y": 0,
    "wing1_z": 0,
    "wing1_airfoil1": "s1223",
    "wing1_airfoil2": "s1223",
    "wing1_span1": 1.8,
    "wing1_span2": 0,
    "wing1_chord1": 0.25,
    "wing1_chord2": 0.25,
    "wing1_chord3": 0,
    "wing1_twist1": 0,
    "wing1_twist2": 0,
    "wing1_twist3": 0,
    "wing1_incidence": 0,

    # For FlightStability - momentary
    "wing1_area": 0.45,
    "wing1_CL_alpha": clw_wh,
    "wing1_CD_alpha": cdw_wh,
    "wing1_CM_ca": cmw,
    "wing1_X_CA": -0.0625,
    "wing1_Y_CA": 0,
    "wing1_stall_min": -20,
    "wing1_stall_max": 20,


    # wing2
    "wing2_x": 0,
    "wing2_y": 0,
    "wing2_z": 0,
    "wing2_airfoil1": "s1223",
    "wing2_airfoil2": "s1223",
    "wing2_span1": 1.8,
    "wing2_span2": 0,
    "wing2_chord1": 0.25,
    "wing2_chord2": 0.25,
    "wing2_chord3": 0,
    "wing2_twist1": 0,
    "wing2_twist2": 0,
    "wing2_twist3": 0,
    "wing2_incidence": 0,

    # For FlightStability - momentary
    "wing2_area": 0.45,
    "wing2_CL_alpha": clw_wh,
    "wing2_CD_alpha": cdw_wh,
    "wing2_CM_ca": cmw,
    "wing2_X_CA": -0.0625,
    "wing2_Y_CA": 0,
    "wing2_stall_min": -20,
    "wing2_stall_max": 20,

    # hs
    "hs_x": 0,
    "hs_y": 0,
    "hs_z": 0,
    "hs_airfoil1": "s1223",
    "hs_airfoil2": "s1223",
    "hs_span1": 0.47,
    "hs_span2": 0,
    "hs_chord1": 0.2,
    "hs_chord2": 0.155,
    "hs_chord3": 0,
    "hs_twist1": 0,
    "hs_twist2": 0,
    "hs_twist3": 0,
    "hs_incidence": 0,

    # For FlightStability - momentary
    "hs_area": 0.083,
    "hs_CL_alpha": clt_wh,
    "hs_CD_alpha": cdt_wh,
    "hs_CM_ca": cmt,
    "hs_X_CA": -0.7625 - 0.0725,
    "hs_Y_CA": 0,
    "hs_stall_min": -20,
    "hs_stall_max": 20,

    # motor
    "static_thrust": 45,
    "linear_decay_coefficient": 1.28,

    # cg
    "cg_x": -0.0725,
    "cg_y": -0.01
}

plane = Plane(plane_data)

flight_stability = FlightStability("monoplane", plane)
CM_plane_on_CG = flight_stability.CM_plane_CG()
static_margin = flight_stability.static_margin()

flight_stability.plane.show_plane()

# CM_plane_root = find_root(flight_stability.alpha_plane_range,
#                           CM_plane_on_CG,
#                           [flight_stability.plane_stall_min,
#                            flight_stability.plane_stall_max])

# print("Plane trims for alpha = {} degrees".format(round(CM_plane_root, 2)))

#print("wing1.Cl_alpha", flight_stability.wing1.CL_alpha)
#print("wing1.dCl_dalpha", flight_stability.wing1.dCL_dalpha)

plt.figure(1)
plt.grid()
plt.xlabel("Alpha")
plt.ylabel("CM on CG")
plt.title("Momentum coeficients on CG")
plt.plot(flight_stability.wing1.CM_alpha_CG, label="Wing1")
if plane_type == 'biplane':
    plt.plot(flight_stability.wing2.CM_alpha_CG, label="Wing2")
plt.plot(flight_stability.hs.CM_alpha_CG, label="Tail")
plt.plot(CM_plane_on_CG, label="Plane")
plt.legend()

plt.figure(2)
plt.grid()
plt.xlabel("Alpha")
plt.ylabel("SM")
plt.title("Static Margin")
plt.plot(static_margin)

plt.show()
