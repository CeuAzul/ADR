from ADR.main import adr_analyser
from ADR.optmizer import main

import matplotlib.pyplot as plt

# Choose between using a ready_airplane or not. If True, the runner will
# use the ready_airplane file. If False, it will use the default_parameters file:
use_ready_airplane = True

# Choose between plotting the analysis curves or not:
plot = True

# Choose between running the optmizer instead of the analyser:
run_optmizer = True

# Define the optmizer parameters:
opt_population = 20
opt_generations = 5
opt_crossover = 0.5
opt_mutation = 0.2
opt_halloffame = 2

# Those are the callers, you don't need to edit those lines:
if not run_optmizer:
    adr_analyser(plot, use_ready_airplane)
else:
    pop, log, hof = main(opt_population, opt_generations, opt_crossover, opt_mutation, opt_halloffame)

    for i, individual in enumerate(hof):
        print("Individual #{} is: {}\nwith fitness: {}".format(i+1, individual, individual.fitness))
