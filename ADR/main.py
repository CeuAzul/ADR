from ADR import parameters
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

from matplotlib import pyplot as plt
import numpy as np

plot = True

plane_data = parameters.plane_data()
performance_data = parameters.performance_data()

plane = Plane(plane_data)

takeoff_analysis = Takeoff(plane, performance_data)
mtow = takeoff_analysis.get_mtow()
plot_takeoff_data(takeoff_analysis, mtow)

print('Initial MTOW is {}'.format(mtow))

flight_stability = FlightStability(plane)
flight_stability.CM_plane_CG(plane.cg)
flight_stability.static_margin()
plot_stability_data(flight_stability)

power_analysis = Power(plane, performance_data)
plot_power_curves(power_analysis)

trimm_range_checker = TrimmRangeChecker(plane)
trimm_range_checker.check()

sm_checker = StaticMarginChecker(plane)
sm_checker.check()

maybe_an_assassin = MaybeAnAssassin(plane)
maybe_an_assassin.score_or_kill()

print('Final MTOW is {}'.format(mtow))

if plot == True:
    plt.show()
