"""
Origem: Bordo de ataque da asa raiz
"""

# Descobre o intervalo aceitavel de posicionamento do CG
import math
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from scipy import interpolate
from scipy.optimize import root_scalar

from ADR.Components.Aerodynamic_components.Wing import Wing
from ADR.Components.Aerodynamic_components.HS import HS
from ADR.Components.References.Static_margin import SM
from ADR.Analysis.Stability.Flight_stability.Momentum_CG import wing_momentum
from ADR.Analysis.Stability.Flight_stability.Momentum_CG import tail_momentum
from ADR.Components.Points.CG import CG
from ADR.Core.import_functions import import_x5_aerodynamic_data

### inputs variáveis
# wing 1
clw_wh, cdw_wh, cmw_wh = import_x5_aerodynamic_data('World/References/X5_Stability/', 'Asa.txt')
cmw = -0.32

# tail
clt_wh, cdt_wh, cmt_wh = import_x5_aerodynamic_data('World/References/X5_Stability/', 'Profundor.txt')
cmt = 0.092

# Aviao
clp_wh, cdp_wh, cmp_wh = import_x5_aerodynamic_data('World/References/X5_Stability/', 'Aviao.txt')

# Angulos de ataque a serem usados
alpha_graus_wh = clp_wh.index.values

# --- Inputs --- #

wing1 = Wing({
    "x": 0,
    "y": 0,
    "z": 0,
    "airfoil1": "s1223", "airfoil2": "s1223",
    "CL_alpha": clw_wh, "CD_alpha": cdw_wh, "CM_alpha": cmw,
    "span1": 1.8, "span2": 0,
    "chord1": 0.25, "chord2": 0.25, "chord3": 0,
    "area": 0.45,
    "twist1": 0, "twist2": 0, "twist3": 0,
    "X_CA": 0.0625,
    "H_CA": 0,
    "incidence": 0,
    "stall_min": -20,
    "stall_max": 20
})

wing2 = wing1

hs = HS({
    "x": 0,
    "y": 0,
    "z": 0,
    "airfoil1": "s1223", "airfoil2": "s1223",
    "CL_alpha": clt_wh, "CD_alpha": cdt_wh, "CM_alpha": cmt,
    "span1": 0.47, "span2": 0,
    "chord1": 0.2, "chord2": 0.155, "chord3": 0,
    "area": 0.083,
    "twist1": 0, "twist2": 0, "twist3": 0,
    "X_CA": 0.7625,
    "H_CA": 0.1,
    "incidence": 0,
    "stall_min": -20,
    "stall_max": 20
})

cg = CG(0.0725, 0.022)

# ------ #


def toRad(graus):
    return [(i * math.pi / 180) for i in graus]

# ------ #


def sepDictionary(d):
    lists = sorted(d.items())
    x, y = zip(*lists)
    return x, y

# ------ Analise ------ #


