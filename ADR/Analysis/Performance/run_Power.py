from ADR import parameters
from ADR.Components.Plane import Plane
from ADR.Analysis.Performance.Power import Power

from matplotlib import pyplot as plt


def plot_power_curves(power_analysis):

    fig1, ((ax1, ax2, ax3, ax4)) = plt.subplots(1, 4)

    ax1.plot(power_analysis.alpha_df, label="Alpha")
    ax1.grid()
    ax1.legend()

    ax2.plot(power_analysis.thrust_required_df, label="Thrust required")
    ax2.plot(power_analysis.thrust_available_df, label="Thrust available")
    ax2.grid()
    ax2.legend()

    ax3.plot(power_analysis.power_required_df, label="Power required")
    ax3.plot(power_analysis.power_available_df, label="Power available")
    ax3.grid()
    ax3.legend()

    ax4.plot(power_analysis.power_excess_df, label="Power excess")
    ax4.plot(power_analysis.power_excess_df, label="Power excess")
    ax4.grid()
    ax4.legend()


def power_curves(mtow, plot=True):
    plane_parameters = parameters.get_plane_parameters()
    performance_data = parameters.get_performance_parameters()

    plane = Plane(plane_parameters)
    plane.mtow = mtow
    power_analysis = Power(plane, performance_data)
    plane.show_plane()

    if plot == True:
        print("V_max : ", plane.V_max)
        print("V_min : ", plane.V_min)
        plot_power_curves(power_analysis)
        plt.show()


if __name__ == "__main__":
    power_curves(mtow=18.299999999999994)
