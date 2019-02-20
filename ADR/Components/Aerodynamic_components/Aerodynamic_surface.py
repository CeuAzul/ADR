from ADR.Components.Points.CA import CA
from ADR.Components.Aerodynamic_components.Aerodynamic_section import Aerodynamic_section
from ADR.Components.Aerodynamic_components.Airfoil import Airfoil
from ADR.Components.Component import Component
from ADR.Methods.VLM.AVL.avl_runner import get_aero_coeffs
from ADR.Methods.VLM.pyVLM.pyvlm.vlm import PyVLM
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

        self.vlm = 'pyVLM'
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

        if self.vlm == 'AVL':
            self.CL_alpha, self.CD_alpha, self.CM_alpha = get_aero_coeffs(self.data)

            self.stall_min = -10 #TODO: Implement crictical section method
            self.stall_max = +15

        elif self.vlm == 'pyVLM':
            Aerodynamic_calculator = PyVLM()

            self.stall_min = -10
            self.stall_max = +15

            self.downwash_angle = 0

            # GEOMETRY DEFINITION #
            # Section 2
            c1 = self.section2.chord1
            c2 = self.section2.chord2
            b1 = self.section1.span
            b2 = self.section2.span
            camber = self.section2.airfoil1.Camber_line
            n = 2  # number of panels (chordwise)
            m = 2  # number of panels (spanwise) (For each wing)

            # Left wing
            A = np.array([0, -b1 - b2])
            B = np.array([0, -b1])
            leading_edges_coord_lw = [A, B]
            chord_lengths_lw = [c2, c1]
            Aerodynamic_calculator.add_geometry(leading_edges_coord_lw, chord_lengths_lw, n, m, 1, camber)

            # Section 1
            c1 = self.section1.chord1
            c2 = self.section1.chord2
            b1 = self.section1.span
            camber = self.section1.airfoil1.Camber_line

            # Left wing
            A = np.array([0, -b1])
            B = np.array([0, 0])
            leading_edges_coord_lw = [A, B]
            chord_lengths_lw = [c2, c1]
            Aerodynamic_calculator.add_geometry(leading_edges_coord_lw, chord_lengths_lw, n, m, 1, camber)

            # Right wing
            C = np.array([0, 0])
            D = np.array([0, b1])
            leading_edges_coord_rw = [C, D]
            chord_lengths_rw = [c1, c2]
            Aerodynamic_calculator.add_geometry(leading_edges_coord_rw, chord_lengths_rw, n, m, 1, camber)

            # Section 2
            c1 = self.section2.chord1
            c2 = self.section2.chord2
            b2 = self.section2.span
            camber = self.section2.airfoil1.Camber_line

            # Right wing
            C = np.array([0, b1])
            D = np.array([0, b1 + b2])
            leading_edges_coord_rw = [C, D]
            chord_lengths_rw = [c1, c2]
            Aerodynamic_calculator.add_geometry(leading_edges_coord_rw, chord_lengths_rw, n, m, 1, camber)

            # Aerodynamic_calculator.check_mesh()

            # SIMULATION
            # Flight condition parameters
            V = 12
            rho = 1.225  # Value applied internally in the code
            alpha_length = self.stall_max - self.stall_min + 1
            alpha2 = np.linspace(self.stall_min, self.stall_max, alpha_length)
            alpha_rad = alpha2 * np.pi / 180
            alpha = []
            cl = []
            cd = []
            cm = []
            cm2 = []
            Xcp = []
            clc_max = 2.2 #TODO: pegar do perfil
            q = rho*(V**2)/2
            for i in range(alpha_length):
                L, D, M, y, clc = Aerodynamic_calculator.vlm(V, alpha_rad[i], self.airfoil1_name) #TODO: COLOCAR AIRFOIL CERTO
                cp = -M/(L*self.MAC) #TODO: Corda 1 apenas?
                if max(clc) > clc_max:
                    break
                alpha.append(alpha2[i])
                cd.append(D/(q*self.area))
                cl.append(L/(q*self.area))
                cm.append(-(cp-0.25)*L/(q*self.area)) #TODO: Multiplica por 0?

            self.CL_alpha = pd.DataFrame({'CL': cl, 'alpha': alpha})
            self.CL_alpha.set_index('alpha', inplace=True)

            CL_alpha0 = self.CL_alpha.at[0.0, 'CL']
            CL_alpha_ang_coeff = self.CL_alpha.at[1.0, 'CL']-self.CL_alpha.at[0.0, 'CL']
            alpha_CL0 = -CL_alpha0/CL_alpha_ang_coeff

            alpha_transpose = -11.5-alpha_CL0

            correct_alpha_CL0 = -11.5
            correct_CL_alpha0 = -correct_alpha_CL0*CL_alpha_ang_coeff

            transposed_CL = {}
            for i, row in self.CL_alpha.iterrows():
                transposed_CL[i] = correct_CL_alpha0 + CL_alpha_ang_coeff*i


            self.CL_alpha_transposed = pd.DataFrame.from_dict(transposed_CL, orient='index', columns=['CL'])
            self.CL_alpha_transposed.index.name = 'alpha'

            self.CL_alpha = self.CL_alpha_transposed

            self.CD_alpha = pd.DataFrame({'CD': cd, 'alpha': alpha})
            self.CD_alpha.set_index('alpha', inplace=True)

            self.CM_alpha = pd.DataFrame({'CM': cm, 'alpha': alpha})
            self.CM_alpha.set_index('alpha', inplace=True)

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