def flight_stability(plane_type):

    alpha_wing1_range = range(wing1.stall_min, wing2.stall_max + 1)
    alpha_tail_range = range(hs.stall_min, hs.stall_max + 1)

    plane_stall_min = max(hs.stall_min, wing1.stall_min)
    plane_stall_max = min(hs.stall_max, wing1.stall_max)
    alpha_plane_range = range(plane_stall_min, plane_stall_max + 1)

    CM_alpha_CG_tail = {}
    CM_alpha_CG_wing = {}
    CM_alpha_CG_plane = {}
    _SM = []
    status_CM_alpha = {}
    status_ME = {}

    print("Tipo de aviao = ", plane_type)
    print("X_CG = ", cg.x)
    print("H_CG = ", cg.h)
    print()

    print("wing1")
    # print("\twing1.CL_alpha = ", wing1.CL_alpha)
    # print("\twing1.CD_alpha = ", wing1.CD_alpha)
    # print("\twing1.CM_alpha = ", wing1.CM_alpha)
    print("\twing1.area = ", wing1.area)
    print("\twing1.chord1 = ", wing1.chord1)
    print("\twing1.X_CA = ", wing1.CA.x)
    print("\twing1.H_CA = ", wing1.CA.h)
    print()

    print("hs")
    # print("\ths.CL_alpha = ", hs.CL_alpha)
    # print("\ths.CD_alpha = ", hs.CD_alpha)
    # print("\ths.CM_alpha = ", hs.CM_alpha)
    print("\ths.area = ", hs.area)
    print("\ths.chord1 = ", hs.chord1)
    print("\ths.X_CA = ", hs.CA.x)
    print("\ths.H_CA = ", hs.CA.h)
    print()

    print("alpha_plane_range = ", alpha_plane_range, "\n")

    for alpha_plane in alpha_plane_range:
        wing1.attack_angle = wing2.attack_angle = hs.attack_angle = float(alpha_plane)

        # Getting CM_alpha of wing1
        #wings_m = wing_momentum(plane_type, wing1, wing2, cg, alpha_plane)
        CM_alpha_CG_wing[wing1.attack_angle] = wing1.moment_on_CG(wing1, wing1, cg, alpha_plane)

        # Getting CM_alpha of tail
        #tail_m = tail_momentum(wing1, hs, cg, alpha_plane)
        CM_alpha_CG_tail[hs.attack_angle] = hs.moment_on_CG(hs, wing1, cg, alpha_plane)

        # Summing CM of tail with CM of wing per each alpha
        # Getting CM_alpha of plane
        CM_alpha_CG_plane[alpha_plane] = CM_alpha_CG_wing[alpha_plane] + CM_alpha_CG_tail[alpha_plane]

        # Calculating Static Margin for each alpha
        """sm = SM(plane_type, wing1, wing2, hs,
                alpha_plane,
                CM_alpha_CG_plane[alpha_plane])"""

        #_SM.append(sm.SM)

    #wing1.CM_alpha_CG = pd.DataFrame.from_dict(CM_alpha_CG_wing, orient="index", columns=["CM"]))
# ------- Results ------- #

    """print("alpha_plane_range", alpha_plane_range)
    print("CM_alpha_CG_wing[i]", CM_alpha_CG_wing)
    print("CM_alpha_CG_tail[i]", CM_alpha_CG_tail)
    print("CM_alpha_CG_plane[i]", CM_alpha_CG_plane)
    print()"""

    CM_alpha_CG_plane_interp = interpolate.interp1d(alpha_plane_range, sepDictionary(CM_alpha_CG_plane)[1])
    CM_alpha_CG_plane_root = root_scalar(CM_alpha_CG_plane_interp, bracket=[plane_stall_min, plane_stall_max], method="bisect")
    print("Plane trims for alpha(degrees) = ", CM_alpha_CG_plane_root.root)

    """plt.figure(5)
    plt.grid()
    plt.title("Wing1")
    plt.plot(alpha_wing1_range, wing1.CL_alpha, label="CL")
    plt.plot(alpha_wing1_range, wing1.CD_alpha, label="CD")
    plt.plot(alpha_wing1_range, wing1.dCL_dalpha, label="dCL")
    plt.plot(alpha_wing1_range, wing1.dCD_dalpha, label="dCD")
    plt.legend()

    plt.figure(4)
    plt.grid()
    plt.title("Tail")
    plt.plot(alpha_tail_range, hs.CL_alpha, label="CL")
    plt.plot(alpha_tail_range, hs.CD_alpha, label="CD")
    plt.plot(alpha_tail_range, hs.dCL_dalpha, label="dCL")
    plt.plot(alpha_tail_range, hs.dCD_dalpha, label="dCD")
    plt.legend()"""

    plt.figure(3)
    plt.grid()
    plt.xlabel("Alpha angle of component")
    plt.ylabel("CM on CG")
    plt.title("Momentum coeficient of component on CG")
    a = sepDictionary(CM_alpha_CG_wing)
    plt.plot(a[0], a[1], label="CM_alpha_CG_wing")
    a = sepDictionary(CM_alpha_CG_tail)
    plt.plot(a[0], a[1], label="CM_alpha_CG_tail")
    a = sepDictionary(CM_alpha_CG_plane)
    plt.plot(a[0], a[1], label="CM_alpha_CG_plane")
    plt.legend()

    """plt.figure(2)
    plt.grid()
    plt.xlabel("Alpha angle of plane")
    plt.ylabel("SM")
    plt.title("SM for different attack angle of plane")
    plt.plot(alpha_plane_range, _SM)"""

    plt.show()


# Chama flight_stability
flight_stability("monoplane")
