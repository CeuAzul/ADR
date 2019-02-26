from ADR import parameters
from ADR import parameters_optmizer
from ADR.Components.Plane import Plane
from ADR.Analysis.Performance.Takeoff import Takeoff
from ADR.Analysis.Performance.test_Takeoff import plot_takeoff_data
from ADR.Analysis.Performance.Power import Power
from ADR.Analysis.Performance.test_Power import plot_power_curves
from ADR.Analysis.Stability.FlightStability.FlightStability import FlightStability
from ADR.Analysis.Stability.FlightStability.test_FlightStability import plot_stability_data

from ADR.Checkers.TrimmRange import TrimmRangeChecker
from ADR.Checkers.StaticMargin import StaticMarginChecker
from ADR.Checkers.Scoreboard import MaybeAnAssassin
from ADR.Checkers.Dimensions import Ruler

from matplotlib import pyplot as plt
import numpy as np

import traceback
import logging

plot = False

def adr_analyser(optmizer_list):

    try:
        if len(optmizer_list) != 0:
            airplane_var_data = parameters_optmizer.enter_parameters(optmizer_list)
            plane_data = parameters_optmizer.plane_data(airplane_var_data)
            performance_data = parameters_optmizer.performance_data()
        else:
            plane_data = parameters.plane_data()
            performance_data = parameters.performance_data()

        plane = Plane(plane_data)
        plane.show_plane()

        print('Plane parameters: {}'.format(optmizer_list))

        takeoff_analysis = Takeoff(plane, performance_data)
        mtow = takeoff_analysis.get_mtow()

        print('Initial MTOW is {}'.format(mtow))

        flight_stability = FlightStability(plane)
        flight_stability.CM_plane_CG(plane.cg)
        flight_stability.static_margin()

        power_analysis = Power(plane, performance_data)

        trimm_range_checker = TrimmRangeChecker(plane)
        trimm_range_checker.check()

        sm_checker = StaticMarginChecker(plane)
        sm_checker.check()

        ruler = Ruler(plane)
        ruler.measure()

        maybe_an_assassin = MaybeAnAssassin(plane)
        maybe_an_assassin.score_or_kill()

        print('Final MTOW is {}'.format(plane.mtow))

        if plot == True:
            plot_takeoff_data(takeoff_analysis, mtow)
            plot_stability_data(flight_stability)
            plot_power_curves(power_analysis)
            plt.show()

        return plane.score,

    except Exception as e:
        logging.error(traceback.format_exc())
        print("--------------------------------sefsdfdsf---Error-----------------------------------")
        return 0,

if __name__ == "__main__":
    plot = True
    plane_data = parameters.plane_data()
    adr_analyser([0.13871328223159263, 0.7440855281071194, 0.5122958759754443, 0.1770265953909208, 0.3423403831822237, 0.32601107216390657, 0.04757035250450403, 0.739722623828638, 0.45727374696035916])