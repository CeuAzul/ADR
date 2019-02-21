from matplotlib import pyplot as plt
import numpy as np
from avl_runner import get_aero_coef
from avl_runner import change_dimensions
        
data_wing = {
    "surface_name": 'wing',
    "cl_max_airfoil": 2.2,
    "airfoil1_name": 's1223',
    "airfoil2_name": 's1223',
    "airfoil3_name": 's1223',
    "LE_x_location" : 0,
    "LE_z_location" : 0,
    "span1": 0.4,
    "span2": 0.4,
    "chord1": 0.4,
    "chord2": 0.3,
    "chord3": 0.2,
    "twist1": 0,
    "twist2": 0,
    "twist3": 0,
    "incidence": 0
}

change_dimensions(data_wing)

CLdic, CDdic, Cmdic, CL_df, CD_df, Cm_df = get_aero_coef(data_wing.get('cl_max_airfoil'))

plt.plot(CL_df, label = 'CL')
plt.plot(CD_df, label = 'CD')
plt.plot(Cm_df, label = 'Cm')
plt.legend()
plt.grid()
plt.show()
