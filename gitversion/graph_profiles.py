#!/usr/bin/python/env
# -*- coding: utf8 -*-
import numpy as np
import matplotlib.pyplot as plt
import math
import os,glob
import sys 
carpeta='/home/D1_CEILO/UNAM/PRCL/Results/Perfiles/'
outputdir='/home/D1_CEILO/UNAM/PRCL/Results/Plots/article/'
os.chdir(carpeta)
flist=glob.glob(carpeta+"*.txt")
filename=flist[0]
file2=flist[1]
l=700
with open(filename,'r') as f: 
	for i in range(6):
		f.readline()
        allprf=np.genfromtxt(filename,skip_header=8)
        z=np.array(f.readline().split()[1:],dtype=float)
        tarr=np.array(f.readline().split()[1:],dtype=float)
sinfiltro=np.genfromtxt(file2,skip_header=8)
lista=[3.,6.,9.,12.,15.,18.,21.]
z=range(100,5000,10)
print len(lista)
plt.figure(figsize=(12,8))
for i in lista: 
	index,=np.where(tarr==i)
	vec=allprf[:,int(index)]
	vec2=sinfiltro[:,int(index)]
	vec2=vec2[10:]
	vec=vec[10:]
	print len(vec)
	vec=vec+l
	vec2=vec2+l
	if i == 21.:
		break
	plt.plot(vec,z,color='b',linestyle='-')
	plt.plot(vec2,z,color='k',linestyle='-')
	l=l+700
plt.plot(vec,z,color='b',linestyle='-',label='Cloud')
plt.plot(vec2,z,color='k',linestyle='-',label='No filter')
plt.xlabel('Time (h) UT-6',fontsize=14)
plt.xticks(np.linspace(700, 4900, 7),['3','6','9','12','15','18','21'])

plt.xlim([550,(4900+700)])
plt.ylabel('Height [m.a.g.l.]',fontsize=14)
plt.title( u'Backscattering profiles',fontsize=16)
plt.legend(loc='upper right',fontsize=12,title='Filter')
plt.grid()
plt.savefig( outputdir +  'perfl_comparacion'+".png")
	#plt.show()
