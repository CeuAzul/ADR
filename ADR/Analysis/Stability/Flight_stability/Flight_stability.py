"""
Origem: Bordo de ataque da asa raiz
"""

# Descobre o intervalo aceitavel de posicionamento do CG
import math
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

from ADR.Components.Planes.Aerodynamic_surfaces.Wing import Wing
from ADR.Components.Planes.Aerodynamic_surfaces.EH import EH
from ADR.Components.Planes.References.Static_margin import SM
from ADR.Analysis.Stability.Flight_stability.Momentum_CG import wing_momentum
from ADR.Analysis.Stability.Flight_stability.Momentum_CG import tail_momentum

# --- Reescreve arquivos do X5 --- #
'''
# processando arquivos de dados do x5
file1 = open("X5_files2/Asa.txt", "r")
file2 = open("X5_files2/Asa_escrita.txt", "wt")
for line in file1:
    file2.write(' '.join(line.split()) + '\n')
file1.close()
file2.close()
file1 = open("X5_files2/Profundor.txt", "r")
file2 = open("X5_files2/Profundor_escrito.txt", "wt")
for line in file1:
    file2.write(' '.join(line.split()) + '\n')
file1.close()
file2.close()
file1 = open("X5_files2/Aviao.txt", "r")
file2 = open("X5_files2/Aviao_escrito.txt", "wt")
for line in file1:
    file2.write(' '.join(line.split()) + '\n')
file1.close()
file2.close()
'''

### inputs variáveis
# wing 1
pd_wing = pd.read_csv('X5_files2/Asa_escrita.txt', skiprows=7, sep=' ')
clw_wh = pd_wing.loc[:, 'CL'].values
cdw_wh = pd_wing.loc[:, 'CD'].values
cmw = -0.32

# tail
pd_tail = pd.read_csv('X5_files2/Profundor_escrito.txt', skiprows=7, sep=' ')
clt_wh = pd_tail.loc[:, 'CL'].values
cdt_wh = pd_tail.loc[:, 'CD'].values
cmt = 0.092

# Aviao
pd_plane = pd.read_csv('X5_files2/Aviao_escrito.txt', skiprows=7, sep=' ')
clp_wh = pd_plane.loc[:, 'CL'].values
cdp_wh = pd_plane.loc[:, 'CD'].values

# Angulos de ataque a serem usados
alpha_graus_wh = pd_plane.loc[:, 'alpha'].values

alpha_graus = []
clw = []
cdw = []
clt_reversed = []
cdt_reversed = []
clt = []
cdt = []
clp = []
cdp = []

# --- Excluindo termos com casas decimais --- #
for i in range(len(alpha_graus_wh)):
    if i % 2 == 0:
        alpha_graus.append(alpha_graus_wh[i])
        clw.append(clw_wh[i])
        cdw.append(cdw_wh[i])
        clp.append(clp_wh[i])
        cdp.append(cdp_wh[i])
        clt_reversed.append(-clt_wh[i])
        cdt_reversed.append(cdt_wh[i])

# --- Invertendo o perfil do profundor --- #
for i in reversed(clt_reversed):
    clt.append(i)
for i in reversed(cdt_reversed):
    cdt.append(i)


# --- Inputs --- #

SM = SM()

Wing1 = Wing({
    "CL": clw, "CD": cdw, "CM": cmw,
    "area": 0.45, "X_CA": 0.0625, "H_CA": 0, "downwash_angle": 0,
    "chord": 0.25, "stall_min": -15, "stall_max": 15, "incidence": 0
})

Wing2 = Wing({
    "CL": clw, "CD": cdw, "CM": cmw,
    "area": 0.45, "X_CA": 0.0625, "H_CA": 0.7, "downwash_angle": 0,
    "chord": 0.25, "stall_min": -15, "stall_max": 15, "incidence": 0
})

EH = EH({
    "CL": clt, "CD": cdt, "CM": cmt,
    "area": 0.083, "X_CA": 0.7625, "H_CA": 0.1,
    "chord": 0.1775, "stall_min": -15, "stall_max": 15, "incidence": 0
})

# ------ #

# Variáveis internas

# Posicao da origem em relacao a usada na competicao
# 0.1528-Wing.CA.getX()
# 0.1275

Xcg_min = 0.0
Xcg_max = 0.1
Xcg_div = 4  # n de divisões entre min e max

Hcg_min = -0.1
Hcg_max = 0
Hcg_div = 4

# ME e alpha
SM_min = 0.01
SM_max = 0.2
CM_min = -0.05
CM_max = 0.05

X_CG = 0.0725
H_CG = 0#.02279068177

# From grads to rad
def toRad(graus):
    return [(i * math.pi / 180) for i in graus]

# ------ #


CM = []
ME = []
status_CM = {}
status_ME = {}
dCMda = []
den = 0

