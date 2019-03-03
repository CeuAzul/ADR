from numpy import interp

def generate_forced_parameters(genes):

    genes_bounds = [0,1]

    wing_span_bounds     =   [1.00, 3.00]
    wing_chord_bounds    =   [0.05, 0.80]
    hs_span_bounds       =   [1.00, 3.00]
    hs_chord_bounds      =   [0.05, 0.40]
    wing2_height_bounds  =   [0.35, 1.00]
    hs_z_bounds          =   [0.00, 1.00]
    motor_z_bounds       =   [0.00, 0.50]
    cg_x_bounds          =   [0, 0.1]
    tpr_x_bounds         =   [0, 0.1]

    wing_span            =   interp(genes[0], genes_bounds, wing_span_bounds)
    wing_chord           =   interp(genes[1], genes_bounds, wing_chord_bounds)
    hs_span              =   interp(genes[2], genes_bounds, hs_span_bounds)
    hs_chord             =   interp(genes[3], genes_bounds, hs_chord_bounds)
    wing2_height         =   interp(genes[4], genes_bounds, wing2_height_bounds)
    hs_z                 =   interp(genes[5], genes_bounds, hs_z_bounds)
    motor_z              =   interp(genes[6], genes_bounds, motor_z_bounds)
    cg_x                 =  -interp(genes[7], genes_bounds, cg_x_bounds) - wing_chord/4
    tpr_x                =  -interp(genes[8], genes_bounds, tpr_x_bounds) + cg_x

    motor_x = 0.2
    y_max = max(wing_span, hs_span)
    hs_x = -(3.70 - y_max - motor_x - hs_chord)

    total_dimension = y_max + motor_x + hs_chord - hs_x

    forced_parameters = {
        'wing1_span1' : wing_span/4,
        'wing1_span2' : wing_span/4,
        'wing1_chord1' : wing_chord,
        'wing1_chord2' : wing_chord,
        'wing1_chord3' : wing_chord,

        'wing2_span1' : wing_span/4,
        'wing2_span2' : wing_span/4,
        'wing2_chord1' : wing_chord,
        'wing2_chord2' : wing_chord,
        'wing2_chord3' : wing_chord,

        'hs_span1' : hs_span/4,
        'hs_span2' : hs_span/4,
        'hs_chord1' : hs_chord,
        'hs_chord2' : hs_chord,
        'hs_chord3' : hs_chord,

        'wing2_z' : wing2_height,
        'hs_z' : hs_z,
        'motor_z' : motor_z,
        'cg_x' : cg_x,
        'tpr_x' : tpr_x,

        'motor_x' : motor_x,
        'hs_x' : hs_x,
    }

    print('-----------------------------------------')
    for key, value in forced_parameters.items():
        print('{} : {:.3f}'.format(key, value))
    print('-----------------------------------------')

    return forced_parameters