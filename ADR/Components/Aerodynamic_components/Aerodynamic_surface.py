from ADR.Components.Points.CA import CA
from ADR.Components.Aerodynamic_components.Aerodynamic_section import Aerodynamic_section
from ADR.Components.Aerodynamic_components.Airfoil import Airfoil
from ADR.Components.Component import Component
from ADR.Methods.VLM.pyVLM.pyvlm.vlm import PyVLM
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


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

        self.attack_angle = 0

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

        self.airfoil1 = Airfoil({"airfoil": self.airfoil1})
        self.airfoil2 = Airfoil({"airfoil": self.airfoil2})

        self.calc_aerodynamic_data()

        self.CA = CA(data.get("X_CA"), data.get("H_CA"))

    def calc_aerodynamic_data(self):
        # This entire method is bullshit\

        #self.CA = CA(0.25*(self.chord1+self.chord2+self.chord3)/3, 0)

        Aerodynamic_calculator = PyVLM()

        self.stall_min = -15
        self.stall_max = 15
        # GEOMETRY DEFINITION #
        # Section 2
        c1 = self.section2.chord1
        c2 = self.section2.chord2
        b1 = self.section1.span
        b2 = self.section2.span
        n = 4  # number of panels (chordwise)
        m = 5   # number of panels (spanwise) (For each wing)

        # Left wing
        A = np.array([0, -b1-b2])
        B = np.array([0, -b1])
        leading_edges_coord_lw = [A, B]
        chord_lengths_lw = [c2, c1]
        Aerodynamic_calculator.add_geometry(leading_edges_coord_lw, chord_lengths_lw, n, m, 0)

        # Section 1
        c1 = self.section1.chord1
        c2 = self.section1.chord2
        b1 = self.section1.span
        n = 4  # number of panels (chordwise)
        m = 5   # number of panels (spanwise) (For each wing)

        # Left wing
        A = np.array([0, -b1])
        B = np.array([0, 0])
        leading_edges_coord_lw = [A, B]
        chord_lengths_lw = [c2, c1]
        Aerodynamic_calculator.add_geometry(leading_edges_coord_lw, chord_lengths_lw, n, m, 0)

        # Right wing
        C = np.array([0, 0])
        D = np.array([0, b1])
        leading_edges_coord_rw = [C, D]
        chord_lengths_rw = [c1, c2]
        Aerodynamic_calculator.add_geometry(leading_edges_coord_rw, chord_lengths_rw, n, m, 0)

        # Section 2
        c1 = self.section2.chord1
        c2 = self.section2.chord2
        b2 = self.section2.span
        n = 4  # number of panels (chordwise)
        m = 5   # number of panels (spanwise) (For each wing)

        # Right wing
        C = np.array([0, b1])
        D = np.array([0, b1+b2])
        leading_edges_coord_rw = [C, D]
        chord_lengths_rw = [c1, c2]
        Aerodynamic_calculator.add_geometry(leading_edges_coord_rw, chord_lengths_rw, n, m, 0)
        
        Aerodynamic_calculator.check_mesh()
 
        S = self.section1.area+self.section2.area
        self.stall_min = 0
        self.stall_max = 20

        self.downwash_angle = 0
 
        # SIMULATION
        # Flight condition parameters
        V = 12
        rho = 1.225 #Value applied internally in the code
        alpha_length = self.stall_max-self.stall_min+1
        alpha2 = np.linspace(self.stall_min, self.stall_max, alpha_length)
        alpha_rad = alpha2*np.pi/180
        alpha = []
        cl = []
        cd = []
        cm = []
        cm2 = []
        Xcp = []
        clc_max = 1.5
        q = rho*(V**2)/2
        for i in range(alpha_length):
            L, D, M, y, clc = Aerodynamic_calculator.vlm(V, alpha_rad[i])
            cp = -M/(L*self.chord1)
            if max(clc) > clc_max:
                break
            print(alpha_rad[i], L)
            alpha.append(alpha2[i])
            cd.append(D/(q*S))
            cl.append(L/(q*S))
            cm.append(-(cp-0.25)*L/(q*S))

        plt.plot(alpha, cl)
        plt.plot(alpha, cd)
        plt.plot(alpha, cm)
        plt.show()

        self.CL_alpha = pd.DataFrame({'Cl': cl, 'alpha': alpha})
        self.CD_alpha = pd.DataFrame({'Cd': cd, 'alpha': alpha})
        self.CM_alpha = pd.DataFrame({'Cm': cm, 'alpha': alpha})

        self.dCL_dalpha = self.diff(self.CL_alpha)
        self.dCD_dalpha = self.diff(self.CD_alpha)

        self.downwash_angle = 0

    def attack_angle_index(self):
        return self.attack_angle + abs(self.stall_min)

    def diff(self, array):
        x = list(np.diff(array))
        x.append(x[-1])     # doubles last term
        return x

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
