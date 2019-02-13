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
    "X_CA": -0.0625,
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
    "X_CA": -0.7625-0.0725,
    "H_CA": 0,
    "incidence": 0,
    "stall_min": -20,
    "stall_max": 20
})

cg = CG(-0.0725, -0.01)

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

    for alpha_plane in alpha_plane_range:

        wing1.attack_angle = wing2.attack_angle = float(alpha_plane)
        hs.attack_angle = -float(alpha_plane)

        # Getting CM_alpha of wing1
        CM_alpha_CG_wing[alpha_plane] = wing1.moment_on_CG("wing", wing1, wing1, cg, alpha_plane)

        # Getting CM_alpha of tail
        CM_alpha_CG_tail[alpha_plane] = hs.moment_on_CG("hs", hs, wing1, cg, alpha_plane)

    for alpha_plane in alpha_plane_range:

        # Summing CM of tail with CM of wing per each alpha
        # Getting CM_alpha of plane
        CM_alpha_CG_plane[alpha_plane] = CM_alpha_CG_wing[alpha_plane] + CM_alpha_CG_tail[alpha_plane]

        # Calculating Static Margin for each alpha
        """sm = SM(plane_type, wing1, wing2, hs,
                alpha_plane,
                CM_alpha_CG_plane[alpha_plane])"""

        #_SM.append(sm.SM)
    wing1.CM_alpha_CG = pd.DataFrame.from_dict(CM_alpha_CG_wing, orient="index", columns=["CM"])
    wing1.CM_alpha_CG.index.name = 'alpha'

    hs.CM_alpha_CG = pd.DataFrame.from_dict(CM_alpha_CG_tail, orient="index", columns=["CM"])
    hs.CM_alpha_CG.index.name = 'alpha'

    CM_alpha_CG_plane_obj = pd.DataFrame.from_dict(CM_alpha_CG_plane, orient="index", columns=["CM"])
    CM_alpha_CG_plane_obj.index.name = 'alpha'

# ------- Results ------- #

    CM_alpha_CG_plane_interp = interpolate.interp1d(alpha_plane_range, CM_alpha_CG_plane_obj['CM'])
    CM_alpha_CG_plane_root = root_scalar(CM_alpha_CG_plane_interp, bracket=[plane_stall_min, plane_stall_max], method="bisect")
    print("Plane trims for alpha = {} degrees".format(CM_alpha_CG_plane_root.root))

    plt.figure(3)
    plt.grid()
    plt.xlabel("Alpha")
    plt.ylabel("CM on CG")
    plt.title("Momentum coeficients on CG")
    plt.plot(wing1.CM_alpha_CG, label="Wing")
    plt.plot(hs.CM_alpha_CG, label="Tail")
    plt.plot(CM_alpha_CG_plane_obj, label="Plane")
    plt.legend()

    plt.show()

# Chama flight_stability
flight_stability("monoplane")
