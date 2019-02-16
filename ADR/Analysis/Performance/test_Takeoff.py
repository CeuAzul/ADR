from ADR.Analysis.Performance.Takeoff import Takeoff
from ADR.Components.Plane import Plane
from ADR.Components.Aerodynamic_components.Airfoil import Airfoil

wing1_CM_ca = -0.32
wing2_CM_ca = -0.32
hs_CM_ca = 0.092

plane_type = 'monoplane'

plane_data = {
    "wing1_x": 0,
    "wing1_y": 0,
    "wing1_z": 0,
    "wing1_airfoil1_name": "s1223",
    "wing1_airfoil2_name": "s1223",
    "wing1_span1": 0.45,
    "wing1_span2": 0.45,
    "wing1_chord1": 0.25,
    "wing1_chord2": 0.25,
    "wing1_chord3": 0.25,
    "wing1_twist1": 0,
    "wing1_twist2": 0,
    "wing1_twist3": 0,
    "wing1_incidence": 0,
    "wing1_CM_ca": wing1_CM_ca,

    "wing2_x": 0,
    "wing2_y": 0,
    "wing2_z": 0.3,
    "wing2_airfoil1_name": "s1223",
    "wing2_airfoil2_name": "s1223",
    "wing2_span1": 0.45,
    "wing2_span2": 0.45,
    "wing2_chord1": 0.25,
    "wing2_chord2": 0.25,
    "wing2_chord3": 0.25,
    "wing2_twist1": 0,
    "wing2_twist2": 0,
    "wing2_twist3": 0,
    "wing2_incidence": 0,
    "wing2_CM_ca": wing2_CM_ca,

    "hs_x": -0.7,
    "hs_y": 0,
    "hs_z": 0,
    "hs_airfoil1_name": "s1223",
    "hs_airfoil2_name": "s1223",
    "hs_span1": 0.12,
    "hs_span2": 0.12,
    "hs_chord1": 0.2,
    "hs_chord2": 0.15,
    "hs_chord3": 0.10,
    "hs_twist1": 0,
    "hs_twist2": 0,
    "hs_twist3": 0,
    "hs_incidence": 0,
    "hs_CM_ca": hs_CM_ca,


    "vs_x": -0.7,
    "vs_y": 0,
    "vs_z": 0,
    "vs_airfoil1_name": "s1223",
    "vs_airfoil2_name": "s1223",
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
    "I_airp": 2.0, # Momento de Inercia da aeronave []
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

takeoff_analysis = Takeoff(plane, takeoff_parameters)
takeoff_analysis.calculate_mtow()
mtow = takeoff_analysis.mtow
print('Final MTOW is {}'.format(mtow))
