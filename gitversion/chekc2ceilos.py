#!/usr/bin/python/env
#Version 201605
import matplotlib
matplotlib.use('Agg')
import os 
import numpy as np
import glob 
import sys
import time 
import matplotlib.pyplot as plt
from ceilotools import * 
carpeta1='/home/D1_CEILO/UNAM/PRCL/V2/Matrix/'
carpeta2='/home/D1_CEILO/UNAM/matrices/v201510_10_matrix/'
flist1=glob.glob(carpeta1+'2012*.txt')
flist2=glob.glob(carpeta2+'2012*.txt')
newlist1=[]
newlist2=[]
daylist=['09','12','16','25','28']
flist1=np.sort(flist1)
flist2=np.sort(flist2)
base=1.0/6.0

for filename in flist2:
	fname1=filename.split('/')[-1]
	fname=fname1[0:8]
	if fname[6:8] in daylist:
		for flename in flist1:
			fname2=flename.split('/')[-1]
			f2name=fname2[0:8]
			if f2name==fname:
				newlist1.append(filename)
				newlist2.append(flename)
x=[]
y=[]
newlist1=np.sort(newlist1)
print newlist1
for i,filename in enumerate(newlist1):
	x=[]
	y=[]
	t=1
	f=readmatrixfile(filename,t)
	#print newlist2[i]
	rs=[]
	t=2
	f2=readmatrixfile(newlist2[i],t)
	fname1=filename.split('/')[-1]
	fname=fname1[0:8]
	tarr1=f[0]
	allpf1=f[1]
	tarr2=f2[0]
	allprf2=f2[1]
	if len(tarr1)==len(tarr2):
		
		for j,tt in enumerate(tarr2):
			t1=myround(tt,base)
			t2=myround(tarr1[j],base)
			if t1==t2:
				#print tt
				for k in range(0,500):
					x1=allpf1[k,j]
					y1=allprf2[k,j]
					x.append(x1)
					y.append(y1)
		#print x,y
		
		x=np.asarray(x)
		y=np.asarray(y)
		r=np.corrcoef(x,y)
		r=r[1,0]
		totaldat=len(x)
		rs.append(r)
	#print np.linalg.lstsq(x,y)
		textstr='$r$ Pearson = '+str(r)+'\n Numero de datos ='+str(totaldat)
		print textstr
	#props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
r=np.asarray(rs)
print np.mean(r)
	#fig, ax= plt.subplots(1)
	#plt.scatter(x,y)
	#plt.xlabel('Retrodispersion Ceilo 2')
	#plt.ylabel('Retrodispersion Ceilo 1')
	#ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
	#plt.title( 'Comparacion de ceilometros'+fname)
	#plt.savefig( '/home/D1_CEILO/UNAM/Plots/ceilos_'+fname+".png")
	#plt.show()

				
