from ADR.Components.Aerodynamic_components.Wing import Wing
from ADR.Components.Aerodynamic_components.HS import HS
from ADR.Components.Aerodynamic_components.VS import VS
from ADR.Components.Propulsion.Motor import Motor
from ADR.Components.Points.CG import CG
from ADR.Components.Points.TPR import TPR


class Plane:
    def __init__(self, data):
        wing1_data = {
            "x": data.get("wing1_x"),
            "y": data.get("wing1_y"),
            "z": data.get("wing1_z"),
            "airfoil1_name": data.get("wing1_airfoil1_name"),
            "airfoil2_name": data.get("wing1_airfoil2_name"),
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
            "airfoil1_name": data.get("wing2_airfoil1_name"),
            "airfoil2_name": data.get("wing2_airfoil2_name"),
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
            "airfoil1_name": data.get("hs_airfoil1_name"),
            "airfoil2_name": data.get("hs_airfoil2_name"),
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

        vs_data = {
            "x": data.get("vs_x"),
            "y": data.get("vs_y"),
            "z": data.get("vs_z"),
            "airfoil1_name": data.get("vs_airfoil1_name"),
            "airfoil2_name": data.get("vs_airfoil2_name"),
            "span1": data.get("vs_span1"),
            "span2": data.get("vs_span2"),
            "chord1": data.get("vs_chord1"),
            "chord2": data.get("vs_chord2"),
            "chord3": data.get("vs_chord3"),
            "twist1": data.get("vs_twist1"),
            "twist2": data.get("vs_twist2"),
            "twist3": data.get("vs_twist3"),
            "incidence": data.get("vs_incidence")
        }

        motor_data = {
            "static_thrust": data.get("static_thrust"),
            "linear_decay_coefficient": data.get("linear_decay_coefficient")
        }

        cg_data = {
            "x": data.get("cg_x"),
            "z": data.get("cg_z")
        }

        tpr_data = {
            "x": data.get("tpr_x"),
            "z": data.get("tpr_z")
        }

        self.wing1 = Wing(wing1_data)
        self.wing2 = Wing(wing2_data)
        self.hs = HS(hs_data)
        #self.vs = VS(vs_data)
        self.motor = Motor(motor_data)
        self.cg = CG(cg_data)
        self.tpr = CG(tpr_data)

        self.dCM_dalpha = 0

    def __str__(self):
        return self.__class__.__name__

    def show_plane(self):
        print("\nPlane components:\n")

        print("\t--- ", self.wing1, " ---")
        print("\tairfoil1 = ", self.wing1.airfoil1)
        print("\tairfoil2 = ", self.wing1.airfoil2)
        print("\tspan1 = ", self.wing1.span1)
        print("\tspan2 = ", self.wing1.span2)
        print("\tchord1 = ", self.wing1.chord1)
        print("\tchord2 = ", self.wing1.chord2)
        print("\tchord3 = ", self.wing1.chord3)
        print("\ttwist1 = ", self.wing1.twist1)
        print("\ttwist2 = ", self.wing1.twist2)
        print("\ttwist3 = ", self.wing1.twist3)
        print("\tincidence = ", self.wing1.incidence)
        print("\tca.x = ", self.wing1.ca.x)
        print("\tca.z = ", self.wing1.ca.z)
        print("\tstall_min = ", self.wing1.stall_min)
        print("\tstall_max = ", self.wing1.stall_max)
        print("\tdownwash_angle = ", self.wing1.downwash_angle)
        print()

        print("\t--- ", self.hs, " ---")
        print("\tairfoil1 = ", self.hs.airfoil1)
        print("\tairfoil2 = ", self.hs.airfoil2)
        print("\tspan1 = ", self.hs.span1)
        print("\tspan2 = ", self.hs.span2)
        print("\tchord1 = ", self.hs.chord1)
        print("\tchord2 = ", self.hs.chord2)
        print("\tchord3 = ", self.hs.chord3)
        print("\ttwist1 = ", self.hs.twist1)
        print("\ttwist2 = ", self.hs.twist2)
        print("\ttwist3 = ", self.hs.twist3)
        print("\tincidence = ", self.hs.incidence)
        print("\tca.x = ", self.hs.ca.x)
        print("\tca.z = ", self.hs.ca.z)
        print("\tstall_min = ", self.hs.stall_min)
        print("\tstall_max = ", self.hs.stall_max)
        print("\tdownwash_angle = ", self.hs.downwash_angle)
        print()

        print("\t--- ", self.cg, " ---")
        print("\tcg.x = ", self.cg.x)
        print("\tcg.z = ", self.cg.z)

        print()
