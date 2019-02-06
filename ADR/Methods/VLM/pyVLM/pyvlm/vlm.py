import numpy as np
import matplotlib.pyplot as plt
import ADR

from .panel import Panel
from .mesh_generator import Mesh
from .airfoils import NACA4


class PyVLM(object):
    """
    Given a geometry, angle of attack, upstream velocity and mesh
    chordwise and spanwise densities, applies the VLM theory to
    the defined lifting surface.

    Parameters
    ----------
    V : float
        Upstream flow velocity
    alpha : float
            Angle of attack of the surface
    lead_edge_coord : list (containing arrays)
                      Coordinates of the leading edge points
                      as arrays in a 2D euclidean space
    chord_lengths : list
                    Chord lenghts corresponding to the sections
                    defined by the leading edge coordinates
    n, m : integer
           n - nº of chordwise panels
           m - nº of spanwise panels
    """

    def __init__(self):
        self.Points = []
        self.Panels_points = []
        self.Panels_span = []
        self.Chordwise_panel_positions = []
        self.sections_airfoil = []
        self.n = []
        self.m = []

        self.rho = 1.225

    def reset(self):
        """
        Resets values of the list containing the information of the mesh.
        Use when a different geometry or mesh discretization is needed.
        """

        self.Points = []
        self.Panels_points = []
        self.Panels_span = []
        self.Chordwise_panel_positions = []
        self.sections_airfoil = []
        self.n = []
        self.m = []

    def add_geometry(self, lead_edge_coord, chord_lengths, n, m,section_airfoil):
        """
        Allows to add wings, stabilizers, canard wings or any other
        lifting surface to the mesh. These are defined by their chords'
        lengths and leading edges locations. The spanwise and chordwise
        density of the mesh can be controlled through n and m.
        """

        if len(lead_edge_coord) != len(chord_lengths):
            msg = 'Same number of chords and leading edges required'
            raise ValueError(msg)

        # MESH GENERATION

        # When more than two chords -with their respectives leading
        # edges coordinates- are provided, it iterates through the
        # list containing both location and length

        Nle = len(lead_edge_coord)

        for k in range(0, Nle - 1):
            leading_edges = [lead_edge_coord[k],
                             lead_edge_coord[k + 1]]
            chords = [chord_lengths[k],
                      chord_lengths[k + 1]]

            # The mesh is created taking into account the desired
            # mesh density spanwise -"n"- and chordwise -"m"-

            mesh = Mesh(leading_edges, chords, n, m)

            # The points of the mesh, its panels - sets of 4 points
            # orderly arranged -, the position of each panel relative to
            # its local chord and the span of each panel are calculated

            Points_ = mesh.points()
            Panels_points_ = mesh.panels()
            Panels_span_ = mesh.panels_span()
            Chordwise_panel_positions_ = mesh.panel_chord_positions()

            self.Points.extend(Points_)
            self.Panels_points.extend(Panels_points_)
            self.Panels_span.extend(Panels_span_)
            self.Chordwise_panel_positions.extend(Chordwise_panel_positions_)
            temp = np.ones(len(Chordwise_panel_positions_))*section_airfoil
            self.sections_airfoil.extend(temp)
            self.n.append(n)
            self.m.append(m) 

    def check_mesh(self):
        """
        Prints the points of the mesh, the disposition of each panel and
        plots them for visual check.
        """

        Points = self.Points
        Panels = self.Panels_points
        Panels_span = self.Panels_span
        Panels_chordwise_pos = self.Chordwise_panel_positions

        # Check for coincident points
        N = len(Points)
        for i in range(0, N):
            count = 0
            for j in range(0, N):
                if(((Points[j] == Points[i]).all()) is True):
                    count += 1
                    if(count > 1):
                        msg = "Two points of the mesh coincide"
                        raise ValueError(msg)

        # Check for incorrectly defined panels
        N = len(Panels)
        for i in range(0, N):
            P1, P2, P3, P4 = Panels[i][:]

            P1P2 = P2 - P1
            P1P3 = P3 - P1
            P1P4 = P4 - P1
            P3P4 = P4 - P3

            i_inf = np.array([1, 0])

            if np.cross(P1P2, i_inf) != 0:
                msg = 'P1P2 segment not aligned with OX'
                raise ValueError(msg)

            if np.cross(P1P2, P3P4) != 0:
                msg = 'Panel incorrectly defined, P1P2 and P3P4 not parallel'
                raise ValueError(msg)

            if np.sign(np.cross(P1P2, P1P3)) != np.sign(np.cross(P1P3, P1P4)):
                msg = 'Points not in a clockwise/counterclockwise fashion'
                raise ValueError(msg)

        # PRINTING AND PLOTTING
        # print('\n Point |    Coordinates ')
        # print('------------------------')
        # for i in range(0, len(Points)):
        #     print('  %2s   |' % i, np.round(Points[i], 2))

        print('\nPanel| Chrd% |  Span |  Points coordinates')
        print('------------------------------------------------')
        for i in range(0, len(Panels)):
            print(' %3s | %5.2f | %5.3f | '
                  % (i, 100*Panels_chordwise_pos[i], Panels_span[i]),
                  np.round(Panels[i][0], 2), np.round(Panels[i][1], 2),
                  np.round(Panels[i][2], 2), np.round(Panels[i][3], 2))

        plt.style.use('ggplot')
        plt.xlim(-5, 15), plt.ylim(-10, 10)
        for i in range(0, len(Points)):
            P = Points[i]
            plt.plot(P[0], P[1], 'ro')
        plt.show()

    def vlm(self, V, alpha, print_output=False):
        """
        For a given set of panels (defined by its 4 points) and their
        chordwise position (referred to the local chord), both presented
        as lists, applies the VLM theory:

            1. Calculates the induced velocity produced by all the
               associated horseshoe vortices of strength=1 on each panel,
               calculated on its control point where the boundary condition
               will be imposed.
            2. Computes the circulation by solving the linear equation.
            3. Calculates the aerodynamic forces.
        """

        Panels = self.Panels_points
        Panels_span = self.Panels_span
        Panels_chordwise_position = self.Chordwise_panel_positions
        sections_airfoil = self.sections_airfoil

        rho = self.rho

        # 1. BOUNDARY CONDITION
        # To impose the boundary condition we must calculate the normal
        # components of (a) induced velocity "Wn" by horshoe vortices of
        # strength=1 and (b) upstream normal velocity "Vinf_n"

        #     1.a INDUCED VELOCITIES
        #     - "Wn", normal component of the total induced velocity by the
        #       horshoe vortices, stored in the matrix "A" where the element
        #       Aij is the velocity induced by the horshoe vortex in panel j
        #       on the control point of panel i
        #     - also the induced velocity by *only* trailing vortices "Wi" is
        #       calculated and stored in the array "W_induced", where the
        #       element Winduced[i] is the velocity induced by all the trailing
        #       vortices on the panel i

        N = len(Panels)
        A = np.zeros(shape=(N, N))  # Aerodynamic Influence Coefficient matrix
        W_induced = np.zeros(N)  # induced velocity by trailing vortices
        alpha_induced = np.zeros(N)  # induces angle of attack
        S = np.zeros(N)  # induced velocity by trailing vortices

        for i in range(0, N):
            P1, P2, P3, P4 = Panels[i][:]
            panel_pivot = Panel(P1, P2, P3, P4)
            s = panel_pivot.area()
            S[i] = s
            CP = panel_pivot.control_point()

            Wi_ = 0
            for j in range(0, N):
                PP1, PP2, PP3, PP4 = Panels[j][:]
                panel = Panel(PP1, PP2, PP3, PP4)
                Wn, Wi = panel.induced_velocity(CP)
                A[i, j] = Wn
                Wi_ += Wi

            W_induced[i] = Wi_
            alpha_induced[i] = np.arctan(-W_induced[i]/V)  # rad

        #     1.b UPSTREAM NORMAL VELOCITY
        #     that will depend on the angle of attach -"alpha"- and the
        #     camber gradient at each panel's position within the local
        #     chord

        Vinf_n = np.zeros(shape=N)

        airfoil = NACA4()
        #print(Panels_chordwise_position)
        #print(sections_airfoil)
        for i in range(0, N):
            position = Panels_chordwise_position[i]
            if sections_airfoil[i] == 0:
                Vinf_n[i] = alpha - airfoil.camber_gradient(position)
            else:
                Vinf_n[i] = alpha - airfoil.camber_gradient(position,1,0.8,10)
            Vinf_n[i] *= -V

        # 2. CIRCULATION (Γ or gamma)
        # by solving the linear equation (AX = Y) where X = gamma
        # and Y = Vinf_n

        gamma = np.linalg.solve(A, Vinf_n)

        # 3. AERODYNAMIC FORCES
        l = np.zeros(N)
        d = np.zeros(N)
        mm = np.zeros(N)
        centro_x = np.zeros(N)
        centro_y = np.zeros(N)
        cl_chord = np.zeros(self.n)
        for i in range(0, N):
            l[i] = V * rho * gamma[i] * Panels_span[i]
            d[i] = rho * gamma[i]*gamma[i] * Panels_span[i] * abs(W_induced[i]) #one more term of gamma[i] added, seems to work fine
            i_Panel = Panels[i]
            xj = np.zeros(4)
            yj = np.zeros(4)
            for j in range(0,4):
                xj[j] = i_Panel[j][0]
                yj[j] = i_Panel[j][1]
            ordem_y=np.argsort(yj)
            ordem_x=np.argsort(-xj)
            #print(ordem_y,yj)
            #print(ordem_x,xj)
            x_novo_ponto = np.zeros(2)
            y_novo_ponto = np.zeros(2)
            x_novo_ponto[0] = (xj[ordem_y[0]]+xj[ordem_y[1]])/2
            x_novo_ponto[1] = (xj[ordem_y[2]]+xj[ordem_y[3]])/2
            y_novo_ponto[0] = (yj[ordem_y[0]]+yj[ordem_y[1]])/2
            y_novo_ponto[1] = (yj[ordem_y[2]]+yj[ordem_y[3]])/2
            cp_x_novo = (x_novo_ponto[0]+x_novo_ponto[1]+xj[ordem_x[0]]+xj[ordem_x[1]])/4
            cp_y_novo = (y_novo_ponto[0]+y_novo_ponto[1]+yj[ordem_x[0]]+yj[ordem_x[1]])/4
            #plt.plot(xj,yj,'x')
            #plt.plot(cp_x_novo,cp_y_novo,'+')
            #plt.xticks(np.arange(min(xj), max(xj)+0.01, 0.01))
            centro_x[i] = sum(xj)/4
            centro_y[i] = sum(yj)/4
            mm[i] = -l[i]*centro_x[i]
        clc = []
        cdc = []
        ys = []
        temp = 0
        for k in range(0,len(self.n)):
            l_chord = np.zeros(self.m[k])
            d_chord = np.zeros(self.m[k])
            S_chord = np.zeros(self.m[k])
            cl_chord = np.zeros(self.m[k])
            cd_chord = np.zeros(self.m[k])
            y_chord = np.zeros(self.m[k])
            d_chord_visc = np.zeros(self.m[k])

            for i in range(0, self.m[k]):
                for j in range(0, self.n[k]):
                    a = temp+i+j*self.m[k]
