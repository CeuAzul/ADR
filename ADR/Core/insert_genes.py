from numpy import interp
from ADR.Core.Optmizer.opt_config import plane_parameters_selector
from ADR.Core.Optmizer.opt_bounds import plane_parameters_bounds
from ADR.Core.Optmizer.opt_force import get_forced_parameters
from ADR import parameters
from ADR.Core.data_manipulation import replace_forced_parameters

def num_opt_params():
    num_opt_params = 0
    for param, optmize in plane_parameters_selector.items():
        if optmize == True:
            num_opt_params += 1
    return num_opt_params

def generate_forced_parameters(original_parameters, genes):

    geneticized_parameters = change_params_from_genes(genes)
    forced_parameters = get_forced_parameters(original_parameters, geneticized_parameters)

    forced_parameters = replace_forced_parameters(geneticized_parameters, forced_parameters)

    print('----- Forced optmized parameters -----')
    for key, value in forced_parameters.items():
        print('{} : {:.3f}'.format(key, value))
    print('-----------------------------------------')

    return forced_parameters

def change_params_from_genes(genes):
    genes_bounds = [0,1]

    geneticized_parameters = {}
    gene_index = 0
    for param, optmize in plane_parameters_selector.items():
        if optmize == True:
            geneticized_parameters[param] = interp(genes[gene_index], genes_bounds, plane_parameters_bounds.get(param))
            gene_index += 1

    # print('----- Original optmized parameters -----')
    # for key, value in geneticized_parameters.items():
    #     print('{} : {:.3f}'.format(key, value))
    # print('-----------------------------------------')
    return geneticized_parameters

