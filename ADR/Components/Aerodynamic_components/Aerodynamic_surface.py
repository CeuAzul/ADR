from ADR.Components.Points.CA import CA
from ADR.Components.Aerodynamic_components.Aerodynamic_section import Aerodynamic_section
from ADR.Components.Aerodynamic_components.Airfoil import Airfoil
from ADR.Components.Component import Component
from ADR.Methods.VLM.AVL.avl_runner import get_aero_coeffs
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from math import radians, cos, sin


class Aerodynamic_surface(Component):
    def __init__(self, data):
        super().__init__(data)

        self.data = data

        self.airfoil1_name = data.get("airfoil1_name")
        self.airfoil2_name = data.get("airfoil2_name")
        self.airfoil3_name = data.get("airfoil3_name")
        self.span1 = data.get("span1")
        self.span2 = data.get("span2")
        self.chord1 = data.get("chord1")
        self.chord2 = data.get("chord2")
        self.chord3 = data.get("chord3")
        self.twist1 = data.get("twist1")
        self.twist2 = data.get("twist2")
        self.twist3 = data.get("twist3")
        self.incidence = data.get("incidence")

        self.attack_angle = None
        self.CM_alpha_CG = None

        data_section1 = {
            "airfoil1_name": self.airfoil1_name,
            "airfoil2_name": self.airfoil2_name,
            "span": self.span1,
            "chord1": self.chord1,
            "chord2": self.chord2,
            "twist1": self.twist1,
            "twist2": self.twist2
        }

        data_section2 = {
            "airfoil1_name": self.airfoil2_name,
            "airfoil2_name": self.airfoil3_name,
            "span": self.span2,
            "chord1": self.chord2,
            "chord2": self.chord3,
            "twist1": self.twist2,
            "twist2": self.twist3
        }

        self.section1 = Aerodynamic_section(data_section1)
        self.section2 = Aerodynamic_section(data_section2)

        self.area = 2 * (self.section1.area + self.section2.area)
        self.MAC = self.calc_MAC()

        self.calc_aerodynamic_data()

        self.ca = CA({
            "x": - self.MAC / 4,
            "z": 0,
            "surface_x": self.x,
            "surface_z": self.z,
            })
        self.CM_ca = data.get("CM_ca")

        self.downwash_angle = 0

    def __str__(self):
        return self.__class__.__name__

    def calc_aerodynamic_data(self):
        # This entire method is NOT bullshit\

        self.CL_alpha, self.CD_alpha, self.CM_alpha = get_aero_coeffs(self.data)

        self.stall_min = -10 #TODO: Implement crictical section method
        self.stall_max = -15

        self.dCL_dalpha = self.CL_alpha.diff()
        self.dCD_dalpha = self.CD_alpha.diff()
        self.dCL_dalpha.fillna(method="bfill", inplace=True)
        self.dCD_dalpha.fillna(method="bfill", inplace=True)

        self.downwash_angle = 0

    def moment_on_CG(self, reference_surface, cg, alpha_plane):

        resultant = 0

        surface_CL = self.CL_alpha.at[self.attack_angle, 'CL']
        surface_CD = self.CD_alpha.at[self.attack_angle, 'CD']

        sin_component = sin(radians(alpha_plane + self.incidence))
        cos_component = cos(radians(alpha_plane + self.incidence))

        horizontal_distance = self.x + self.ca.x - cg.x
        vertical_distance = self.z + self.ca.z - cg.z

        item1 = surface_CL * cos_component * horizontal_distance / reference_surface.MAC
        item2 = surface_CL * sin_component * vertical_distance / reference_surface.MAC
        item3 = surface_CD * sin_component * horizontal_distance / reference_surface.MAC
        item4 = surface_CD * cos_component * vertical_distance / reference_surface.MAC
        if self.__str__() == "Wing":
            resultant = + item1 - item2 + item3 + item4
        elif self.__str__() == "HS":
            resultant = - item1 + item2 + item3 + item4

        CM = (self.CM_ca * self.MAC / reference_surface.MAC + resultant) * self.area / reference_surface.area
        return CM

    def get_alpha_range(self):
        return range(self.stall_min, self.stall_max + 1)

    def calc_MAC(self):
        MAC = self.section1.MAC * (self.section1.area/(self.section1.area + self.section2.area)) \
            + self.section2.MAC * (self.section2.area/(self.section1.area + self.section2.area))
        return MAC

    def get_CL(self, alpha):
        CL = np.interp(alpha, self.CL_alpha.index.values, self.CL_alpha['CL'])
        return CL

    def get_CD(self, alpha):
        CD = np.interp(alpha, self.CD_alpha.index.values, self.CD_alpha['CD'])
        return CD

    def get_CM(self, alpha):
        CM = np.interp(alpha, self.CM_alpha.index.values, self.CM_alpha['CM'])
        return CM

    def lift(self, air_density, velocity, alpha):
        lift = 0.5 * air_density * velocity ** 2 * self.area * self.get_CL(alpha)
        return lift

    def drag(self, air_density, velocity, alpha):
        drag = 0.5 * air_density * velocity ** 2 * self.area * self.get_CD(alpha)
        return drag

    def moment(self, air_density, velocity, alpha):
        moment = 0.5 * air_density * velocity ** 2 * self.area * self.get_CM(alpha)
        return moment
