from funcao_dimensao_asa import dimensao_superficie
from funcao_transferencia_avl_codigo import read1
import subprocess
import os
import math
import time
import numpy as np
from matplotlib import pyplot as plt

file = 'testerafa.avl'
passo = 1
alpha = list(np.arange(-20,20+passo,passo))

cl = []
cd = []
cm=[]

dimensao_superficie(file,'s1223.dat','s1223.dat','s1223.dat','wing',0,0,0.7,1.4,0,0.4,0.4,0.4,0,0,0,0)

start = time.time()
for a1 in alpha:
    os.remove('export.txt')
    comm_string = 'load {}\n oper\n a\n a\n {}\n x\n ft\nexport.txt\n o\n'.format(file,a1)
    Process=subprocess.Popen(['avl.37.exe'], stdin=subprocess.PIPE, shell = True)
    Process.communicate(bytes(comm_string,encoding='utf8'))

    cl.append(float(read1('CLtot').strip('\n')))
    cd.append(float(read1('CDtot').strip('\n')))
    cm.append(float(read1('Cmtot').strip('\n')))
    

end = time.time()
print(end-start)

cl_alpha = (cl[-1]-cl[0])/(math.radians(alpha[-1])-math.radians(alpha[0]))
print(cl_alpha)
#plt.plot(alpha,cm)

plt.plot(alpha,cl)
plt.grid()
plt.show()
