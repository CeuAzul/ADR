from ADR import parameters
from ADR.Components.Plane import Plane
from ADR.Analysis.Performance.Takeoff import Takeoff
from matplotlib import pyplot as plt


def plot_takeoff_data(takeoff_analysis, mtow):

    fig1, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3)

    ax1.plot(takeoff_analysis.mass_dict[mtow]["N"], label="Normal")
    ax1.plot(takeoff_analysis.mass_dict[mtow]["L"], label="Lift")
    ax1.plot(takeoff_analysis.mass_dict[mtow]["L_w1"], label="Lift Wing1")
    ax1.plot(takeoff_analysis.mass_dict[mtow]["L_w2"], label="Lift Wing2")
    ax1.plot(takeoff_analysis.mass_dict[mtow]["L_hs"], label="Lift HS")
    ax1.grid()
    ax1.legend()

    ax2.plot(takeoff_analysis.mass_dict[mtow]["D"], label="Drag")
    ax2.plot(takeoff_analysis.mass_dict[mtow]["D_w1"], label="Drag Wing1")
    ax2.plot(takeoff_analysis.mass_dict[mtow]["D_w2"], label="Drag Wing2")
    ax2.plot(takeoff_analysis.mass_dict[mtow]["D_hs"], label="Drag HS")
    ax2.grid()
    ax2.legend()

    ax3.plot(takeoff_analysis.mass_dict[mtow]["M"], label="Moment")
    ax3.plot(takeoff_analysis.mass_dict[mtow]["M_w1"], label="Moment Wing1")
    ax3.plot(takeoff_analysis.mass_dict[mtow]["M_w2"], label="Moment Wing2")
    ax3.plot(takeoff_analysis.mass_dict[mtow]["M_hs"], label="Moment HS")
    ax3.grid()
    ax3.legend()

    ax4.plot(takeoff_analysis.mass_dict[mtow]["dTheta"], label="dTheta")
    ax4.grid()
    ax4.legend()

    ax5.plot(takeoff_analysis.mass_dict[mtow]
             ["incidence_hs"], label="HS incidence")
    ax5.plot(takeoff_analysis.mass_dict[mtow]["theta"], label="Theta")
    ax5.grid()
    ax5.legend()

    ax6.plot(takeoff_analysis.mass_dict[mtow]["dist_x"], label="Distance")
    ax6.plot(takeoff_analysis.mass_dict[mtow]["V_x"], label="Velocity")
    ax6.grid()
    ax6.legend()


def takeoff(plot=True):
    plane_parameters = parameters.get_plane_parameters()
    performance_data = parameters.get_performance_parameters()

    plane = Plane(plane_parameters)
    takeoff_analysis = Takeoff(plane, performance_data)
    mtow = takeoff_analysis.get_mtow()

    print("Final MTOW is {}".format(mtow))
    print("V_takeoff : ", plane.V_takeoff)

    if plot == True:
        plot_takeoff_data(takeoff_analysis, mtow)
        plt.show()


if __name__ == "__main__":
    takeoff()
