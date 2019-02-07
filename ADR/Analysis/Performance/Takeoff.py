import math

from ADR.Methods.FundamentalEquations import lift, drag, moment


def get_MTOW(plane, takeoff_parameters):

    rho_air = takeoff_parameters.get("rho_air")
    I_airp = takeoff_parameters.get("I_airp")
    C_D_tp = takeoff_parameters.get("C_D_tp")
    C_D_fus = takeoff_parameters.get("C_D_fus")
    f_f = takeoff_parameters.get("f_f")
    f_r = takeoff_parameters.get("f_r")
    d_L_w_cg = takeoff_parameters.get("d_L_w_cg")
    d_L_hs_cg = takeoff_parameters.get("d_L_hs_cg")
    dist_max = takeoff_parameters.get("dist_max")
    offset_pilot = takeoff_parameters.get("offset_pilot")

    theta_airplane_deg = 0 # Angulo do aviao com a pista [°]
    m = 1 # Massa total inicial do aviao [kg]
    g = 9.81 # Constante gravitacional [m/s^2]
    V_x = 0 # Velocidade inicial do aviao no eixo X [m/s]
    V_y = 0 # Velocidade inicial do aviao no eixo Y [m/s]
    S_w = plane.wing.area
    pilot_triggered = False # O piloto acionou o profundor?

    dist_x = 0 # Distancia percorrida em X [m]
    N = 0.1 # Força normal [N]
    t = 0 # Tempo [s]
    dt = 0.01 # Incremento discreto de tempo [s]
    dm = 0.1 #Incremento de massa [kg]

    incidence_w = 0 # Angulo de incidencia da asa [deg]
    incidence_hs = 0 # Angulo de incidencia do profundor [deg]
    incidence_active_hs = 12 # Angulo de incidencia adicionado no profundor ao ser acionado [deg]

    on_ground = True
    takeoff_failed = False

    mtow = 0

    while(not takeoff_failed):
        on_ground = True
        m = m+dm
        while(on_ground and not takeoff_failed):
            alpha_w = theta_airplane_deg + incidence_w
            alpha_hs = theta_airplane_deg + incidence_hs

            E = plane.motor.thrust(V_x)

            t = t + dt

            L_w = plane.wing.lift(rho_air, V_x, alpha_w)
            L_hs = plane.hs.lift(rho_air, V_x, alpha_hs)
            L = L_w - L_hs

            E_y = E*math.sin(math.radians(theta_airplane_deg))
            W = m*g

            N = W - L - E_y

            E_x = E*math.cos(math.radians(theta_airplane_deg))

            D_w = plane.wing.drag(rho_air, V_x, alpha_w)
            D_hs = plane.hs.drag(rho_air, V_x, alpha_hs)
            D_tp = drag(rho_air, V_x, S_w, C_D_tp)
            D_fus = drag(rho_air, V_x, S_w, C_D_fus)
            D = D_w + D_hs + D_tp + D_fus

            F_at_f = f_f*N
            F_at_r = f_r*N
            F_at = F_at_f + F_at_r

            dV_x = ((E_x - D - F_at)/m) * dt
            V_x = V_x + dV_x
            dist_x = dist_x + V_x * dt

            M_w = plane.wing.moment(rho_air, V_x, alpha_w)
            M_hs = plane.hs.moment(rho_air, V_x, alpha_hs)
            dTheta = (((M_hs - M_w + L_w*d_L_w_cg + L_hs*d_L_hs_cg)/I_airp)*dt)*dt

            if (dist_max-dist_x) <= offset_pilot and pilot_triggered == False:
                incidence_hs += incidence_active_hs
                pilot_triggered = True
                alpha_hs = theta_airplane_deg + incidence_hs

            if theta_airplane_deg >= 0:
                theta_airplane_deg = theta_airplane_deg + dTheta

            if dist_x > dist_max:
                takeoff_failed = True
            else:
                takeoff_failed = False
                mtow = m

            if N>0:
                on_ground = True
            else:
                on_ground = False
        print('MTOW now is {}'.format(mtow))

    return mtow
