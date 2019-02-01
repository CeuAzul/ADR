import math
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os

from ADR.Analysis.Performance.Motor import Motor
from ADR.Components.Planes.Aerodynamic_surfaces.Wings import Wing

wing = Wing()

dir_path = os.path.dirname(os.path.realpath(__file__))

s1223_df = pd.read_csv(dir_path + '\s1223.csv', skiprows=10, index_col=0)
s1223_cl = s1223_df[["Cl"]]
s1223_cd = s1223_df[["Cd"]]
s1223_cm = s1223_df[["Cm"]]

motor = Motor()
E = motor.get_take_off_thrust() # Empuxo [N]

theta_airplane_deg = 0 # Angulo do aviao com a pista [°]
theta_airplane_rad = math.radians(theta_airplane_deg) # Angulo do aviao com a pista [rad]
rho_air = 1.225 # Densidade do ar [kg/m^3]
m = 20 # Massa total do aviao [kg]
g = 9.81 # Constante gravitacional [m/s^2]
I_airp = 0.2 # Momento de Inercia da aeronave []

V_x = 0 # Velocidade inicial do aviao no eixo X [m/s]
V_y = 0 # Velocidade inicial do aviao no eixo Y [m/s]

S_w = 2 # Area de asa [m^2]
S_vs = 0.2 # Area do estabilizdor horizontal [m^2]

C_D_0_w = 0.2 # Coeficiente de arrasto de pressao da asa
C_D_0_vs = 0.2 # Coeficiente de arrasto de pressao do estabilizdor horizontal
C_D_tp = 0.02 # Coeficiente de arrasto do trem de pouso
C_D_fus = 0.02 # Coeficiente de arrasto da fuselagem

C_L_w = 2.0 # Coeficiente de sustentaçao da asa
C_L_vs = 2.0 # Coeficiente de sustentaçao do estabilizdor horizontal

f_f = 0.01 # Coeficiente de atrito dinamico da roda frontal
f_r = 0.01 # Coeficiente de atrito dinamico da roda traseira

d_L_w_cg = 0.1 # Distancia da resultante das forças na Asa ao CG
d_L_vs_cg = 0.9 # Distancia da resultante das forças no profundor ao CG

_t = []
_V_x = []
_dist_x = []
_N = []

dist_x = 0 # Distancia percorrida em X [m]
N = 0.1 # Força normal [N]
t = 0 # Tempo [s]
dt = 0.001 # Incremento discreto de tempo [s]

def calc_drag(rho, V, S, C_D):
    Drag = 0.5*rho*V**2*S*C_D
    return Drag

def calc_lift(rho, V, S, C_L):
    Lift = 0.5*rho*V**2*S*C_L
    return Lift

def calc_moment(rho, V, S, C_M):
    Moment = 0.5*rho*V**2*S*C_M
    return Moment

while(N>0):
    alpha_w = 0
    alpha_vs = 0
    alpha_theta_w = theta_airplane_deg + alpha_w
    alpha_theta_vs = theta_airplane_deg + alpha_vs

    C_L_w = np.interp(alpha_theta_w, s1223_cl.index.values, s1223_cl['Cl'])
    C_D_w = np.interp(alpha_theta_w, s1223_cd.index.values, s1223_cd['Cd'])
    C_M_w = np.interp(alpha_theta_w, s1223_cm.index.values, s1223_cm['Cm'])

    C_L_vs = np.interp(alpha_theta_vs, s1223_cl.index.values, s1223_cl['Cl'])
    C_D_vs = np.interp(alpha_theta_vs, s1223_cd.index.values, s1223_cd['Cd'])
    C_M_vs = np.interp(alpha_theta_vs, s1223_cm.index.values, s1223_cm['Cm'])

    t = t + dt
    L_w = calc_lift(rho_air, V_x, S_w, C_L_w)
    L_vs = calc_lift(rho_air, V_x, S_vs, C_L_vs)
    E_y = E*math.sin(theta_airplane_rad)
    W = m*g

    N = W + L_vs - L_w - E_y

    E_x = E*math.cos(theta_airplane_rad)
    D_w = calc_drag(rho_air, V_x, S_w, C_D_w)
    D_vs = calc_drag(rho_air, V_x, S_vs, C_D_vs)
    D_tp = calc_drag(rho_air, V_x, S_w, C_D_tp)
    D_fus = calc_drag(rho_air, V_x, S_w, C_D_fus)
    F_at_f = f_f*N
    F_at_r = f_r*N

    dV_x = ((E_x - D_w - D_vs - D_tp - D_fus - F_at_f - F_at_r)/m) * dt
    V_x = V_x + dV_x
    dist_x = dist_x + V_x * dt

    _t.append(t)
    _V_x.append(V_x)
    _N.append(N)
    _dist_x.append(dist_x)

    M_w = calc_moment(rho_air, V_x, S_w, C_M_w)
    M_vs = calc_moment(rho_air, V_x, S_vs, C_M_vs)
    dTheta = (((M_vs - M_w + L_w*d_L_w_cg + L_vs*d_L_vs_cg)/I_airp)*dt)*dt
    if dTheta > 0:
        theta_airplane_deg = theta_airplane_deg + dTheta

    print('Angulo da aeronave: ' + str(theta_airplane_deg))

vel_plot, = plt.plot(_t, _V_x)
vel_plot.set_label('Velocidade')

dist_plot, = plt.plot(_t, _dist_x)
dist_plot.set_label('Distancia')

plt.title('Plots')
plt.xlabel('Tempo')
plt.grid(True)
plt.legend()
plt.show()
