from matplotlib import pyplot as plt


def plot_aerodynamic_data(plane):

    fig1, ((ax1, ax2, ax3, ax4)) = plt.subplots(1, 4)

    ax1.set_xlabel("Alpha")
    ax1.set_ylabel("CL")
    ax1.set_title("CL x Alpha")
    ax1.plot(plane.CL_alpha)
    ax1.grid()

    ax2.set_xlabel("Alpha")
    ax2.set_ylabel("CD")
    ax2.set_title("CD x Alpha")
    ax2.plot(plane.CD_alpha)
    ax2.grid()

    ax3.set_xlabel("Alpha")
    ax3.set_ylabel("CL")
    ax3.set_title("CL x Alpha for surfaces")
    ax3.plot(plane.wing1.CL_alpha, label="Wing1")
    ax3.plot(plane.wing2.CL_alpha, label="Wing2")
    ax3.plot(plane.hs.CL_alpha, label="HS")
    ax3.grid()
    ax3.legend()

    ax4.set_xlabel("CD")
    ax4.set_ylabel("CL")
    ax4.set_title("CL x CD")
    ax4.plot(plane.CD_alpha["CD"], plane.CL_alpha["CL"])
    ax4.grid()
