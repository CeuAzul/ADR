from ADR.Analysis.Performance.Takeoff import Takeoff
from ADR.Components.Plane import Plane
from ADR.Components.Aerodynamic_components.Airfoil import Airfoil
from matplotlib import pyplot as plt

wing1_CM_ca = -0.32
wing2_CM_ca = -0.32
hs_CM_ca = 0.092

plane_data = {
    "plane_type": 'monoplane',

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

    "static_thrust": 27,
    "linear_decay_coefficient": 0.875,

    "cg_x": -0.0725,
    "cg_z": -0.1,

    "tpr_x": -0.1225,
    "tpr_z": -0.2,

    "Iyy_TPR": 0.114,
    "CD_tp": 0.02,
    "CD_fus": 0.02,
    "u_k": 0.05
}

takeoff_parameters = {
    "rho_air": 1.15, # Densidade do ar [kg/m^3]
    "dist_max": 60, # Distancia maxima de decolagem pelo regulamento [m]
    "offset_pilot": 5 # Distancia antes do fim da pista em que o piloto aciona o profundor [m]
}

# Instantiate plane object using plane_data
plane = Plane(plane_data)

takeoff_analysis = Takeoff(plane, takeoff_parameters)
takeoff_analysis.calculate_mtow()
mtow = takeoff_analysis.mtow
print('Final MTOW is {}'.format(mtow))

fig1, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3)

ax1.plot(takeoff_analysis.mass_dict[mtow]['N'], label='Normal')
ax1.plot(takeoff_analysis.mass_dict[mtow]['L'], label='Lift')
ax1.plot(takeoff_analysis.mass_dict[mtow]['L_w'], label='Lift Wing')
ax1.plot(takeoff_analysis.mass_dict[mtow]['L_hs'], label='Lift HS')
ax1.grid()
ax1.legend()

ax2.plot(takeoff_analysis.mass_dict[mtow]['D'], label='Drag')
ax2.plot(takeoff_analysis.mass_dict[mtow]['D_w'], label='Drag Wing')
ax2.plot(takeoff_analysis.mass_dict[mtow]['D_hs'], label='Drag HS')
ax2.grid()
ax2.legend()

ax3.plot(takeoff_analysis.mass_dict[mtow]['M'], label='Moment')
ax3.plot(takeoff_analysis.mass_dict[mtow]['M_w'], label='Moment Wing')
ax3.plot(takeoff_analysis.mass_dict[mtow]['M_hs'], label='Moment HS')
ax3.grid()
ax3.legend()

ax4.plot(takeoff_analysis.mass_dict[mtow]['dTheta'], label='dTheta')
ax4.grid()
ax4.legend()

ax5.plot(takeoff_analysis.mass_dict[mtow]['incidence_hs'], label='HS incidence')
ax5.plot(takeoff_analysis.mass_dict[mtow]['theta'], label='Theta')
ax5.grid()
ax5.legend()

ax6.plot(takeoff_analysis.mass_dict[mtow]['dist_x'], label='Distance')
ax6.plot(takeoff_analysis.mass_dict[mtow]['V_x'], label='Velocity')
ax6.grid()
ax6.legend()

plt.show()