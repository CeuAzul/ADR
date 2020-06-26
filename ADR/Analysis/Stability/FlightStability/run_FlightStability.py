from matplotlib import pyplot as plt

# from scipy.optimize import root_scalar

from ADR import parameters
from ADR.Components.Plane import Plane
from ADR.Analysis.Stability.FlightStability.FlightStability import FlightStability


def plot_stability_data(flight_stability):

    fig1, ((ax1, ax2)) = plt.subplots(1, 2)

    ax1.set_xlabel("Alpha")
    ax1.set_ylabel("CM on CG")
    ax1.set_title("Momentum coeficients on CG")

    ax1.plot(flight_stability.wing1.CM_alpha_CG, label="Wing1")
    if flight_stability.plane.plane_type == "biplane":
        ax1.plot(flight_stability.wing2.CM_alpha_CG, label="Wing2")
    for hs_incidence in flight_stability.hs.incidence_range:
        ax1.plot(
            flight_stability.CM_alpha_CG_plane_each_hs_incidence[hs_incidence]
        )  # Ploting for cg in first position(cg1)
    ax1.grid()
    ax1.legend()

    ax2.set_xlabel("Alpha")
    ax2.set_ylabel("SM")
    ax2.set_title("Static Margin")
    # Ploting for cg in first position(cg1)
    ax2.plot(flight_stability.SM_alpha_df)
    ax2.grid()


if __name__ == "__main__":
    plane_data = parameters.plane_data()

    plane = Plane(plane_data)
    flight_stability = FlightStability(plane)

    plot_stability_data(flight_stability)
    plt.show()