#                    print(a,l[a],len(l),self.m,self.n)
                    l_chord[i] = l_chord[i] + l[a]
                    d_chord[i] = d_chord[i] + d[a]
                    S_chord[i] = S_chord[i] + S[a]
                cl_chord[i] = (2*l_chord[i])/(V**2*S_chord[i]*rho)
                cd_chord[i] = (2 * d_chord[i]) / (V ** 2 * S_chord[i] * rho)
                y_chord[i] = centro_y[temp+i]
            clc.extend(cl_chord)
            cdc.extend(cd_chord)
            ys.extend(y_chord)
            temp = self.n[k]*self.m[k]+temp
        ys, clc = zip(*sorted(zip(ys, clc)))
        package_filepath = ADR.__file__.replace('__init__.py', '')
        airfoil_aerodynamic_data_filename = "T1_Re0.100_M0.00_N9.0.txt"
        airfoil_aerodynamic_data_filepath = package_filepath + 'World/Profiles/AerodynamicData/' + airfoil_aerodynamic_data_filename
        Data = np.loadtxt(airfoil_aerodynamic_data_filepath) #precisa mudar
        cl_foil = []
        cd_foil = []
        alpha_foil = []
        for i in range(0, len(Data)):
            alpha_foil.append(Data[i, 0])
            cl_foil.append(Data[i, 1])
            cd_foil.append(Data[i, 2])
        cd_foil_alpha = np.interp(clc, cl_foil, cd_foil)
        cd_chord_cor = np.add(cdc, cd_foil_alpha)
        d_chord_visc = []
        for k in range(0, len(self.n)):
            print(k)
            for i in range(0, self.m[k]):
                d_chord_visc.append(cd_chord_cor[i]*S_chord[i]*rho*V**2/(2))
        #print(cl_chord)
        #print(cd_chord)
        #print(cl_foil)
        #print(cd_foil)
        #print(cd_foil_alpha)
        #print(cd_chord_cor)
        #print(alpha*180/3.14)
