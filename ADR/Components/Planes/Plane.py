from ADR.Components.Planes.Aerodynamic_surfaces.Wing import Wing
from ADR.Components.Planes.Aerodynamic_surfaces.EH import EH
from ADR.Components.Planes.Aerodynamic_surfaces.EV import EV

class Plane():
    def __init__(self, data):
        # Ideia de como criar o aviao
        wing_data = {"span": data.get("span_Wing"), "CL_alpha": data.get("CL_alpha_asa")}
        eh_data = {"span": data.get("span_EH")}
        ev_data = {"chord": data.get("chord_EV")}
        self.wing = Wing(wing_data)
        self.eh = EH(eh_data)
        self.ev = EV(ev_data)


