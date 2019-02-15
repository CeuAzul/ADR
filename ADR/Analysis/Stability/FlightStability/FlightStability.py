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

from ADR.Components.References.Static_margin import SM
from ADR.Components.Points.CG import CG


class FlightStability:
    def __init__(self, plane_type, plane):
        self.plane_type = plane_type
        self.plane = plane
        self.wing1 = self.plane.wing1
        self.wing2 = self.plane.wing2  # wing2 equals wing 1 for now (monoplane)
        self.hs = self.plane.hs
        #self.cg = None      # CG({"x": -0.0725, "y": -0.01})

        self.CM_alpha_CG_plane_obj = None
        self.CM_alpha_CG_plane_root = None

    def vary_CG(self, cg_x_range, cg_y_range):
        CM_plane_changing_CG = {}
        SM_plane_changing_CG = {}
        name = 1
        for cg_x in cg_x_range:
            for cg_y in cg_y_range:
                cg = CG({"x": cg_x, "y": cg_y})
                cg.tag = "cg" + str(name)
                CM_plane_changing_CG[cg.tag] = self.CM_plane_CG(cg)
                SM_plane_changing_CG[cg.tag] = self.static_margin()
                name += 1
        return CM_plane_changing_CG, SM_plane_changing_CG

    def CM_plane_CG(self, cg):
        self.surfaces_stall_min = min(self.wing1.stall_min, self.wing2.stall_min, key=abs)
        self.surfaces_stall_max = min(self.wing1.stall_max, self.wing2.stall_max, key=abs)

        incidence_min = min(self.wing1.incidence, self.wing2.incidence)
        incidence_max = max(self.wing1.incidence, self.wing2.incidence)

        self.plane_stall_min = self.surfaces_stall_min - incidence_min
        self.plane_stall_max = self.surfaces_stall_max - incidence_max

        self.alpha_plane_range = range(self.plane_stall_min, self.plane_stall_max + 1)

        CM_alpha_CG_tail = {}
        CM_alpha_CG_wing1 = {}
        CM_alpha_CG_wing2 = {}
        CM_alpha_CG_wings = {}
        CM_alpha_CG_plane = {}
        CM_alpha_CG_plane_each_hs_incidence = {}

        for alpha_plane in self.alpha_plane_range:

            self.wing1.attack_angle = self.wing2.attack_angle = float(alpha_plane)

            # Getting CM_alpha of wing1
            CM_alpha_CG_wing1[alpha_plane] = self.wing1.moment_on_CG(self.wing1, cg, alpha_plane)

            CM_alpha_CG_wings[alpha_plane] = CM_alpha_CG_wing1[alpha_plane]

            if self.plane_type == "biplane":
                CM_alpha_CG_wing2[alpha_plane] = self.wing2.moment_on_CG(self.wing1, cg, alpha_plane)
                CM_alpha_CG_wings[alpha_plane] += CM_alpha_CG_wing2[alpha_plane]

        for hs_incidence in self.hs.get_alpha_range():
            self.hs.incidence = hs_incidence
            for alpha_plane in self.alpha_plane_range:
                self.hs.attack_angle = -float(alpha_plane) + self.hs.incidence

                if self.hs.attack_angle in range(-20, 21):
                    # Getting CM_alpha of tail
                    CM_alpha_CG_tail[alpha_plane] = self.hs.moment_on_CG(self.wing1, cg, alpha_plane)

                    # Summing CM of tail with CM of wing per each alpha
                    # Getting CM_alpha of plane
                    CM_alpha_CG_plane[alpha_plane] = CM_alpha_CG_wings[alpha_plane] + CM_alpha_CG_tail[alpha_plane]
                else:
                    break


            CM_alpha_CG_plane_df = self.dict_to_data_frame(CM_alpha_CG_plane)
            CM_alpha_CG_plane_each_hs_incidence[hs_incidence] = CM_alpha_CG_plane_df

        dCM_dalpha_plane_df = CM_alpha_CG_plane_df.diff()
        dCM_dalpha_plane_df.fillna(method="bfill", inplace=True)
        self.plane.dCM_dalpha = dCM_dalpha_plane_df

        self.wing1.CM_alpha_CG = self.dict_to_data_frame(CM_alpha_CG_wing1)
        self.wing2.CM_alpha_CG = self.dict_to_data_frame(CM_alpha_CG_wing2)
        self.hs.CM_alpha_CG = self.dict_to_data_frame(CM_alpha_CG_tail)

        return CM_alpha_CG_plane_each_hs_incidence

    def static_margin(self):
        SM_alpha = {}
        self.hs.incidence = 0
        for alpha_plane in self.alpha_plane_range:
            self.wing1.attack_angle = self.wing2.attack_angle = float(alpha_plane)
            self.hs.attack_angle = -float(alpha_plane)

            # Calculating Static Margin for each alpha
            self.sm = SM(self.plane_type,
                         self.wing1, self.wing2, self.hs,
                         alpha_plane,
                         self.plane.dCM_dalpha.at[alpha_plane, 'CM'])
            SM_alpha[alpha_plane] = self.sm.SM

        self.SM_alpha_df = self.dict_to_data_frame(SM_alpha)
        return self.SM_alpha_df

    def dict_to_data_frame(self, dict):
        dataframe = pd.DataFrame.from_dict(dict, orient="index", columns=["CM"])
        dataframe.index.name = 'alpha'
        return dataframe