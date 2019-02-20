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
        self.mass = 9.3
        self.weight = self.mass * 9.81
        self.power_required()
        self.power_available()

    def power_required(self):
        thrust_required_dict = {}
        power_required_dict = {}
        alpha_dict = {}
        for velocity in np.arange(0,26,0.1):
            total_lift = 0
            alpha = -20
            while(total_lift < self.weight):
                alpha += 0.1
                total_lift = self.wing1.lift(self.rho, velocity, alpha) + \
                             self.wing2.lift(self.rho, velocity, alpha) - \
                             self.hs.lift(self.rho, velocity, alpha)
                if alpha >= 20:
                    alpha_nivel = None
                    break
                else:
                    alpha_nivel = alpha

            thrust_required = (0.5 * self.rho * velocity**2 * self.area_ref * (self.plane.CD_tp + self.plane.CD_fus)) + \
                              self.wing1.drag(self.rho, velocity, alpha_nivel) + \
                              self.wing2.drag(self.rho, velocity, alpha_nivel) + \
                              self.hs.drag(self.rho, velocity, alpha_nivel)

            alpha_dict[velocity] = alpha_nivel
            thrust_required_dict[velocity] = thrust_required

        for velocity in thrust_required_dict:
            power_required_dict[velocity] = thrust_required_dict[velocity] * velocity


        self.thrust_required_dict = thrust_required_dict
        self.power_required_dict = power_required_dict
        self.alpha_dict = alpha_dict
        self.alpha_df = pd.DataFrame.from_dict(alpha_dict, orient = 'index', columns = ['alpha'])
        self.thrust_required_df = pd.DataFrame.from_dict(thrust_required_dict, orient = 'index', columns = ['thrust'])
        self.power_required_df = pd.DataFrame.from_dict(power_required_dict, orient = 'index', columns = ['power'])

        return self.alpha_df, self.thrust_required_df, self.power_required_df

    def power_available(self):
        thrust_available_dict = {}
        power_available_dict = {}

        for velocity in np.arange(0,26,0.1):
            thrust_available = self.plane.motor.thrust(velocity)
            thrust_available_dict[velocity] = thrust_available

        for velocity in thrust_available_dict:
            power_available_dict[velocity] = thrust_available_dict[velocity] * velocity


        self.thrust_available_dict = thrust_available_dict
        self.power_available_dict = power_available_dict
        self.thrust_available_df = pd.DataFrame.from_dict(thrust_available_dict, orient = 'index', columns = ['thrust'])
        self.power_available_df = pd.DataFrame.from_dict(power_available_dict, orient = 'index', columns = ['power'])

        return self.thrust_available_df, self.power_available_df