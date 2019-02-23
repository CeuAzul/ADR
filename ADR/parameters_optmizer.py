# Generate dictionary with plane and takeoff data
# Ideally you should give all data (like on
# this example). If you don't use some of it, just give
# dummy data (zeros or anything).

def enter_parameters(bounds):
    wing_span = 1 + 1*bounds[0]
    wing_chord = 0.15 + 0.35*bounds[1]
    hs_span = 0.3 + 0.3*bounds[2]
    hs_chord = 0.05 + 0.1*bounds[3]

    motor_x = 0.2
    hs_x = -(3.68 - wing_span - motor_x - hs_chord)

    total_dimension = wing_span + motor_x + hs_chord - hs_x

    print()
    print('---------------------------------------')
    print('Wing span: {}'.format(wing_span))
    print('Wing chord: {}'.format(wing_chord))
    print('HS span: {}'.format(hs_span))
    print('HS chord: {}'.format(hs_chord))
    print('HS_x: {}'.format(hs_x))
    print('Total dimensions is: {}'.format(total_dimension))
    print()


    airplane_data = [wing_span, wing_chord, hs_span, hs_chord, motor_x, hs_x]
    return airplane_data

def plane_data(data):

    plane_data = {
        "plane_type": 'monoplane',

        "wing1_x": 0,
        "wing1_y": 0,
        "wing1_z": 0,
        "wing1_clmax_airfoil": 2.2,
        "wing1_airfoil1_name": "s1223",
        "wing1_airfoil2_name": "s1223",
        "wing1_airfoil3_name": "s1223",
        "wing1_span1": data[0]/4,
        "wing1_span2": data[0]/4,
        "wing1_chord1": data[1],
        "wing1_chord2": data[1],
        "wing1_chord3": data[1],
        "wing1_twist1": 0,
        "wing1_twist2": 0,
        "wing1_twist3": 0,
        "wing1_incidence": 0,

        "wing2_x": 0,
        "wing2_y": 0,
        "wing2_z": 0.3,
        "wing2_clmax_airfoil": 2.2,
        "wing2_airfoil1_name": "s1223",
        "wing2_airfoil2_name": "s1223",
        "wing2_airfoil3_name": "s1223",
        "wing2_span1": data[0]/4,
        "wing2_span2": data[0]/4,
        "wing2_chord1": data[1],
        "wing2_chord2": data[1],
        "wing2_chord3": data[1],
        "wing2_twist1": 0,
        "wing2_twist2": 0,
        "wing2_twist3": 0,
        "wing2_incidence": 0,

        "hs_x": data[5],
        "hs_y": 0,
        "hs_z": 0,
        "hs_clmax_airfoil": 2.2,
        "hs_airfoil1_name": "s1223",
        "hs_airfoil2_name": "s1223",
        "hs_airfoil3_name": "s1223",
        "hs_span1": data[2]/4,
        "hs_span2": data[2]/4,
        "hs_chord1": data[3],
        "hs_chord2": data[3],
        "hs_chord3": data[3],
        "hs_twist1": 0,
        "hs_twist2": 0,
        "hs_twist3": 0,
        "hs_incidence": 0,


        "vs_x": -0.7,
        "vs_y": 0,
        "vs_z": 0,
        "vs_clmax_airfoil": 2.2,
        "vs_airfoil1_name": "s1223",
        "vs_airfoil2_name": "s1223",
        "vs_airfoil3_name": "s1223",
        "vs_span1": 0.1,
        "vs_span2": 0.1,
        "vs_chord1": 0.2,
        "vs_chord2": 0.2,
        "vs_chord3": 0.1,
        "vs_twist1": 0,
        "vs_twist2": 0,
        "vs_twist3": 0,
        "vs_incidence": 0,

        "motor_x": data[4],
        "motor_z": 0,
        "static_thrust": 45,
        "linear_decay_coefficient": 0.875,

        "cg_x": - data[1]/4 - 0.01,
        "cg_z": -0.1,

        "tpr_x": - data[1]/4 - 0.01 - 0.1,
        "tpr_z": -0.2,

        "Iyy_TPR": 0.2,
        "CD_tp": 0.02,
        "CD_fus": 0.02,
        "u_k": 0.05
    }

    return plane_data

def performance_data():

    takeoff_parameters = {
        "rho_air": 1.225, # Densidade do ar [kg/m^3]
        "dist_max": 60, # Distancia maxima de decolagem pelo regulamento [m]
        "offset_pilot": 5 # Distancia antes do fim da pista em que o piloto aciona o profundor [m]
    }

    return takeoff_parameters