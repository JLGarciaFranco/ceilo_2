#!/usr/bin/python/env
# -*- coding: utf8 -*-
import numpy as np
import matplotlib.pyplot as plt
import math
import os,glob
import sys 
import pandas as pd
carpeta='/home/D1_CEILO/UNAM/PRCL/Results/Perfiles/meses/'
os.chdir(carpeta)
outputdir='/home/D1_CEILO/UNAM/PRCL/Results/'
outfile=outputdir+'c2_article_db.csv'
flist=glob.glob(carpeta+"*perfil*.txt")
flist2=glob.glob(carpeta+"*prfl*.txt")
flist=np.sort(flist)
flist2=np.sort(flist2)
print flist
print flist2
df=pd.read_csv(outfile)
filename=outputdir+'Perfiles/perfilprom_snbs.txt'
#dfold.index=dfold[dfold.columns[0]]
#standard=dfold['Min60']
df.index=df[df.columns[0]]
df.index=pd.to_datetime(df.index)
print df.columns
df=df['Delice']
df=df.dropna()
data=df.groupby([df.index.hour, df.index.minute]).mean()
flist=np.sort(flist)
l=700
#print flist 
#x=yy
def matrixplot(filename,place,titulo,mmax):
	with open(filename,'r') as f: 
		for i in range(6):
			f.readline()
		allprf=np.genfromtxt(filename,skip_header=8)
		z=np.array(f.readline().split()[1:],dtype=float)
		global tarr
		tarr=np.array(f.readline().split()[1:],dtype=float)
	#Configuracion para plotear sin valores en blanco, si un valor sale del rango apar$
	#Colorbar maximum color level y ticks range
	maxcollevel = mmax
	#maxcollevel=maxcollevel+int(maxcollevel*0.5)
	#Un color cada colorss niveles (Valores sugeridos para que el colorbar tenga conti$
	colorss= (maxcollevel-10)/100
	tickrange = maxcollevel+10
	#Tick every tickt number of levels
	tickt = 40
	#Levels of plot
	levels=range(0,maxcollevel,colorss)
	for i in range(len(allprf[0,:])):
		for j in range(len(allprf[:,0])):
			dif1=allprf[j,i]-allprf[j-1,i]
			dif2=allprf[j,i]-allprf[j,i-1]
		        if allprf[j,i] > max(levels):
		                allprf[j,i] = max(levels)
		        elif allprf[j,i] < min(levels) or allprf[j,i] == np.nan:

		                allprf[j,i] = min(levels)
			if tarr[i] > 16. and z[j] > 200: 

				if np.abs(dif1) > 150 or np.abs(dif2) > 150:
					allprf[j,i] = allprf[j-1,i-1]
	#Hacer plot de contorno del perfil. 
	plt.figure(figsize=(15,9))
#	plt.subplot(place)
	c1=plt.contourf(tarr,z,allprf,levels)

	# Colorbarticks range y labels
	cticks=range(0,tickrange,tickt)
	cb=plt.colorbar(c1,ticks=cticks)
	cb.set_label(u'Backscattering [ a. Units]',fontsize=20)
	plt.xlabel('Time [UT-6]',fontsize=22)
	plt.ylabel('Height [m]',fontsize=22)
	plt.title(titulo,fontsize=24)
	plt.xlim(0,24)
	plt.xticks(np.arange(0,24,3),fontsize=18)
	plt.ylim(100,4000)
	plt.yticks(fontsize=18)
def perflindv(filename,file2,place,titulo,color,label):
	with open(filename,'r') as f: 
		for i in range(6):
			f.readline()
		allprf=np.genfromtxt(filename,skip_header=8)
		z=np.array(f.readline().split()[1:],dtype=float)
		tarr=np.array(f.readline().split()[1:],dtype=float)
	sinfiltro=np.genfromtxt(file2,skip_header=8)
	lista=[3.,6.,9.,12.,15.,18.,21.]
	z=range(100,5000,10)
	place=place+320
	print place
	plt.subplot(place)
	l=700
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
		plt.plot(vec,z,color=color,linestyle='-')
		plt.plot(vec2,z,color='b',linestyle='-')
		l=l+700
	plt.plot(vec,z,color=color,linestyle='-',label='Filtered')
	plt.plot(vec2,z,color='b',linestyle='-',label='NA')
	plt.xlabel('Time (h) UT-6',fontsize=17)
	plt.xticks(np.linspace(700, 4900, 7),['3','6','9','12','15','18','21'],fontsize=14)
	plt.yticks(fontsize=14)
	plt.xlim([550,(4900+900)])
	plt.ylabel('Height [m]',fontsize=17)
	plt.title( titulo,fontsize=18)
	plt.legend(loc='upper right',fontsize=12,title='Filter')
	plt.grid()
	plt.tight_layout()
	plt.grid()
meses=[1,2,3,4,5,0]
maximos=[160,190,360,460,360,160]
places=1
titulos=['January-February','March-April','May-June','July-August','September-October','November-December']
#plt.figure(figsize=(12,16))
matrixplot(filename,places,u'Mean filtered backscattering ',360)
plt.scatter(tarr,data,color='white',s=13)
plt.savefig(outputdir+'paperplots/prfilwfiltr_3.eps')
plt.show()
x=yy
for j,i in enumerate(meses): 
	filename=flist[j]
#filename=flist[0]
	file2=flist2[j]
	titulo=titulos[j]
	print filename,places,titulo
	maxi=maximos[j]
#matrixplot(filename,places,u'Mean backscattering ',530)
#titulo=''
#	perflindv(file2,places,titulo,'b','Nubes')
	perflindv(filename,file2,places,titulo,'k','NA')
	plt.grid()
	legend=plt.legend(loc='upper right',fontsize=13,title='Filter')
	legend.get_title().set_fontsize('13')
	plt.tight_layout()
	places=places+1

#plt.scatter(tarr,data,color='black',s=12)
#plt.savefig('/home/D1_CEILO/UNAM/PRCL/Results/Plots/article/colorplot_nofilter.eps')
plt.show()


