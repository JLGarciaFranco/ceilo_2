#!/usr/bin/env/python
# -*- coding: utf-8 -*
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.special import erf
import os,sys,glob
# Define idealized profile function method, inputs are backscattering matrix, height (z) and time (t) arrays.
def ipf(allprf,z,t):
	# Alocation of possible entraiment values s.
	s=np.arange(10,100,10)
	# obtenemos la longitud de s
	isz=len(s)
	#indices de z
	z_i=np.arange(0,len(z),dtype=int)
	# indices de s
	s_i=np.arange(0,isz)
	# niveles a probar como posiblles zm
	niv=len(z)
	# nivel minimo a partir donde se empieza a busar la altura.
	niv_min=15

	mlh=np.zeros(len(t))
	for i,tt in enumerate(t):

		rmsd=np.zeros((len(np.arange(niv_min,niv-np.max(s))),isz))
		s_espesor=np.zeros((len(np.arange(niv_min,niv-np.max(s))),isz))
	# Time-loop
		zk=np.zeros((len(t),isz),dtype=int)
		prf=allprf[:,i]
		# height loop over possible values of entrainment
		Bu=np.zeros((len(np.arange(niv_min,niv-np.max(s))),len(s)))
		B=np.zeros((len(z_i),len(np.arange(niv_min,niv-np.max(s))),len(s)))
		for k,z0 in enumerate(s):
			# Loop over all levels
			Bm=np.zeros(len(np.arange(niv_min,niv-np.max(s))))
			for ij,j in enumerate(np.arange(niv_min,niv-np.max(s))):
				zm=int(z[j-1])
			        s_espesor[ij,k]=float(z[int(j+s[k])]-z[j]-1)
                		Bm[ij]=np.nanmean(prf[0:j])
 		                Bu[ij,k]=np.nanmean(prf[j:j+s[k]])
			        B[z_i,ij,k]=(((Bm[ij]+Bu[ij,k])/2.)-((Bm[ij]-Bu[ij,k])/2.))*(erf(((z[z_i]-zm))/s_espesor[ij,k]))
               			rmsd[ij,k]=np.sqrt((1/float(niv))*(np.nansum(B[:,ij,k]-prf))**2)
				if np.nanmin(rmsd[niv_min:-1,k])>np.nanmean(np.nonzero(rmsd)):
					B[z_i,ij,k]=(((Bm[ij]+Bu[ij,k])/2.)-((Bm[ij]-Bu[ij,k])/2.))*(-erf(((z[z_i]-zm))/s_espesor[ij,k]))
				rmsd[ij,k]=np.sqrt((np.nansum(B[s[k]:len(z_i)-s[k],ij,k]-prf[s[k]:len(z_i)-s[k]]-1)**2)/float(niv))
			zk[i,k]=int(np.where(rmsd==np.nanmin(rmsd[:,k]))[0])+niv_min-1
		mlh[i]=int(z[zk[i,0]])
		if np.nonzero(np.nanmin(rmsd[:,k]))>np.nanmean(np.nonzero(rmsd)):
			mlh[i]=np.nan
		if mlh[i]<201 or mlh[i]>4300:
			mlh[i]=np.nan
	return mlh
def calmlh(fl):
	fle=open(fl,'r')
	fle.readline()
	fle.readline()
	fle.readline()
	fle.readline()
	fle.readline()
	fle.readline()
	allprf=np.genfromtxt(fl,skip_header=8)
	z=np.array(fle.readline().split()[1:],dtype=float)
	tarr=np.array(fle.readline().split()[1:],dtype=float)
	ipf(allprf,z,tarr)
#filename='20170402_UNAM_prf.txt'
#calmlh(filename)
