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

if __name__ == "__main__":
    plane_data = parameters.plane_data()

    plane = Plane(plane_data)
    flight_stability = FlightStability(plane)

    cg_x_range = [round(i, 3) for i in np.linspace(-0.05, -0.1, 10)]
    cg_z_range = [round(i, 3) for i in np.linspace(-0.01, 0.01, 10)]
    CM_plane_on_CG, SM_plane_on_CG = flight_stability.vary_CG(cg_x_range, cg_z_range)

    plot_stability_data()

    #flight_stability.plane.show_plane()

    # hs_incidence = 0
    # CM_plane_root = find_root(flight_stability.alpha_plane_range,
    #                         CM_plane_on_CG[hs_incidence],
    #                         [flight_stability.plane_stall_min,
    #                         flight_stability.plane_stall_max])

    # print("With hs.incidence = {}, plane trims for alpha_plane = {} degrees".format(hs_incidence, round(CM_plane_root, 2)))