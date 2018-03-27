#!/usr/bin/python/env
#Version 201505 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import glob,os
import sys
import csv
import math
import datetime
import itertools
from ceilotools import *
from itertools import islice
#Carpeta de destino de los plots 
plotdir= "/home/D1_CEILO/UNAM/PRCL/FDB_10/Plots/"
#Carpeta de destino de los mlh.txt
mlhdir = "/home/D1_CEILO/UNAM/PRCL/FDB_10/MLH/"
#Carpeta de destino de los matrix.txts
matrixdir = "/home/D1_CEILO/UNAM/PRCL/FDB_10/Perfiles/"
#Colorbar maximum color level y ticks range
maxcollevel = 2100
estacion='UNAM'
#Un color cada colorss niveles (Valores sugeridos para que el colorbar tenga continuidad). 
colorss= (maxcollevel-100)/80
tickrange = maxcollevel+400
#Tick every tickt number of levels
tickt = (maxcollevel-100)/4
levels=range(0,maxcollevel,colorss)
# Carpeta de archivos. 
carpeta='/home/D1_CEILO/wolf/'
monthlist=['11','12']
filelist=[]
for i in monthlist:
	newfilelist=glob.glob(carpeta+"2010"+i+"*.txt")
	filelist.extend(newfilelist)
filelist=np.sort(filelist)
print filelist
for filename in filelist:
	flname=filename.split('/')[-1]
	prof=np.genfromtxt(filename,delimiter=',')
	dtime=np.genfromtxt(filename, usecols=(0),dtype=None,delimiter=',')
	dat=dtime[1][0:10]
	year=dat[0:4]
	mes=dat[5:7]
	dia=dat[8:10]
	oldm=np.zeros((770,len(dtime)))
	for j,perfil in enumerate(prof):
		oldm[:,j]=perfil[1:]
		#print oldm[:,j]
	base=10.0/60.0 
	tvec=frange(0,24,base)
	rtvec=np.zeros(len(dtime))
	zmax=5000
	for i,tt in enumerate(dtime):
		dt=datetime.datetime.strptime(tt[0:19], "%Y/%m/%d-%H:%M:%S")
		hora=dt.hour
		minuto=dt.minute
		redondeado=roundt(minuto,dt.second)
		minuto=redondeado
		#print minuto, redondeado
		t=float(hora)+float(minuto)/60
		rtvec[i]=t
	rtveciter=iter(rtvec)
	if np.min(rtvec)==0.0 :
		a=1
	else:
		a=2
	newvec=np.zeros(((np.max(rtvec)-np.min(rtvec))/(10.0/60.0))+a)
	newprofile=np.zeros((770,len(newvec)))
	j=0
	i=0
	z=range(10,5010,10)
	print filename
	while j < len(rtvec):
		newvec[i]=rtvec[j]
		h=1
		#print j,rtvec[j],rtvec[j+1]
		if rtvec[j]==rtvec[j+1]:
			newprofile[:,i]=(oldm[:,j+1]+oldm[:,j])/2
			j=j+2
		else:
			newprofile[:,i]=oldm[:,j]
			j=j+1			
		i=i+1
		#print i,j
		#print newvec,rtvec
	allprf=newprofile[0:500,:]
	tarr=newvec
	writematrix(matrixdir+'2010'+flname[4:8]+'_'+estacion+'_matrix.txt',allprf,z,tarr,estacion,flname[0:8], 'Recovered from Wolf')
	#Configuracion para plotear sin valores en blanco, si un valor sale del rango aparece el valor maximo o minimo segun el caso
	for i in range(len(allprf[0,:])):
		for j in range(len(allprf[:,0])):
			if allprf[j,i] > max(levels):
				allprf[j,i] = max(levels)
			elif allprf[j,i] < min(levels):
				allprf[j,i] = min(levels)

	#contour plot. 
	c1=plt.contourf(tarr,z,allprf,levels)

	# Colorbarticks range y labels
	cticks=range(0,tickrange,tickt) 
	cb=plt.colorbar(c1,ticks=cticks)
	cb.set_label('Retrodispersion [a.Units]')
	plt.xlabel('Time [UT-6]')
	plt.ylabel('Height [m a.g.l.]')
	plt.title('Ceilometer ' +estacion + " 201" +filename[1:-6])
	ttext=np.max(tarr)/3
	plt.xlim(0,24)
	plt.ylim(0,zmax)
	#Para obtener mlh. 
	mlh=np.zeros(len(tarr),dtype=float)
	for i,t in enumerate(tarr):
	    vec=allprf[6:400,i]-allprf[5:399,i]
	    imin=np.argmin(vec)
	    mlh[i]=z[imin+5]
	#Plotear mlh
	plt.plot(tarr,mlh,'r_')
	#Guardar archivo de mlh
	writemlh( mlhdir + '2010'+flname[4:8]+ "_" +estacion+ "_mlh.txt",tarr,mlh,estacion)
	#Guardar figura
	plt.savefig( plotdir + '2010'+flname[4:8]+ "_" + estacion +".png")
	plt.show()	
	
