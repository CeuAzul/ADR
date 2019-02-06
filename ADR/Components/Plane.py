from ADR.Components.Aerodynamic_components.Wing import Wing
from ADR.Components.Aerodynamic_components.HS import HS
from ADR.Components.Aerodynamic_components.VS import VS
from ADR.Components.Propulsion.Motor import Motor

class Plane():
    def __init__(self, data):

        wing_data = {
            "x": data.get("wing_x"),
            "y": data.get("wing_y"),
            "z": data.get("wing_z"),
            "airfoil1": data.get("wing_airfoil1"),
            "airfoil2": data.get("wing_airfoil2"),
            "span1": data.get("wing_span1"),
            "span2": data.get("wing_span2"),
            "chord1": data.get("wing_chord1"),
            "chord2": data.get("wing_chord2"),
            "chord3": data.get("wing_chord3"),
            "twist1": data.get("wing_twist1"),
            "twist2": data.get("wing_twist2"),
            "twist3": data.get("wing_twist3"),
            "incidence": data.get("wing_incidence")
        }

        hs_data = {
            "x": data.get("hs_x"),
            "y": data.get("hs_y"),
            "z": data.get("hs_z"),
            "airfoil1": data.get("hs_airfoil1"),
            "airfoil2": data.get("hs_airfoil2"),
            "span1": data.get("hs_span1"),
            "span2": data.get("hs_span2"),
            "chord1": data.get("hs_chord1"),
            "chord2": data.get("hs_chord2"),
            "chord3": data.get("hs_chord3"),
            "twist1": data.get("hs_twist1"),
            "twist2": data.get("hs_twist2"),
            "twist3": data.get("hs_twist3"),
            "incidence": data.get("hs_incidence")
        }

        vs_data = {
            "x": data.get("vs_x"),
            "y": data.get("vs_y"),
            "z": data.get("vs_z"),
            "airfoil1": data.get("vs_airfoil1"),
            "airfoil2": data.get("vs_airfoil2"),
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

        self.wing = Wing(wing_data)
        self.hs = HS(hs_data)
        self.vs = VS(vs_data)
        self.motor = Motor(motor_data)
