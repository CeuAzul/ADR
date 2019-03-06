from ADR import parameters, my_own_parameters
from ADR.Core.insert_genes import generate_forced_parameters
from ADR.Components.Plane import Plane
from ADR.Analysis.Performance.Power import Power

from matplotlib import pyplot as plt

def plot_power_curves(power_analysis):

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

def power_curves(mtow, genes, plot=True, use_own_parameters=False, use_genes=True):
    if use_genes:
        forced_parameters = generate_forced_parameters(genes)
    else:
        forced_parameters = {}

    if use_own_parameters:
        plane_parameters = my_own_parameters.plane_parameters(forced_parameters)
        performance_data = my_own_parameters.performance_parameters(forced_parameters)
    else:
        plane_parameters = parameters.plane_parameters(forced_parameters)
        performance_data = parameters.performance_parameters(forced_parameters)

    plane = Plane(plane_parameters)
    plane.mtow = mtow
    power_analysis = Power(plane, performance_data)
    plane.show_plane()

    if plot == True:
        print('V_max : ', plane.V_max)
        print('V_min : ', plane.V_min)
        plot_power_curves(power_analysis)
        plt.show()

if __name__ == "__main__":
    power_curves(mtow=18.299999999999994, genes=[0.6368717909213074, 0.49634100006739956, 0.4916183010303584, 0.8680241758171354, 0.38362358047862344, 0.7093876027664122, 0.0, 0.7708603646630342, 0.03795404093558552])