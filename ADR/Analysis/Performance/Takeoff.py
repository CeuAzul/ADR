import math
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os

from ADR.Methods.FundamentalEquations import lift, drag, moment
from ADR.Components.Plane import Plane

plane_data = {
    "wing_x": 1,
    "wing_y": 2,
    "wing_z": 3,
    "wing_airfoil1": "s1223",
    "wing_airfoil2": "s1223",
    "wing_span1": 0.8,
    "wing_span2": 0.4,
    "wing_chord1": 0.45,
    "wing_chord2": 0.35,
    "wing_chord3": 0.20,
    "wing_twist1": 0,
    "wing_twist2": 0,
    "wing_twist3": -5,
    "wing_incidence": 3,

    "hs_x": 1,
    "hs_y": 2,
    "hs_z": 3,
    "hs_airfoil1": "s1223",
    "hs_airfoil2": "s1223",
    "hs_span1": 0.2,
    "hs_span2": 0.1,
    "hs_chord1": 0.15,
    "hs_chord2": 0.15,
    "hs_chord3": 0.10,
    "hs_twist1": 0,
    "hs_twist2": 0,
    "hs_twist3": -5,
    "hs_incidence": 0,

    "vs_x": 1,
    "vs_y": 2,
    "vs_z": 3,
    "vs_airfoil1": "s1223",
    "vs_airfoil2": "s1223",
    "vs_span1": 0.1,
    "vs_span2": 0.1,
    "vs_chord1": 0.2,
    "vs_chord2": 0.2,
    "vs_chord3": 0.1,
    "vs_twist1": 0,
    "vs_twist2": 0,
    "vs_twist3": 0,
    "vs_incidence": 0,

    "static_thrust": 45,
    "linear_decay_coefficient": 1.28
}

plane = Plane(plane_data)

theta_airplane_deg = 0 # Angulo do aviao com a pista [°]
theta_airplane_rad = math.radians(theta_airplane_deg) # Angulo do aviao com a pista [rad]
rho_air = 1.225 # Densidade do ar [kg/m^3]
m = 20 # Massa total do aviao [kg]
g = 9.81 # Constante gravitacional [m/s^2]
I_airp = 0.2 # Momento de Inercia da aeronave []

V_x = 0 # Velocidade inicial do aviao no eixo X [m/s]
V_y = 0 # Velocidade inicial do aviao no eixo Y [m/s]

C_D_tp = 0.02 # Coeficiente de arrasto do trem de pouso
C_D_fus = 0.02 # Coeficiente de arrasto da fuselagem

S_w = plane.wing.area

f_f = 0.01 # Coeficiente de atrito dinamico da roda frontal
f_r = 0.01 # Coeficiente de atrito dinamico da roda traseira

d_L_w_cg = 0.1 # Distancia da resultante das forças na Asa ao CG
d_L_hs_cg = 0.9 # Distancia da resultante das forças no profundor ao CG

_t = []
_V_x = []
_dist_x = []
_N = []

dist_x = 0 # Distancia percorrida em X [m]
N = 0.1 # Força normal [N]
t = 0 # Tempo [s]
dt = 0.001 # Incremento discreto de tempo [s]

while(N>0):
    alpha_w = 0
    alpha_hs = 0
    alpha_theta_w = theta_airplane_deg + alpha_w
    alpha_theta_hs = theta_airplane_deg + alpha_hs

    E = plane.motor.thrust(V_x)

    t = t + dt
    L_w = plane.wing.lift(rho_air, V_x, alpha_theta_w)
    L_hs = plane.hs.lift(rho_air, V_x, alpha_theta_hs)
    E_y = E*math.sin(theta_airplane_rad)
    W = m*g

    N = W + L_hs - L_w - E_y

    E_x = E*math.cos(theta_airplane_rad)
    D_w = plane.wing.drag(rho_air, V_x, alpha_theta_w)
    D_hs = plane.hs.drag(rho_air, V_x, alpha_theta_hs)
    D_tp = drag(rho_air, V_x, S_w, C_D_tp)
    D_fus = drag(rho_air, V_x, S_w, C_D_fus)
    F_at_f = f_f*N
    F_at_r = f_r*N

    dV_x = ((E_x - D_w - D_hs - D_tp - D_fus - F_at_f - F_at_r)/m) * dt
    V_x = V_x + dV_x
    dist_x = dist_x + V_x * dt

    _t.append(t)
    _V_x.append(V_x)
    _N.append(N)
    _dist_x.append(dist_x)

    M_w = plane.wing.moment(rho_air, V_x, alpha_theta_w)
    M_hs = plane.hs.moment(rho_air, V_x, alpha_theta_hs)
    dTheta = (((M_hs - M_w + L_w*d_L_w_cg + L_hs*d_L_hs_cg)/I_airp)*dt)*dt
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
