import subprocess
import os
from math import radians
import numpy as np
import pandas as pd
from get_cl_max import get_clmax
from io_avl import get_value, set_dimensions

def change_dimensions(data):

    surface_name = data.get("surface_name")
    LE_x_location = data.get("LE_x_location")
    LE_z_location = data.get("LE_z_location")
    airfoil1_name = data.get("airfoil1_name")
    airfoil2_name = data.get("airfoil2_name")
    airfoil3_name = data.get("airfoil3_name")
    span1 = data.get("span1")
    span2 = data.get("span2")
    chord1 = data.get("chord1")
    chord2 = data.get("chord2")
    chord3 = data.get("chord3")
    twist1 = data.get("twist1")
    twist2 = data.get("twist2")
    twist3 = data.get("twist3")
    incidence = data.get("incidence")

    dir_name = os.path.dirname(os.path.abspath(__file__))
    airfoils_path = os.path.join(dir_name, 'airfoils')
    
    config_file = os.path.join(dir_name, 'configs.avl')
    
    airfoil1_file = os.path.join(airfoils_path, airfoil1_name + '.dat')
    airfoil2_file = os.path.join(airfoils_path, airfoil2_name + '.dat')
    airfoil3_file = os.path.join(airfoils_path, airfoil3_name + '.dat')

    set_dimensions(config_file, airfoil1_file, airfoil2_file, airfoil3_file,
                   surface_name, LE_x_location, 0, span1, span1+span2, LE_z_location, chord1, chord2, chord3,
                   incidence, twist1, twist2, twist3)


def get_aero_coef(Cl_max_airfoil):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(dir_name, 'configs.avl')
    outputs_path = os.path.join(dir_name, 'outputs')
    output_file = os.path.join(outputs_path, 'coeficients.txt')
    output2_file = os.path.join(outputs_path, 'coeficients_along_span.txt')
    avl_file = os.path.join(dir_name, 'avl.exe')

    alpha_range = np.arange(-20, 21, 1)

    CL_dict = {}
    CD_dict = {}
    Cm_dict = {}

    open(output_file, 'a').close()
    open(output2_file, 'a').close()
    

    for alpha in alpha_range:
        os.remove(output_file)
        os.remove(output2_file)
        comm_string = 'load {}\n oper\n a\n a\n {}\n x\n ft\n{}\nfs\n{}\n'.format(config_file, alpha, output_file, output2_file)
        Process=subprocess.Popen([avl_file], stdin=subprocess.PIPE, shell = True)
        Process.communicate(bytes(comm_string, encoding='utf8'))
        if get_clmax(output2_file) > Cl_max_airfoil:
            break
        else:
            CL_dict[alpha] = get_value(output_file, 'CLtot')
            CD_dict[alpha] = get_value(output_file, 'CDtot')
            Cm_dict[alpha] = get_value(output_file, 'Cmtot')

    CL_df = pd.DataFrame.from_dict(CL_dict,  orient="index", columns=["CL"])
    CL_df.index.name = 'alpha'
    CD_df = pd.DataFrame.from_dict(CD_dict,  orient="index", columns=["CD"])
    CD_df.index.name = 'alpha'
    Cm_df = pd.DataFrame.from_dict(Cm_dict,  orient="index", columns=["CM"])
    Cm_df.index.name = 'alpha'

    return CL_dict, CD_dict, Cm_dict, CL_df, CD_df, Cm_df
