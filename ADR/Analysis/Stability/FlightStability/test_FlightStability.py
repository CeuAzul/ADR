from matplotlib import pyplot as plt
from scipy import interpolate
from scipy.optimize import root_scalar

from ADR import parameters
from ADR.Components.Plane import Plane
from ADR.Analysis.Stability.FlightStability.FlightStability import FlightStability
from ADR.Components.Points.CG import CG
import numpy as np

def find_root(x_axis, y_axis, extremes):
    intepolated = interpolate.interp1d(x_axis, y_axis['CM'])
    data = root_scalar(intepolated, bracket=extremes, method="bisect")
    return data.root

def plot_stability_data():

    fig1, ((ax1, ax2)) = plt.subplots(1, 2)

    ax1.set_xlabel("Alpha")
    ax1.set_ylabel("CM on CG")
    ax1.set_title("Momentum coeficients on CG")

    ax1.plot(flight_stability.wing1.CM_alpha_CG, label="Wing1")
    if flight_stability.plane.plane_type == 'biplane':
        ax1.plot(flight_stability.wing2.CM_alpha_CG, label="Wing2")
    for hs_incidence in flight_stability.hs.get_alpha_range():
        ax1.plot(CM_plane_on_CG_fixed[hs_incidence])   # Ploting for cg in first position(cg1)
    ax1.grid()
    ax1.legend()

    ax2.set_xlabel("Alpha")
    ax2.set_ylabel("SM")
    ax2.set_title("Static Margin")
    ax2.plot(SM_alpha_df)     # Ploting for cg in first position(cg1)
    ax2.grid()
    ax2.legend()

    plt.show()

if __name__ == "__main__":
    plane_data = parameters.plane_data()

    plane = Plane(plane_data)
    flight_stability = FlightStability(plane)

    cg = CG({"x": -0.0725, "z": -0.1})
    CM_plane_on_CG_fixed = flight_stability.CM_plane_CG(cg)

    SM_alpha_df = flight_stability.static_margin()

    # cg_x_range = [round(i, 3) for i in np.linspace(-0.05, -0.1, 10)]
    # cg_z_range = [round(i, 3) for i in np.linspace(-0.01, 0.01, 10)]
    # CM_plane_on_CG, SM_plane_on_CG = flight_stability.vary_CG(cg_x_range, cg_z_range)

    plot_stability_data()

    #flight_stability.plane.show_plane()

    # hs_incidence = 0
    # CM_plane_root = find_root(flight_stability.alpha_plane_range,
    #                         CM_plane_on_CG[hs_incidence],
    #                         [flight_stability.plane_stall_min,
    #                         flight_stability.plane_stall_max])

    # print("With hs.incidence = {}, plane trims for alpha_plane = {} degrees".format(hs_incidence, round(CM_plane_root, 2)))