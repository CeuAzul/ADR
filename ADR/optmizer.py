import numpy

from deap import algorithms
from deap import base
from deap import benchmarks
from deap import cma
from deap import creator
from deap import tools

import random

from ADR.main import adr_analyser
from ADR.parameters_optmizer import plane_data, enter_parameters

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.uniform, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=9)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", adr_analyser)

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.10)
toolbox.register("select", tools.selTournament, tournsize=2)

def main():
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(5)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=5, stats=stats, halloffame=hof, verbose=True)

    return pop, logbook, hof

if __name__ == "__main__":
    pop, log, hof = main()

    print("Individual #{} is: {}\nwith fitness: {}".format(1, hof[0], hof[0].fitness))
    print("Individual #{} is: {}\nwith fitness: {}".format(2, hof[1], hof[1].fitness))
    print("Individual #{} is: {}\nwith fitness: {}".format(3, hof[2], hof[2].fitness))
    print("Individual #{} is: {}\nwith fitness: {}".format(4, hof[3], hof[3].fitness))
    print("Individual #{} is: {}\nwith fitness: {}".format(5, hof[4], hof[4].fitness))

    import matplotlib.pyplot as plt
    gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
    plt.plot(gen, avg, label="average")
    plt.plot(gen, min_, label="minimum")
    plt.plot(gen, max_, label="maximum")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(loc="lower right")
    plt.show()