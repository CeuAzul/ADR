from ADR import parameters
from ADR.Core.insert_genes import generate_forced_parameters
from ADR.Core.data_manipulation import save_dict
from ADR.Components.Plane import Plane
from ADR.Analysis.Performance.Takeoff import Takeoff
from ADR.Analysis.Performance.run_Takeoff import plot_takeoff_data
from ADR.Analysis.Performance.Power import Power
from ADR.Analysis.Performance.run_Power import plot_power_curves
from ADR.Analysis.Stability.FlightStability.FlightStability import FlightStability
from ADR.Analysis.Stability.FlightStability.run_FlightStability import (
    plot_stability_data,
)
from ADR.Analysis.Aerodynamics.AerodynamicPlots import plot_aerodynamic_data

from ADR.Checkers.TrimmRange import TrimmRangeChecker
from ADR.Checkers.StaticMargin import StaticMarginChecker
from ADR.Checkers.Scoreboard import MaybeAnAssassin
from ADR.Checkers.Dimensions import Ruler

from matplotlib import pyplot as plt
import numpy as np

import traceback
import logging


def adr_optmizer(genes):
    forced_parameters = generate_forced_parameters(
        parameters.original_plane_parameters, genes
    )
    score = adr_analyser(forced_parameters=forced_parameters)
    return score


def adr_analyser(plot=False, use_ready_airplane=False, forced_parameters={}):

    try:
        plane_parameters = parameters.plane_parameters(forced_parameters)
        performance_data = parameters.performance_parameters(forced_parameters)

        plane = Plane(plane_parameters)
        plane.show_plane()

        takeoff_analysis = Takeoff(plane, performance_data)
        mtow = takeoff_analysis.get_mtow()

        print("Initial MTOW is {}".format(mtow))

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

        print("Final MTOW is {}".format(plane.mtow))

        if plot == True:
            plot_takeoff_data(takeoff_analysis, mtow)
            plot_stability_data(flight_stability)
            plot_power_curves(power_analysis)
            plot_aerodynamic_data(plane)
            plt.show()

        if plane.dead == True:
            save_dict(plane_parameters, performance_data, mtow, "dead")
        else:
            save_dict(plane_parameters, performance_data, mtow, "alive")
        return (plane.score,)

    except Exception as e:
        logging.error(traceback.format_exc())
        print(
            "-----------------------------------Error-----------------------------------"
        )
        return (0,)


if __name__ == "__main__":
    plot = True
    adr_analyser(plot=True)
