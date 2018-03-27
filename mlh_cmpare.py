#!/usr/bin/python/env
#Version 201605
#import matplotlib
#matplotlib.use('Agg')
import os 
import numpy as np
import glob 
import sys
import time 
import matplotlib.pyplot as plt
from ceilotools import * 
carpeta1='/home/D1_CEILO/UNAM/PRCL/V2/MLH/'
carpeta2='/home/D1_CEILO/UNAM/MLH/v201510_MLH_10_50_5000/'
flist1=glob.glob(carpeta1+'*.txt')
flist2=glob.glob(carpeta2+'*.txt')
newlist1=[]
newlist2=[]
flist1=np.sort(flist1)
flist2=np.sort(flist2)
base=1.0/6.0
for filename in flist2:
	fname1=filename.split('/')[-1]
	fname=fname1[0:8]
	for flename in flist1:
		fname2=flename.split('/')[-1]
		f2name=fname2[0:8]
		if f2name==fname:
			newlist1.append(filename)
			newlist2.append(flename)
			break
x=[]
y=[]
#print newlist2
#newlist1=np.sort(newlist1)
def readmlh(filename):
	profil=np.genfromtxt(filename,skip_header=4)
	return profil
for i,filename in enumerate(newlist1):
	#x=[]
	#y=[]
	t=1
	f=readmlh(filename)
	#print newlist2[i]
	rs=[]
	t=2
	f2=readmlh(newlist2[i])
	fname1=filename.split('/')[-1]
	fname=fname1[0:8]
	tarr1=f[:,0]
	mlh1=f[:,1]
	tarr2=f2[:,0]
	mlh2=f2[:,1]
	if len(tarr1)==len(tarr2):
		for j,tt in enumerate(tarr2):
			t1=myround(tt,base)
			t2=myround(tarr1[j],base)
			if t1==t2:
				x1=mlh1[j]
				y1=mlh2[j]
				x.append(x1)
				y.append(y1)
				if x1==y1:
					print 'Iguales'
				else: 
					print x1,y1
		#print x,y
		
x=np.asarray(x)
y=np.asarray(y)
r=np.corrcoef(x,y)
r=r[1,0]
totaldat=len(x)
rs.append(r)
#print np.linalg.lstsq(x,y)
textstr='$r$ Pearson = '+str(r)+'\n Numero de datos ='+str(totaldat)
#print textstr
#props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
#r=np.asarray(rs)
#print np.mean(r)
#fig, ax= plt.subplots(1)
plt.scatter(x,y)
plt.xlabel('OLD Data')
plt.ylabel('Newest Version')
#plt.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
plt.title( 'Comparacion de MLH'+fname)
#plt.savefig( '/home/D1_CEILO/UNAM/Plots/ceilos_'+fname+".png")
plt.show()
