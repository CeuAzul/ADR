from ADR import parameters
from ADR.Components.Plane import Plane
from ADR.Analysis.Performance.Power import Power

if __name__ == "__main__":
    plane_data = parameters.plane_data()

    plane = Plane(plane_data)
    power_analysis = Power(plane)