#        print(ys,clc)
        L = sum(l)
        D = sum(d)
        D_visc = sum(d_chord_visc)
        M = sum(mm) #Pitch moment calculator MIGUÉ
        A = []
        A = sum(S)
        if (print_output is True):
            print('\nPanel|  V∞_n |   Wi   |  α_i  |   Γ   |    l   |   d  |')
            print('-------------------------------------------------------')
            for i in range(0, len(Panels)):
                print(' %3s | %5.2f | %6.2f | %5.2f | %5.2f |%7.1f | %4.2f |'
                      % (i, Vinf_n[i], W_induced[i],
                         np.rad2deg(alpha_induced[i]), gamma[i], l[i], d[i]))
            print('\n L = %6.3f     D = %6.3f \n' % (L, D))

        airfoil_aerodynamic_data_filename = 'T1-12_0 m_s-VLM2-1_0kg-x0_0m_flap.txt'
        airfoil_aerodynamic_data_filepath = package_filepath + 'World/Profiles/AerodynamicData/' + airfoil_aerodynamic_data_filename
        Data = np.loadtxt(airfoil_aerodynamic_data_filepath)  # precisa mudar
        CL_plane = []
        CD_plane = []
        for i in range(0, len(Data)):
            CL_plane.append(Data[i, 2])
            CD_plane.append(Data[i, 5])


        CL = 2*L/(rho*A*V**2)
        CD = 2*D/(rho*A*V**2)
        CD_visc = 2*D_visc/(rho*A*V**2)
        #plt.plot(CD,CL)
        plt.plot(CD, CL, '+')
        plt.plot(CD_visc, CL, 'x')
        plt.plot(CD_plane,CL_plane)
        return L, D, M, ys, clc
