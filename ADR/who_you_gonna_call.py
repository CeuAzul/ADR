from ADR.main import adr_analyser

# Insert your list of genes (or leave it as is)
genes = [0.14, 0.74, 0.51, 0.18, 0.34, 0.33, 0.05, 0.74, 0.46]

# Choose between using the genes or not
use_genes = False

# Choose between running with the default parameters or your own:
use_my_own_parameters = False

# Choose between plotting the analysis curves or not
plot = True

adr_analyser(plot, use_my_own_parameters, use_genes, genes)