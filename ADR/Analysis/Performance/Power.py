from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

class Power:
    def __init__(self, plane):

        self.plane = plane
        self.wing1 = plane.wing1
        self.wing2 = plane.wing2
        self.hs = plane.hs
        self.area_ref = plane.wing1.area
        self.rho = 1.225
        self.thrust_required()
        self.mass = 10
        self.weight = 10 * 9.81

    def thrust_required(self):
        thrust_dict = {}
        power_dict = {}
        alpha_dict = {}
        for velocity in np.arange(1,26,0.1):
            total_lift = 0
            alpha = 0
            while(total_lift < 98 and alpha < 31):
                alpha += 1
                total_lift = self.wing1.lift(self.rho, velocity, alpha) + \
                             self.wing2.lift(self.rho, velocity, alpha) - \
                             self.hs.lift(self.rho, velocity, alpha)
            if alpha == 30: 
                alpha_nivel = 0
            else:
                alpha_nivel = alpha - 0.5

            alpha_dict[velocity] = alpha_nivel

            thrust_required = (0.5 * self.rho * velocity**2 * self.area_ref * (self.plane.CD_tp + self.plane.CD_fus)) + \
                                self.wing1.drag(self.rho, velocity, alpha_nivel) + \
                                self.wing2.drag(self.rho, velocity, alpha_nivel) + \
                                self.hs.drag(self.rho, velocity, alpha_nivel)

            thrust_dict[velocity] = thrust_required

            for velocity in thrust_dict:
                power_dict[velocity] = thrust_dict[velocity] * velocity

            power_df = pd.DataFrame.from_dict(power_dict, orient = 'index', columns = ['power'])
            thrust_df = pd.DataFrame.from_dict(thrust_dict, orient = 'index', columns = ['thrust'])
            alpha_df = pd.DataFrame.from_dict(alpha_dict, orient = 'index', columns = ['alpha'])

        plt.plot(thrust_df)
        plt.show()    
        plt.plot(power_df)
        plt.show()
        plt.plot(alpha_df)
        plt.show()
        print(thrust_dict)
        return thrust_df