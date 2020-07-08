from ADR.Components.Aerodynamic_components.Wing import Wing
from ADR.Components.Aerodynamic_components.HS import HS
from ADR.Components.Propulsion.Motor import Motor
from ADR.Components.Points.CG import CG
from ADR.Components.Points.TPR import TPR
from ADR.Core.data_manipulation import dict_to_dataframe

import numpy as np


class Plane:
    def __init__(self, data):
        self.data = data
        self.plane_type = data.get("plane_type")

        wing1_data = {
            "x": data.get("wing1_x"),
            "y": data.get("wing1_y"),
            "z": data.get("wing1_z"),
            "airfoil_clmax": data.get("wing1_clmax_airfoil"),
            "airfoil1_name": data.get("wing1_airfoil1_name"),
            "airfoil2_name": data.get("wing1_airfoil2_name"),
            "airfoil3_name": data.get("wing1_airfoil3_name"),
            "span1": data.get("wing1_span1"),
            "span2": data.get("wing1_span2"),
            "chord1": data.get("wing1_chord1"),
            "chord2": data.get("wing1_chord2"),
            "chord3": data.get("wing1_chord3"),
            "twist1": data.get("wing1_twist1"),
            "twist2": data.get("wing1_twist2"),
            "twist3": data.get("wing1_twist3"),
            "incidence": data.get("wing1_incidence"),
            "CM_ca": data.get("wing1_CM_ca"),
        }

        wing2_data = {
            "x": data.get("wing2_x"),
            "y": data.get("wing2_y"),
            "z": data.get("wing2_z"),
            "airfoil_clmax": data.get("wing2_clmax_airfoil"),
            "airfoil1_name": data.get("wing2_airfoil1_name"),
            "airfoil2_name": data.get("wing2_airfoil2_name"),
            "airfoil3_name": data.get("wing2_airfoil3_name"),
            "span1": data.get("wing2_span1"),
            "span2": data.get("wing2_span2"),
            "chord1": data.get("wing2_chord1"),
            "chord2": data.get("wing2_chord2"),
            "chord3": data.get("wing2_chord3"),
            "twist1": data.get("wing2_twist1"),
            "twist2": data.get("wing2_twist2"),
            "twist3": data.get("wing2_twist3"),
            "incidence": data.get("wing2_incidence"),
            "CM_ca": data.get("wing2_CM_ca"),
        }

        hs_data = {
            "x": data.get("hs_x"),
            "y": data.get("hs_y"),
            "z": data.get("hs_z"),
            "airfoil_clmax": data.get("hs_clmax_airfoil"),
            "airfoil1_name": data.get("hs_airfoil1_name"),
            "airfoil2_name": data.get("hs_airfoil2_name"),
            "airfoil3_name": data.get("hs_airfoil3_name"),
            "span1": data.get("hs_span1"),
            "span2": data.get("hs_span2"),
            "chord1": data.get("hs_chord1"),
            "chord2": data.get("hs_chord2"),
            "chord3": data.get("hs_chord3"),
            "twist1": data.get("hs_twist1"),
            "twist2": data.get("hs_twist2"),
            "twist3": data.get("hs_twist3"),
            "incidence": data.get("hs_incidence"),
            "CM_ca": data.get("hs_CM_ca"),
        }

        motor_data = {
            "x": data.get("motor_x"),
            "y": data.get("motor_y"),
            "z": data.get("motor_z"),
            "static_thrust": data.get("static_thrust"),
            "linear_decay_coefficient": data.get("linear_decay_coefficient"),
        }

        cg_data = {"x": data.get("cg_x"), "z": data.get("cg_z")}

        tpr_data = {"x": data.get("tpr_x"), "z": data.get("tpr_z")}

        self.Iyy_TPR = data.get("Iyy_TPR")
        self.CD_tp = data.get("CD_tp")
        self.S_tp = data.get("S_tp")
        self.CD_fus = data.get("CD_fus")
        self.S_fus = data.get("S_fus")
        self.u_k = data.get("u_k")

        self.wing1 = Wing(wing1_data)
        self.wing2 = Wing(wing2_data)
        self.hs = HS(hs_data)
        # self.vs = VS(vs_data)
        self.motor = Motor(motor_data)
        self.cg = CG(cg_data)
        self.tpr = TPR(tpr_data)

        self.V_stall = 0
        self.V_min = 0
        self.V_max = 0
        self.V_takeoff = 0
        self.mtow = 5
        self.alpha_min = 0
        self.alpha_max = 0
        self.alpha_trimm_min = 0
        self.alpha_trimm_max = 0
        self.tail_trimm = 0

        self.SM_alpha = None

        self.trimm_for_low_angles = False
        self.trimm_for_high_angles = False
        self.positive_sm_for_positive_alphas = False
        self.dimensions_are_good = False

        self.total_dimensions = 0
        self.dead_weight = 0
        self.payload = 0
        self.score = None

        self.dead = False

        self.get_CL_alpha_plane()
        self.get_CD_alpha_plane()
        self.set_alpha_range()
        self.hs.set_incidence_range(self.stall_min, self.stall_max)

    def __str__(self):
        return self.__class__.__name__

    def set_alpha_range(self):
        wings_stall_min = max(self.wing1.stall_min, self.wing2.stall_min)
        wings_stall_max = min(self.wing1.stall_max, self.wing2.stall_max)

        # incidence_min = min(self.wing1.incidence, self.wing2.incidence)
        # incidence_max = max(self.wing1.incidence, self.wing2.incidence)
        # TODO: Incidence for now is fixed on 0 and should be better implemented

        self.stall_min = wings_stall_min
        self.stall_max = wings_stall_max

        self.alpha_range = np.arange(self.stall_min, self.stall_max + 1)

    def set_alpha_trimmed(self, alpha_airplane):
        self.wing1.update_alpha(alpha_airplane)
        if self.plane_type == "biplane":
            self.wing2.update_alpha(alpha_airplane)
        hs_incidence = np.interp(
            alpha_airplane,
            self.tail_trimm.index.values,
            self.tail_trimm["hs_incidence"],
        )
        self.hs.incidence = hs_incidence
        self.hs.update_alpha(alpha_airplane)

    def get_CL_alpha_plane(self):
        CL_alpha_plane = {}
        for alpha in np.arange(-10, 21, 1.0):
            numerator = (
                self.wing1.get_CL(alpha) * self.wing1.area
                - self.hs.get_CL(alpha) * self.hs.area
            )
            if self.plane_type == "biplane":
                numerator += self.wing2.get_CL(alpha) * self.wing2.area
            CL_alpha_plane[alpha] = numerator / self.wing1.area
        self.CL_alpha = dict_to_dataframe(CL_alpha_plane, "CL", "alpha")
        return self.CL_alpha

    def get_CD_alpha_plane(self):
        CD_alpha_plane = {}
        for alpha in np.arange(-10, 21, 1.0):
            numerator = (
                self.wing1.get_CD(alpha) * self.wing1.area
                - self.hs.get_CD(alpha) * self.hs.area
            )
            if self.plane_type == "biplane":
                numerator += self.wing2.get_CD(alpha) * self.wing2.area
            CD_alpha_plane[alpha] = numerator / self.wing1.area
        self.CD_alpha = dict_to_dataframe(CD_alpha_plane, "CD", "alpha")
        return self.CD_alpha

    def get_V_stall(self, rho):
        self.CL_max = self.CL_alpha.max()[0]
        self.V_stall = (
            (2 * self.mtow * 9.81) / (rho * self.wing1.area * self.CL_max)
        ) ** 0.5
        return self.V_stall

    def get_V_CLmin(self, rho):
        self.CL_min = self.CL_alpha.min()[0]
        self.V_CLmin = (
            (2 * self.mtow * 9.81) / (rho * self.wing1.area * self.CL_min)
        ) ** 0.5
        return self.V_CLmin

    def show_plane(self):
        pass
        # print('-------------------------------------------------------------')

        # print("\nPlane components:\n")

        # print("\t--- ", self.wing1, " ---")
        # "x": data.get("wing1_x"),
        # "y": data.get("wing1_y"),
        # "z": data.get("wing1_z"),
        # "airfoil_clmax": data.get("wing1_clmax_airfoil"),
        # "airfoil1_name": data.get("wing1_airfoil1_name"),
        # "airfoil2_name": data.get("wing1_airfoil2_name"),
        # "airfoil3_name": data.get("wing1_airfoil3_name"),
        # "span1": data.get("wing1_span1"),
        # "span2": data.get("wing1_span2"),
        # "chord1": data.get("wing1_chord1"),
        # "chord2": data.get("wing1_chord2"),
        # "chord3": data.get("wing1_chord3"),
        # "twist1": data.get("wing1_twist1"),
        # "twist2": data.get("wing1_twist2"),
        # "twist3": data.get("wing1_twist3"),
        # "incidence": data.get("wing1_incidence"),
        # "CM_ca": data.get("wing1_CM_ca"),
        # print()

        # print("\t--- ", self.wing2, " ---")
        # "x": data.get("wing2_x"),
        # "y": data.get("wing2_y"),
        # "z": data.get("wing2_z"),
        # "airfoil_clmax": data.get("wing2_clmax_airfoil"),
        # "airfoil1_name": data.get("wing2_airfoil1_name"),
        # "airfoil2_name": data.get("wing2_airfoil2_name"),
        # "airfoil3_name": data.get("wing2_airfoil3_name"),
        # "span1": data.get("wing2_span1"),
        # "span2": data.get("wing2_span2"),
        # "chord1": data.get("wing2_chord1"),
        # "chord2": data.get("wing2_chord2"),
        # "chord3": data.get("wing2_chord3"),
        # "twist1": data.get("wing2_twist1"),
        # "twist2": data.get("wing2_twist2"),
        # "twist3": data.get("wing2_twist3"),
        # "incidence": data.get("wing2_incidence"),
        # "CM_ca": data.get("wing2_CM_ca"),
        # print()

        # print("\t--- ", self.hs, " ---")
        # "x": data.get("hs_x"),
        # "y": data.get("hs_y"),
        # "z": data.get("hs_z"),
        # "airfoil_clmax": data.get("hs_clmax_airfoil"),
        # "airfoil1_name": data.get("hs_airfoil1_name"),
        # "airfoil2_name": data.get("hs_airfoil2_name"),
        # "airfoil3_name": data.get("hs_airfoil3_name"),
        # "span1": data.get("hs_span1"),
        # "span2": data.get("hs_span2"),
        # "chord1": data.get("hs_chord1"),
        # "chord2": data.get("hs_chord2"),
        # "chord3": data.get("hs_chord3"),
        # "twist1": data.get("hs_twist1"),
        # "twist2": data.get("hs_twist2"),
        # "twist3": data.get("hs_twist3"),
        # "incidence": data.get("hs_incidence"),
        # "CM_ca": data.get("hs_CM_ca"),
        # print()

        # "x": data.get("motor_x"),
        # "y": data.get("motor_y"),
        # "z": data.get("motor_z"),
        # "static_thrust": data.get("static_thrust"),
        # "linear_decay_coefficient": data.get("linear_decay_coefficient")
        # print()

        # "x": data.get("cg_x"),
        # "z": data.get("cg_z")
        # print()

        # "x": data.get("tpr_x"),
        # "z": data.get("tpr_z")
        # print()
        # print('-------------------------------------------------------------')
