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
flist=glob.glob(carpeta+"201*.txt")

for filename in flist:
	if '2010' in filename:
		flist.remove(filename)
flist=np.sort(flist)
perfildir='/home/D1_CEILO/UNAM/PRCL/Results/paperplots/prfilfiltr.txt'

#Add cloudfilter 
#Cloudfile 
cdfile='/home/D1_CEILO/UNAM/PRCL/Results/angel_cloud.csv'
cdread=pd.read_csv(cdfile)
cldates=cdread[cdread.columns[1]]
cldates=pd.to_datetime(cldates)


times=np.round(frange(0,24,float(10)/60.0),3)
#print times 
#x=yy
def prfilprom(flist,times,cloudf,cloudfilter):
	meanprf=np.zeros((500,len(times)))
	cldlist=cloudf.tolist()
	#print cldlist
	prl=np.zeros((500,len(flist)),dtype=np.int)
	#print prl
	for t,tt in enumerate(times):
		tt=round(tt,3)
		for j,filename in enumerate(flist):
			print filename	
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
	#print np.average(prl,axis=1,weights=prl.astype(bool))
	#print np.average(prl,axis=0,weights=prl.astype(bool))

		meanprf[:,t]=np.average(prl,axis=1,weights=prl.astype(bool))
	return meanprf
meanprf=prfilprom(flist,times,cldates,True)
#print meanprf
z=range(0,5000,10)
writematrix(perfildir, meanprf,z,times,'UNAM','Perfiles promedio','Sin filtro')
