from ADR.Components.Points.CA import CA
from ADR.Components.Aerodynamic_components.Aerodynamic_section import Aerodynamic_section
from ADR.Components.Aerodynamic_components.Airfoil import Airfoil
from ADR.Components.Component import Component
import numpy as np

class Aerodynamic_surface(Component):
    def __init__(self, data):
        super().__init__(data)

        self.airfoil1 = data.get("airfoil1")
        self.airfoil2 = data.get("airfoil2")
        self.span1 = data.get("span1")
        self.span2 = data.get("span2")
        self.chord1 = data.get("chord1")
        self.chord2 = data.get("chord2")
        self.chord3 = data.get("chord3")
        self.twist1 = data.get("twist1")
        self.twist2 = data.get("twist2")
        self.twist3 = data.get("twist3")
        self.incidence = data.get("incidence")

        data_section1 = {
            "airfoil": self.airfoil1,
            "span": self.span1,
            "chord1": self.chord1,
            "chord2": self.chord2,
            "twist1": self.twist1,
            "twist2": self.twist2
            }
        data_section2 = {
            "airfoil": self.airfoil2,
            "span": self.span2,
            "chord1": self.chord2,
            "chord2": self.chord3,
            "twist1": self.twist2,
            "twist2": self.twist3
            }

        self.section1 = Aerodynamic_section(data_section1)
        self.section2 = Aerodynamic_section(data_section2)

        self.airfoil1 = Airfoil({"airfoil" : self.airfoil1})
        self.airfoil2 = Airfoil({"airfoil" : self.airfoil2})

        self.calc_aerodynamic_data()
        self.calc_area()

    def calc_aerodynamic_data(self):
        # This entire method is bullshit

        self.CA = CA(0.75*(self.chord1+self.chord2+self.chord3)/3, 0)

        self.CL_alpha = self.airfoil1.Cl_alpha
        self.CD_alpha = self.airfoil1.Cd_alpha
        self.CM_alpha = self.airfoil1.Cm_alpha

        self.stall_min = 0
        self.stall_max = 15

        self.downwash_angle = 6

    def get_CL(self, alpha):
        CL = np.interp(alpha, self.CL_alpha.index.values, self.CL_alpha['Cl'])
        return CL

    def get_CD(self, alpha):
        CD = np.interp(alpha, self.CD_alpha.index.values, self.CD_alpha['Cd'])
        return CD

    def get_CM(self, alpha):
        CM = np.interp(alpha, self.CM_alpha.index.values, self.CM_alpha['Cm'])
        return CM

    def lift(self, air_density, velocity, alpha):
        lift = 0.5*air_density*velocity**2*self.area*self.get_CL(alpha)
        return lift

    def drag(self, air_density, velocity, alpha):
        drag = 0.5*air_density*velocity**2*self.area*self.get_CD(alpha)
        return drag

    def moment(self, air_density, velocity, alpha):
        moment = 0.5*air_density*velocity**2*self.area*self.get_CM(alpha)
        return moment
