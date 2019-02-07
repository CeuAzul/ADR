from ADR.Analysis.Performance.Takeoff import get_MTOW
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

takeoff_parameters = {
    "rho_air": 1.225, # Densidade do ar [kg/m^3]
    "I_airp": 0.02, # Momento de Inercia da aeronave []
    "C_D_tp": 0.02, # Coeficiente de arrasto do trem de pouso
    "C_D_fus": 0.02, # Coeficiente de arrasto da fuselagem
    "f_f": 0.01, # Coeficiente de atrito dinamico da roda frontal
    "f_r": 0.01, # Coeficiente de atrito dinamico da roda traseira
    "d_L_w_cg": 0.1, # Distancia do CA da Asa ao CG
    "d_L_hs_cg": 0.9, # Distancia do CA do profundor ao CG
    "dist_max": 50, # Distancia maxima de decolagem pelo regulamento [m]
    "offset_pilot": 5 # Distancia antes do fim da pista em que o piloto aciona o profundor [m]
}

# Instantiate plane object using plane_data
plane = Plane(plane_data)

mtow = get_MTOW(plane, takeoff_parameters)
print('Final MTOW is {}'.format(mtow))