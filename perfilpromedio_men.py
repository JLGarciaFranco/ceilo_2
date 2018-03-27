#!/usr/bin/python/env
# -*- coding: utf8 -*-
import numpy as np
import glob,os
import sys
import csv
import math
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from ceilotools import *
#outputdir= '/home/D1_CEILO/UNAM/MLH/v201510_MLH_10_50_5000/'
carpeta='/home/D1_CEILO/UNAM/PRCL/FDB_10/Perfiles/'
os.chdir(carpeta)
flist=glob.glob(carpeta+"*.txt")
flist=np.sort(flist)
perfildir='/home/D1_CEILO/UNAM/PRCL/Results/Perfiles/meses/prflprm_sflt_'

#Add cloudfilter 
#Cloudfile 
cdfile='/home/D1_CEILO/UNAM/PRCL/Results/cloud.csv'
cdread=pd.read_csv(cdfile)
cldates=cdread[cdread.columns[1]]
cldates=pd.to_datetime(cldates)
def readprofile(fl,tim):
	fle=open(fl,'r')
	for i in range(6):
		fle.readline()
	filename=fl.split('/')[1]
	#Check if filename is in UT-5 months. 
	allprf=np.genfromtxt(fl,skip_header=8)
	z=np.array(fle.readline().split()[1:],dtype=float)
	tarr=np.array(fle.readline().split()[1:],dtype=float)
	fle.close()
	tarr=np.round(tarr,3)
	i,=np.where(tarr==tim)
	if len(i) == 0: 
		return  
        try:
		perfil=allprf[:,int(i[0])]
	except IndexError:
		return
	#print perfil
	#print perfil
	#print len(perfil)
	if len(allprf) == 250:
		for i in range(1,501,2):				
			#print i
			perfil=np.insert(perfil,i,int(0))
	
	#print perfil		 	
	try:	
				
		return perfil
	except: 
		pass 

#print times 
#x=yy
def filterflist(flist,meses):	
	newlist=[]
	for filename in flist: 
		fl=filename.split('/')[-1]
		mes=int(fl[4:6])
		if mes in meses: 
			newlist.append(filename)
	return newlist
def prfilprom(flist,times,cloudf,cloudfilter):
	meanprf=np.zeros((500,len(times)))
	cldlist=cloudf.tolist()
	prl=np.zeros((500,len(flist)),dtype=np.int)
	for t,tt in enumerate(times):
		tt=round(tt,3)
		for j,filename in enumerate(flist):
			if cloudfilter:	
				fl=filename.split('/')[-1]
				ano=int(fl[0:4])
				mes=int(fl[4:6])
				dia=int(fl[6:8])
				horas=int(math.floor(tt))
                                minutos=int(round((tt-horas)*60,-1))
				if datetime.datetime(ano,mes,dia,horas,minutos) in cldlist: 
					continue
			profile=readprofile(filename,tt)
			#print profile, tt
			try:
				prl[:,j]=profile
			except: 
				continue
	#print prl 
		meanprf[:,t]=np.average(prl,axis=1,weights=prl.astype(bool))
	return meanprf
def prflatxt(flist,times,cldates,perfildir,estacion,nombre,especificacion):
	meanprf=prfilprom(flist,times,cldates,False)
#print meanprf
	z=range(0,5000,10)
	writematrix(perfildir, meanprf,z,times,estacion,nombre,especificacion)

##### PARTE FUNCIONAL DEL PROGRAMA ##### 
times=np.round(frange(0,24,float(10)/60.0),3)
meses=np.array([1,2])
for i in range(6): 
	newlist=filterflist(flist,meses)
	print len(newlist)
	prflatxt(newlist,times,cldates,perfildir+'_'+str(meses[0])+'_'+str(meses[1])+'.txt','UNAM','Perfil promedio Bimensual '+str(meses[0])+'-'+str(meses[1]),'Con filtro de nubes')
	meses=meses+2
	print meses
