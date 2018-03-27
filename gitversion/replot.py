#!/usr/bin/python/env
# -*- coding: utf8 -*-
#Version 201505 
import matplotlib
matplotlib.use('GtkAgg')
from colorplot import colorplot
# importar estructura matematica y ploteo 
import numpy as np
import matplotlib.pyplot as plt
import os, glob
outputdir= '/home/D1_CEILO/TOLU/Preliminary/Cplots_var/'
carpeta='/home/D1_CEILO/TOLU/Preliminary/Matrix/'
os.chdir(carpeta)
mlhdir='/home/D1_CEILO/TOLU/Preliminary/MLH/'
flist=glob.glob(carpeta+"*.txt")
flist=np.sort(flist)
def maxim(maxo):
	counter=0
	while counter < maxo: 
		counter+=50
	return counter
def readmlh(filename):
	profil=np.genfromtxt(filename,skip_header=4)
	return profil
def calmlh(fl):
	fle=open(fl,'r')
	for i in range(6):
		fle.readline()
	allprf=np.genfromtxt(fl,skip_header=8)
	z=np.array(fle.readline().split()[1:],dtype=float)
	tarr=np.array(fle.readline().split()[1:],dtype=float)
	tarr=np.round(tarr,3)
	return tarr, z, allprf
for filename in flist:
	fname=filename.split('/')[-1]
	fname=fname[:8]
	mlhname=mlhdir+fname+'_TOLU_mlh.txt'
	mlhs=readmlh(mlhname)
	mlh=mlhs[:,1]
	t,z,allprf=calmlh(filename)
	maximum=np.max(allprf)
	if maximum < 400: 
		maxi=maxim(maximum)
		jump=25
		levels=40
	else: 
		maxi=450
		jump=50
		levels=40
	colorplot(maxi,levels,jump,allprf,t,z,mlh,filename)
	plt.savefig(outputdir+fname+'.png')
	plt.close()
