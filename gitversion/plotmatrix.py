#!/usr/bin/python/env
# -*- coding: utf8 -*-
#Version 201505 
import matplotlib
matplotlib.use('GtkAgg')
#Llamar a la clase ceilo. 
from ceiloclass import ceilo 
# importar estructura matematica y ploteo 
import numpy as np
import matplotlib.pyplot as plt
import os
#import smoothing del script smoothingkernel.py (suavizacion para vecinos cercanos)
from smoothingkernel import smoothmatrix
from smoothingkernel import smoothmatrixn
import fileinput
import sys
carpeta='/home/D1_CEILO/UNAM/CL3UT-6/'
outputdir='/home/D1_CEILO/UNAM/PRCL/Results/Plots/article/'
actualfile=carpeta+'U3121400.DAT'
dt=1.0/60.0*10
readceilo=ceilo(actualfile)
readceilo.init()
alldata=readceilo.readceilofile(actualfile,dt,770,10)
allprf=alldata[2]
tarr=alldata[0]
z=alldata[1]
zmax=5000.0 #np.max(z)
parametros=[0.333]
a0=0.01
amax=0.333
#a0=0.01
#n=100
at0=0.1
at1=0
convt=10
lstyles=['--',':','-','-.']
ctikcs=np.arange(0,0.3,0.015)
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
def normalizematrix(allprf,levels): 
	for i in range(len(allprf[0,:])):
       		for j in range(len(allprf[:,0])):
       		         if allprf[j,i] > max(levels):
                	        allprf[j,i] = max(levels)
             		 elif allprf[j,i] < min(levels):
	
        	              	allprf[j,i] = min(levels)
	return allprf
def FWHM(column):

        HM=np.max(column)/2.0
        imax=np.argmax(column)
	UPz=rango[imax:]
        Lz=rango[:imax]
        upcol=column[imax:]
	#print len(column)
        #print UPz.shape,upcol.shape
	#print len(np.flipud(upcol)),len(np.flipud(UPz))
        lowcol=column[:imax]
        z1=np.interp([HM],np.flipud(upcol),np.flipud(UPz))
        z2=np.interp([HM],lowcol,Lz)
        fwhm=z1[0]-z2[0]
        return fwhm
plt.figure()
rangs=range(0,710,100)
print tarr
for ij,bg in enumerate(parametros):
	a1=(amax-a0)/zmax
	conv=100
	print conv
	SK=smoothmatrixn(z,a0,a1,conv)
	SK=normalizematrix(SK,ctikcs)
	#print SK.shape
	#contour plot. 
	textstr=u'Parámetros \n'+r'$a_0 ='+str(at0)+'$ \n'+r'$a_{max}='+str(at1)+'$ \n'+r'$n = '+str(conv)+'$' 
	plt.figure(figsize=(15,9))
	c1=plt.contourf(SK,levels=ctikcs)
	plt.xlabel('Altura (m)',fontsize=20)
	plt.ylabel('Altura (m)',fontsize=20)
	rango=range(0,710,100)
	rang=range(0,7710,1000)
	list=[]
	for i in rang:
		list.append(str(i))
	#TICKS
	#print ctikcs
	#ticks=['0','6','12','18']
	plt.title(u'Kernel de suavización en altura',fontsize=22)
	plt.xticks(rango,list,fontsize=18)	
	plt.yticks(rango,list,fontsize=18)
	plt.colorbar(c1,ticks=ctikcs)
	plt.text(900,500,textstr,fontsize=22,bbox=props)
	plt.savefig(outputdir+'matrix_'+str(at0)+'_'+str(at1)+'_'+str(convt)+'.png')
	plt.show()
	plt.close()
	x=yy
	#plt.close()
	print 'hola'
	allfw=[]
	z1=np.array([10,100,200,300,400,500,600])
	col1=SK[400,:]
	column1=np.zeros(len(z))
	print 'entering loop'
	labes=['100','1000','2000','3000','4000','5000','6000']
	#plt.plot(col1,z,label='100')
	for i,h in enumerate(z1):
		print h
		column=SK[h,:]
		print len(column)
#		fwhm=FWHM(column)
#		allfw.append(fwhm)
		plt.plot(column,z,label=labes[i])
#		plt.show()
	plt.title('Funciones de peso del kernel',fontsize=20)
	plt.ylim([0,7000])
	plt.xticks(fontsize=16)
	plt.yticks(fontsize=16)
	plt.xlabel('Peso',fontsize=20)
	plt.legend(fontsize=16,title='H (m)')
	plt.ylabel('Altura (m)',fontsize=20)
	plt.savefig(outputdir+'kernel.png')
	plt.show()
	#	column1=column1+column
	#plt.plot(z,col1,label=parametros[ij],linestyle=lstyles[ij],color='k')
		#print column.size, np.sum(column), np.max(column), fwhm
	#allfw=np.asarray(allfw)
	#print allfw
	print len(allfw), len(z[9:700])
	#plt.plot(allfw,z[9:700],color='k')
allfw=np.asarray(allfw)
print allfw
#plt.legend(title=r'$a_{max}$',loc='upper right',fontsize=14)	
plt.ylabel(u'Altura [m]',fontsize=14)
#plt.xlim([3750, 4250])
plt.xlabel('Anchura a altura media [m]',fontsize=14)
#plt.yticks(rangs,ticks)
plt.title(u'Variación del FWHM con la altura',fontsize=17)
plt.savefig(outputdir+'fwhm_f.png')
plt.show()
plt.close()	
#	allfw=np.asarray(allfw)

		
# Colorbarticks range y labels
#cticks=range(0,tickrange,tickt) 
#cb=plt.colorbar(c1,ticks=cticks)
#cb.set_label('Retrodispersion [a.Units]')
#plt.xlabel('Averaging Kernel',fontsize=14)
#plt.ylabel('Height [m a.g.l.]',fontsize=14)3plt.title('All Kernels',fontsize=16)
#ttext=np.max(tarr)/3

#plt.ylim(0,zmax)
#plt.savefig( carpeta+"allkernels.png")
#plt.show()	
