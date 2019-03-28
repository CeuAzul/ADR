import numpy

from deap import algorithms
from deap import base
from deap import benchmarks
from deap import cma
from deap import creator
from deap import tools

import random

from ADR.main import adr_optmizer
from ADR.Core.insert_genes import num_opt_params

N = num_opt_params()

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.uniform, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=N)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", adr_optmizer)

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.10)
toolbox.register("select", tools.selTournament, tournsize=2)

def main(population=20, generations=5, crossover_pb=0.5, mutation_pb=0.2, hallf_of_fame=5):
    pop = toolbox.population(n=population)
    hof = tools.HallOfFame(hallf_of_fame)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=crossover_pb, mutpb=mutation_pb, ngen=generations, stats=stats, halloffame=hof, verbose=True)

    return pop, logbook, hof

if __name__ == "__main__":
    pop, log, hof = main()

    for i, individual in enumerate(hof):
        print("Individual #{} is: {}\nwith fitness: {}".format(i+1, individual, individual.fitness))

    import matplotlib.pyplot as plt
    gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
    plt.plot(gen, avg, label="average")
    plt.plot(gen, min_, label="minimum")
    plt.plot(gen, max_, label="maximum")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(loc="lower right")
    plt.show()