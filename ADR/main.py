import ADR
from ADR import parameters

if __name__ == "__main__":
    plane_parameters = parameters.get_plane_parameters()
    performance_parameters = parameters.get_performance_parameters()

    ADR.analyzer(plane_parameters, performance_parameters, plot=True)