stall_min = max(Wing1.stall_min, Wing2.stall_min)
stall_max = min(Wing1.stall_max, Wing2.stall_max)
incidence_min = min(Wing1.incidence, Wing2.incidence)
incidence_max = max(Wing1.incidence, Wing2.incidence)

alpha_plane_min = stall_min - incidence_min
alpha_plane_max = stall_max - incidence_max

alpha_plane_range = range(alpha_plane_min, alpha_plane_max + 1)

# ------ Analise ------ #


def flight_stability(plane_type):

    print("Tipo de aviao = ", plane_type)
    print("X_CG = ", X_CG)
    print("H_CG = ", H_CG)
    print()

    print("Wing1")
    print("\tWing1.CL = ", Wing1.CL)
    print("\tWing1.CD = ", Wing1.CD)
    print("\tWing1.CM = ", Wing1.CM)
    print("\tWing1.area = ", Wing1.area)
    print("\tWing1.chord = ", Wing1.chord)
    print("\tWing1.X_CA = ", Wing1.CA.getX())
    print("\tWing1.H_CA = ", Wing1.CA.getH())
    print()

    print("EH")
    print("\tEH.CL = ", EH.CL)
    print("\tEH.CD = ", EH.CD)
    print("\tEH.CM = ", EH.CM)
    print("\tEH.area = ", EH.area)
    print("\tEH.chord = ", EH.chord)
    print("\tEH.X_CA = ", EH.CA.getX())
    print("\tEH.H_CA = ", EH.CA.getH())
    print()

    print("alpha_plane_range = ", alpha_plane_range, "\n")

    for alpha_plane in alpha_plane_range:

        alpha_wing1 = alpha_plane + Wing1.incidence
        alpha_wing2 = alpha_plane + Wing2.incidence

        index_aw1 = alpha_wing1 + abs(Wing1.stall_min)
        index_aw2 = alpha_wing1 + abs(Wing2.stall_min)
        index_ap = alpha_plane + abs(alpha_plane_min)

        wing_m = wing_momentum(plane_type, X_CG, H_CG,
                               Wing1.CL, Wing1.CD, Wing1.CM, index_aw1, Wing1.chord, Wing1.area, Wing1.CA.getX(), Wing1.CA.getH(),
                               Wing2.CL, Wing2.CD, Wing2.CM, index_aw2, Wing2.chord, Wing2.area, Wing2.CA.getX(), Wing2.CA.getH(),
                               alpha_plane)

        CM.append([])
        ME.append([])
        dCMda.append([])

        for alpha_tail in range(EH.stall_min, EH.stall_max + 1):
            index_at = alpha_tail + abs(EH.stall_min)

            tail_m = tail_momentum(X_CG, H_CG,
                                   EH.CL, EH.CD, EH.CM, index_at, EH.chord, EH.area, EH.incidence,
                                   EH.CA.getX(), EH.CA.getH(),
                                   Wing1.chord, Wing1.area, Wing1.downwash_angle,
                                   alpha_plane)

            CM_sum = wing_m + tail_m  # Momento total do aviao no CG

            # --- Verifica a qualidade de voo --- #

            # Calcula a margem estatica
            SM.set(Wing1.CL, Wing1.CD, index_aw1, Wing1.area,
                   Wing2.CL, Wing2.CD, index_aw2, Wing2.area,
                   EH.CL, EH.CD, index_at, EH.area, EH.incidence,
                   Wing1.downwash_angle, 0.9, CM_sum,
                   alpha_plane)


            # Interpolar grafico em 2º ordem e achar zero - Moreno, 2019
            if alpha_plane != alpha_plane_min:
                if CM_min < CM_sum < CM_max:
                    status_CM[alpha_plane] = alpha_tail

                if SM_min < SM.get() < SM_max:
                    status_ME[index_ap] = alpha_tail

            ME[index_ap].append(SM.get())
            CM[index_ap].append(CM_sum)


# ------- Resultados ------- #
# APAGUEI TEUS EIXO X DOS PLOTS
# A TRETA TA NA INDEXAÇÃO DOS VETORES PRA CATAR OS COEFS

    plt.figure(3)
    plt.grid()
    plt.xlabel("Ânglo alpha do avião")
    plt.ylabel("Coeficiente de momento no CG")
    plt.title("Momento da aeronave para diferentes angulos de ataque e EH")
    plt.plot(alpha_plane_range, CM)

    plt.figure(2)
    plt.grid()
    plt.xlabel("Ânglo alpha do avião")
    plt.ylabel("ME")
    plt.title("ME da aeronave para diferentes angulos de ataque e EH")
    plt.plot(alpha_plane_range, ME)

    plt.figure(1)
    a=[]
    for i in status_CM:
        plt.plot(i, status_CM.get(i), "o")
    plt.grid()
    plt.xlabel("Alpha plane")
    plt.ylabel("Alpha EH")
    plt.title("Pontos de trimagem")

    plt.show()


# Chama flight_stability
flight_stability("monoplane")
