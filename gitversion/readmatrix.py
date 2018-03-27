import numpy as np
import matplotlib.pyplot as plt
import os
import datetime
filename = '/home/estudiante/Documentos/Python/Matrix/20100101_CCA-UNAM_matrix.txt'
f = open(filename, 'r')
print f.readline()
print f.readline()
print f.readline()
print f.readline()
print f.readline()
z=np.array(f.readline().split()[1:],dtype=float)
tarr=np.array(f.readline().split()[1:],dtype=float)
allprf= np.genfromtxt(filename,skip_header=7)
print len(tarr)
print len(z)
levels=100
plt.contourf(tarr,z,allprf,levels)
plt.colorbar()
print 'hola'
plt.show()
