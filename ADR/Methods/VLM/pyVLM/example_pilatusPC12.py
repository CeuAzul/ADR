"""
    This example shows how to use the PyVLM class in order
    to generate the wing planform of a Pilatus PC12 airplane.

    After defining the flight conditions (airspeed and AOA),
    the geometry will be characterised using the following
    nomenclature:

    Y  ^  D +--+
       |   /    \
       |  /      \
       | /        \
       |/          \
     C +------------+
       +-------------------->
     B +------------+        X
        \          /
         \        /
          \      /
           \    /
          A +--+
"""

import numpy as np
import matplotlib.pyplot as plt

from pyvlm.vlm import PyVLM


pilatusPC12 = PyVLM()

# GEOMETRY DEFINITION #
# Parameters
c = 0.3  # root chord length
b = 3  # panel span length
n = 2  # number of panels (chordwise)
m = 5   # number of panels (spanwise) (For each wing)

# Left wing
A = np.array([-0.5, -b/2])
B = np.array([0, -0.5])
leading_edges_coord_lw = [A, B]
chord_lengths_lw = [c, c]
S_left = (chord_lengths_lw[0] + chord_lengths_lw[1])*(B[1]-A[1])/2
# Right wing
C = np.array([0, 0.5])
D = np.array([-0.5, b/2])
leading_edges_coord_rw = [C, D]
chord_lengths_rw = [c, c]
S_right = (chord_lengths_rw[0] + chord_lengths_lw[1])*(D[1]-C[1])/2
#Center (Flap)
E = np.array([0, -0.5])
F = np.array([0, 0.5])
leading_edges_coord_ct = [E, F]
chord_lengths_ct = [c, c]
S_center = (chord_lengths_ct[0] + chord_lengths_ct[1])*(F[1]-E[1])/2

S = S_left+S_right+S_center
## Horizontal stabilizer
A = np.array([1, 0.3])
B = np.array([1, 0])
C = np.array([1, -0.3])
leading_edges_coord_hs = [A, B, C]
chord_lengths_hs = [0.2, 0.2, 0.2]

pilatusPC12.add_geometry(leading_edges_coord_lw, chord_lengths_lw, n, m,0)
pilatusPC12.add_geometry(leading_edges_coord_rw, chord_lengths_rw, n, m,0)
pilatusPC12.add_geometry(leading_edges_coord_ct, chord_lengths_ct, n, m,1)
#pilatusPC12.add_geometry(leading_edges_coord_hs, chord_lengths_hs, 4, 4)

pilatusPC12.check_mesh()

# SIMULATION
# Flight condition parameters
V = 12
rho = 1.225 #Value applied internally in the code
alpha_min =0
alpha_max = 15
alpha_length = alpha_max-alpha_min+1
alpha = np.linspace(alpha_min,alpha_max,alpha_length)
alpha_rad = alpha*np.pi/180
cl = []
cdi = []
cm = []
cm2 = []
Xcp = []
clc_max = 1.2
q = rho*(V**2)/2
for i in range(alpha_length):
  L, D_i, M, y, clc = pilatusPC12.vlm(V, alpha_rad[i]) #Leading edge moment
  
  cp = -M/(L*c)
  if max(clc)>clc_max:
      break
  Xcp.append(cp*c)
  cdi.append(D_i/(q*S))
  cl.append(L/(q*S))
  cm.append(-(cp-0.25)*L/(q*S))
  cm2.append(M/(q*S*c))

#Data = np.loadtxt( "JP_10.txt")
#Data = np.loadtxt( "Henrique_0_0.txt")
Data = np.loadtxt( "Wing_Graph_0.txt")
#Alpha_Henrique = []
#CL_Henrique = []
#CDi_Henrique = []
#CM_Henrique = []
#XCp_Henrique = []
X_wing=[]
CL_wing=[]
for i in range(0,len(Data)):
  #Alpha_Henrique.append(Data[i,0])
  #CL_Henrique.append(Data[i,2])
  #CDi_Henrique.append(Data[i,3])
  #CM_Henrique.append(-Data[i,2]*(Data[i,12]-0.25*0.3)/0.3)
  #CM_Henrique.append(Data[i,8])
  #XCp_Henrique.append(Data[i,12])
    X_wing.append(Data[i,0])
    CL_wing.append(Data[i,1])

#print(y)
#print(clc)
#plt.plot(X_wing,CL_wing)
#plt.plot(y,clc)
    
#
#plt.subplot(2,2,1)
#plt.plot(alpha,cl,label='CL VLM')
#plt.plot(Alpha_Henrique,CL_Henrique,label='CL Henrique')
#plt.grid()
#plt.legend(loc='upper left')
#
#plt.subplot(2,2,2)
#plt.plot(alpha,cdi,label='CDi VLM')
#plt.plot(Alpha_Henrique,CDi_Henrique,label='CDi Henrique')
#plt.grid()
#plt.legend(loc='upper left')
#
#plt.subplot(2,2,3)
#plt.plot(alpha,cm,label='Cm VLM (25%C)')
#plt.plot(Alpha_Henrique,CM_Henrique,label='Cm Henrique')
#plt.grid()
#plt.legend(loc='lower left')
#
#plt.subplot(2,2,4)
#plt.plot(alpha,Xcp,label='Xcp VLM')
#plt.plot(Alpha_Henrique,XCp_Henrique,label='Xcp Henrique')
#plt.grid()
#plt.legend(loc='lower left')

plt.show()

