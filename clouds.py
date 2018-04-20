import datetime 
import numpy as np
import glob,os
import fileinput
import pandas as pd
import sys
import csv
import math
from  ceilotools import histogram
from dftools import *
outputfile= '/home/D1_CEILO/UNAM/PRCL/Results/unam_cloudx.csv'
carpeta='/home/D1_CEILO/UNAM/perfiles/'
os.chdir(carpeta)
flist=glob.glob(carpeta+"*UNAM*.txt")
flist=np.sort(flist)
print(flist[-1])
def cloudvec(fl):
	fle=open(fl,'r')
	fle.readline()
	fle.readline()
	fle.readline()
	fle.readline()
	fle.readline()
	fle.readline()
	thrs=1550.0
	a=np.genfromtxt(fl,skip_header=8)
	z=np.array(fle.readline().split()[1:],dtype=float)
	tarr=np.array(fle.readline().split()[1:],dtype=float)
	day=fl.split('/')[-1][0:8]
	dia=int(day[6:8])
	year=int(day[0:4])
	mes=int(day[4:6])
	fle.close()
	zi=np.where(z==200.)
	zi=zi[0][0]
	zmax=np.where(z==4000.)
	zmax=zmax[0][0]
	#print zi,zmax
	nbs=[]
	tmps=[]
	count=len(tarr)*len(z[zi:zmax])
	sum=0
	for i,t in enumerate(tarr):
		
		for j,z1 in enumerate(z[zi:zmax]):
			try:
				sum=sum+a[j+zi,i]
			except IndexError: 
	#			print fl
				continue
	mu=sum/count
	deviat=0
	for i,t in enumerate(tarr):
		for j,z1 in enumerate(z[zi:zmax]):
			try: 

				deviat=deviat+((a[j+zi,i]-mu)**2)
			except IndexError:	
				continue

	sigma=deviat/(count-1)
	three=3*np.sqrt(sigma)
	two=np.sqrt(sigma)
	ec=mu+three
#	print 'media','sigma','3','s'
#	print mu,sigma,three,two
	#if ec > 1400: 
	#	print fl, ec
	for i,t in enumerate(tarr):
		for j,z1 in enumerate(z[zi:zmax]):
			try:
				if a[j+zi,i]>ec or a[j+zi,i]>thrs:
					horas=int(math.floor(t))
		        	        minutos=int(round((t-horas)*60,-1))
					tim=datetime.datetime(year,mes,dia,horas,minutos)
					tmps.append(tim)
					nbs.append(z1)
					break
			except IndexError:
				continue
#	print tmps
#	print nbs
	return tmps 
cldf=[]
for filename in flist:
	cloudt = cloudvec(filename)
	cldf.append(cloudt)
	print filename
cldf=[item for sublist in cldf for item in sublist]
cloudf=pd.DataFrame(data=cldf)		
print cloudf
#cloudf=ut_5tout_6(cloudf)	
cloudf.to_csv(outputfile)
#print cloudf 
