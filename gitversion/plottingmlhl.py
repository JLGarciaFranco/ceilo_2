#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import numpy as np
import matplotlib
import glob,os
import sys
import csv
import math
from ceilotools import *
#from scipy import stats
print 'hola'
import matplotlib.pyplot as plt
outputdir='/home/D1_CEILO/UNAM/PRCL/Results/Plots/'
mdir='/home/D1_CEILO/UNAM/PRCL/HDB/'
flist=glob.glob(mdir+"*.txt")
run='comparacion'

flist=np.sort(flist)
print flist
labels=['No estandarizada 02/16','Nueva estandarizada (completa) 07/16']
for i,filename in enumerate(flist):
	f=open(filename,'r')
	for j in range(3):
		f.readline()
	tvec=np.array(f.readline().split()[2:],dtype=float)
	
	matrix=np.genfromtxt(filename,skip_header=4)
	averages=np.average(matrix,axis=0, weights=matrix.astype(bool))
	std=np.zeros(len(tvec))
	sterr=np.zeros(len(tvec))
	ravg=runningMeanFast(averages,3)
	for h in range(len(tvec)):
		nuevovec=matrix[h,:]
	#[c for c, e in enumerate(nuevovec) if e != 0]
		nuevovec=np.nonzero(nuevovec)
		nuevovec=np.asarray(nuevovec)
	#print len(nuevovec)
		std[h]=np.std(nuevovec)
		sterr[h]=std[h]/nuevovec.size
	yerr=sterr
	plt.plot(tvec,ravg,label=labels[i])
plt.xlim(0,np.max(tvec))
plt.xticks(range(0,24,4))
plt.xlabel('Time UT-6')
plt.ylim(600,2600)
legend=plt.legend(title='Bases de datos',loc='upper left') #Legend: list, location, Title (in bold)
legend.get_title().set_fontsize('11') #legend 'Title' fontsize
frame = legend.get_frame()
plt.setp(plt.gca().get_legend().get_texts(), fontsize='9') 
frame.set_facecolor('wheat')
frame.set_edgecolor('wheat')
#legend 'list' fontsize
plt.ylabel('Altura [m.s.n.s]')
plt.title('Comparación de bases de datos')
plt.savefig(outputdir +'rmean_'+run+".png")

plt.close()


#plt.xlim(0,np.max(tvec))
#plt.xticks(range(0,24,4))
#plt.xlabel('Time UT-6')
#legend=plt.legend(title='Bases de Datos',loc='lower right') #Legend: list, location, Title (in bold)
#legend.get_title().set_fontsize('11') #legend 'Title' fontsize
#plt.setp(plt.gca().get_legend().get_texts(), fontsize='9') #legend 'list' fontsize
#plt.legend()
#plt.ylabel('Height [m a.g.l.]')
#plt.title( 'Evolucion de MLH')
#plt.savefig( outputdir +  'evoltn_allpnts'+run+".png")
#plt.show()
#plt.close()
#plt.close()
#plt.figure()



