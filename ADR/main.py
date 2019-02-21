from ADR import parameters
from ADR.Components.Plane import Plane
from ADR.Analysis.Performance.Takeoff import Takeoff
from ADR.Analysis.Performance.Power import Power
from ADR.Analysis.Stability.FlightStability.FlightStability import FlightStability

from matplotlib import pyplot as plt
import numpy as np

plane_data = parameters.plane_data()
performance_data = parameters.performance_data()

plane = Plane(plane_data)

takeoff_analysis = Takeoff(plane, performance_data)
mtow = takeoff_analysis.get_mtow()
print('MTOW is {}'.format(mtow))

flight_stability = FlightStability(plane)
CM_plane_on_CG_fixed = flight_stability.CM_plane_CG(plane.cg)

power_analysis = Power(plane, performance_data)
print('Vmin is {} for AlphaMax of {}'.format(plane.V_min, plane.alpha_max))
print('Vmax is {} for AlphaMin of {}'.format(plane.V_max, plane.alpha_min))
