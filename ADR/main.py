from ADR import parameters
from ADR.Components.Plane import Plane
from ADR.Analysis.Performance.Takeoff import Takeoff
from ADR.Analysis.Stability.FlightStability.FlightStability import FlightStability
from ADR.Analysis.WeightEstimative.Boom import Boom

plane_data = parameters.plane_data()
takeoff_data = parameters.takeoff_data()
mass_data = parameters.mass_data()

plane = Plane(plane_data)

takeoff_analysis = Takeoff(plane, takeoff_data)
mtow = takeoff_analysis.get_mtow()
print('Final MTOW is {}'.format(mtow))

flight_stability = FlightStability(plane)

boom = Boom(plane_data, mass_data)
print(boom.weight)