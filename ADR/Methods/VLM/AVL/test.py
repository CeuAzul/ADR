from matplotlib import pyplot as plt

from avl_runner import get_aero_coeffs

data = {
    "airfoil1_name": 's1223',
    "airfoil2_name": 's1223',
    "airfoil3_name": 's1223',
    "span1": 0.45,
    "span2": 0.45,
    "chord1": 0.30,
    "chord2": 0.20,
    "chord3": 0.10,
    "twist1": 0,
    "twist2": 0,
    "twist3": 0,
    "incidence": 0
}

CL_df, CD_df, Cm_df = get_aero_coeffs(data)

plt.plot(CL_df, label = 'CL')
plt.plot(CD_df, label = 'CD')
plt.plot(Cm_df, label = 'Cm')
plt.legend()
plt.grid()
plt.show()
