from ADR.main import adr_analyser
from ADR.optmizer import main

import matplotlib.pyplot as plt

# Insert your list of genes (or leave it as is):
genes = [0.636, 0.496, 0.491, 0.868, 0.383, 0.709, 0.0, 0.770, 0.037]

# Choose between using the genes or not:
use_genes = True

# Choose between running with the default parameters or your own:
use_my_own_parameters = False

# Choose between plotting the analysis curves or not:
plot = True

# Choose between running the optmizer instead of the analyser:
run_optmizer = False

# Define the optmizer parameters:
opt_population = 2
opt_generations = 1
opt_crossover = 0.5
opt_mutation = 0.2
opt_halloffame = 2

# Remeber that the optmizer uses the my_own_parameters file, so edit the defaults there if needed



# Those are the callers, you don't need to edit those lines:
if not run_optmizer:
    adr_analyser(genes, plot, use_my_own_parameters, use_genes)
else:
    pop, log, hof = main(opt_population, opt_generations, opt_crossover, opt_mutation, opt_halloffame)

    for i, individual in enumerate(hof):
        print("Individual #{} is: {}\nwith fitness: {}".format(i+1, individual, individual.fitness))
