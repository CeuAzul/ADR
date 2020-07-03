import numpy as np
from ADR.Core.data_manipulation import dict_to_dataframe
from ADR.Core.data_manipulation import find_df_roots

from ADR.Methods.FundamentalEquations import drag


class Power:
    def __init__(self, plane, performance_parameters):

        self.plane = plane
        self.wing1 = plane.wing1
        self.wing2 = plane.wing2
        self.hs = plane.hs
        self.area_ref = plane.wing1.area
        self.rho = performance_parameters.get("rho_air")
        self.checks_and_update_mtow()

    def checks_and_update_mtow(self):
        self.plane.get_V_stall(self.rho)
        self.plane.get_V_CLmin(self.rho)
        self.velocity_range = np.arange(
            self.plane.V_stall, self.plane.V_CLmin, 0.1)

        self.power_available()
        self.power_required()
        self.power_excess()

        positive_power = self.power_excess_df["Power excess"] > 0
        has_power_excess = positive_power.any()

        while has_power_excess == False and self.plane.mtow != 0:
            positive_power = self.power_excess_df["Power excess"] > 0
            has_power_excess = positive_power.any()
            # TODO: This is a big reduce-step. We should get this down by getting the power analysis time down.
            self.plane.mtow -= 1
            print("New MTOW: {}".format(self.plane.mtow))
            if self.plane.mtow > 0:
                self.power_available()
                self.power_required()
                self.power_excess()
            else:
                self.plane.mtow = 0
                print("Aircraft cannot sustain flight even with zero weight")

        self.get_V_min_max()

    def power_required(self):
        thrust_required_dict = {}
        power_required_dict = {}
        alpha_dict = {}
        for velocity in self.velocity_range:
            total_lift = 0
            alpha = self.plane.stall_min
            while total_lift < self.plane.mtow * 9.81:
                alpha += 0.1
                total_lift = self.wing1.lift(self.rho, velocity, alpha) - self.hs.lift(
                    self.rho, velocity, alpha
                )
                if self.plane.plane_type == "biplane":
                    total_lift += self.wing2.lift(self.rho, velocity, alpha)
                if alpha >= self.plane.stall_max:
                    alpha_nivel = None
                    break
                else:
                    alpha_nivel = alpha

            thrust_required = (
                drag(self.rho, velocity, self.plane.S_tp, self.plane.CD_tp)
                + drag(self.rho, velocity, self.plane.S_fus, self.plane.CD_fus)
                + self.wing1.drag(self.rho, velocity, alpha_nivel)
                + self.wing2.drag(self.rho, velocity, alpha_nivel)
                + self.hs.drag(self.rho, velocity, alpha_nivel)
            )

            alpha_dict[velocity] = alpha_nivel
            thrust_required_dict[velocity] = thrust_required

        for velocity in thrust_required_dict:
            power_required_dict[velocity] = thrust_required_dict[velocity] * velocity

        self.thrust_required_dict = thrust_required_dict
        self.power_required_dict = power_required_dict
        self.alpha_dict = alpha_dict
        self.alpha_df = dict_to_dataframe(alpha_dict, "Alpha", "Velocity")
        self.thrust_required_df = dict_to_dataframe(
            thrust_required_dict, "Thrust required", "Velocity"
        )
        self.power_required_df = dict_to_dataframe(
            power_required_dict, "Power required", "Velocity"
        )

        return self.alpha_df, self.thrust_required_df, self.power_required_df

    def power_available(self):
        thrust_available_dict = {}
        power_available_dict = {}

        for velocity in self.velocity_range:
            thrust_available = self.plane.motor.thrust(velocity)
            thrust_available_dict[velocity] = thrust_available

        for velocity in thrust_available_dict:
            power_available_dict[velocity] = thrust_available_dict[velocity] * velocity

        self.thrust_available_dict = thrust_available_dict
        self.power_available_dict = power_available_dict

        self.thrust_available_df = dict_to_dataframe(
            thrust_available_dict, "Thrust available", "Velocity"
        )
        self.power_available_df = dict_to_dataframe(
            power_available_dict, "Power available", "Velocity"
        )

        return self.thrust_available_df, self.power_available_df

    def power_excess(self):
        power_excess_dict = {}
        for velocity in self.power_available_dict:
            power_required = self.power_required_dict[velocity]
            power_available = self.power_available_dict[velocity]
            power_excess_dict[velocity] = power_available - power_required
        self.power_excess_dict = power_excess_dict
        self.power_excess_df = dict_to_dataframe(
            power_excess_dict, "Power excess", "Velocity"
        )

    def get_V_min_max(self):
        roots = find_df_roots(self.power_excess_df, "Power excess")
        if len(roots) == 1:
            self.plane.V_min = self.plane.V_stall
            self.plane.V_max = roots[0]
            alpha_max = self.alpha_df.max()[0]
        elif len(roots) == 2:
            self.plane.V_min = roots[0]
            self.plane.V_max = roots[1]
            alpha_max = np.interp(
                self.plane.V_min, self.alpha_df.index.values, self.alpha_df["Alpha"]
            )
        elif len(roots) == 0:
            self.plane.V_min = self.plane.V_stall
            self.plane.V_max = np.amax(self.velocity_range)
            alpha_max = self.alpha_df.max()[0]
        self.plane.alpha_min = self.alpha_dict[self.plane.V_max]

        print("Alpha_max: {}".format(alpha_max))
        self.plane.alpha_max = alpha_max
