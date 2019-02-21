from ADR import parameters
from ADR.Components.Plane import Plane
from ADR.Analysis.Performance.Power import Power

from matplotlib import pyplot as plt

def plot_power_curves():

    fig1, ((ax1, ax2, ax3, ax4)) = plt.subplots(1, 4)

    ax1.plot(power_analysis.alpha_df , label='Alpha')
    ax1.grid()
    ax1.legend()

    ax2.plot(power_analysis.thrust_required_df, label='Thrust required')
    ax2.plot(power_analysis.thrust_available_df, label='Thrust available')
    ax2.grid()
    ax2.legend()

    ax3.plot(power_analysis.power_required_df, label='Power required')
    ax3.plot(power_analysis.power_available_df, label='Power available')
    ax3.grid()
    ax3.legend()

    ax4.plot(power_analysis.power_excess_df, label='Power excess')
    ax4.plot(power_analysis.power_excess_df, label='Power excess')
    ax4.grid()
    ax4.legend()

    plt.show()

if __name__ == "__main__":
    plane_data = parameters.plane_data()
    performance_data = parameters.performance_data()

    plane = Plane(plane_data)
    power_analysis = Power(plane, performance_data)
    plot_power_curves()
