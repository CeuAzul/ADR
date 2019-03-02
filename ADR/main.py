from ADR import parameters, my_own_parameters
from ADR.Core.insert_genes import generate_forced_parameters
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

def adr_analyser(genes, plot=False, use_own_parameters=True, use_genes=True):

    try:

        if use_genes:
            forced_parameters = generate_forced_parameters(genes)
        else:
            forced_parameters = {}

        if use_own_parameters:
            plane_parameters = my_own_parameters.plane_parameters(forced_parameters)
            performance_data = my_own_parameters.performance_parameters(forced_parameters)
        else:
            plane_parameters = parameters.plane_parameters(forced_parameters)
            performance_data = parameters.performance_parameters(forced_parameters)

        plane = Plane(plane_parameters)
        plane.show_plane()

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
        print("-----------------------------------Error-----------------------------------")
        return 0,

if __name__ == "__main__":
    plot = True
    adr_analyser(plot=True, use_own_parameters=False, use_genes=True, genes=[0.636, 0.496, 0.491, 0.868, 0.383, 0.709, 0.0, 0.770, 0.037])