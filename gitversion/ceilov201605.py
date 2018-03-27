#!/usr/bin/python/env
#Version 201505 
import matplotlib
matplotlib.use('Agg')
#Llamar a la clase ceilo. 
from ceiloclass_fdb_1606 import ceilo 
from ceilotools import *
from auxhdf import * 
# importar estructura matematica y ploteo 
import numpy as np
import matplotlib.pyplot as plt
import os
#import smoothing del script smoothingkernel.py (suavizacion para vecinos cercanos)
from smoothingkernel import smoothmatrix
from smoothingkernel import smoothmatrixn
import fileinput
import sys
version = '201605'
print ( 'start')

#Argumentos para correr el loop. 
carpeta= sys.argv[2]
finaldir=sys.argv[3]
dt=int(sys.argv[5])
filename = sys.argv[7]
runv=sys.argv[4]
flag=sys.argv[6]
estacion = sys.argv[1]
a=''
if filename[1] == '7' or filename[1] =='9':
	a='200'
	print a
else: 
	a='201'	
#Carpetas a guardar y archivo actual.
#matrixdir=finaldir+runv+'/Matrix/'
#mlhdir=finaldir+runv+'/MLH/'#
#plotdir=finaldir+runv+'/Plots/'
actualfile='actualfile.dat'

#Colorbar maximum color level y ticks range
maxcollevel = 2100
#Un color cada colorss niveles (Valores sugeridos para que el colorbar tenga continuidad). 
colorss= (maxcollevel-100)/80
tickrange = maxcollevel+400
#Tick every tickt number of levels
tickt = (maxcollevel-100)/4
# remove line
lines=[]
for line in fileinput.input(carpeta+filename):
	lines.append(line)

#Cuantos files se van a procesar. 
nfiles=len(sys.argv)-8
print 'Numero de files' + str(nfiles)
if nfiles > 0 :
	print 'hola nfiles'
	for i in range(nfiles):
		filenamemas=sys.argv[i+8]
		for j,line in enumerate(fileinput.input(carpeta+filenamemas)):
			if j > 1:
				lines.append(line)
#Limpieza de los files

f=open(actualfile,'w')
f.writelines(lines)
f.close()

lines=[]
for line in fileinput.input(actualfile):
    if line.find('Closed') > -1 :
        print (line)
        print (line[0:12])

    if line[0:12] == '-File Closed':
            print ('hola')
    else:
            lines.append(line)
f=open(actualfile,'w')
f.writelines(lines)
f.close()
files = open(actualfile , 'r')
dz=10
nz=770
z0=5
zf=500
readceilo=ceilo(actualfile)
print (readceilo.ipos0)
print dz,nz
#Procesamiento de los datos. 
#Altura de los datos z. 
readceilo.init()
print ('readceilo.tarr')
dt=1.0/60.0*dt
alldata=readceilo.readceilofile(actualfile,dt,nz,dz)
allprf=alldata[2]
tarr=alldata[0]
z=alldata[1]
numprof=alldata[3]
zmax=5000.0 #np.max(z)
amax=0.333
a0=0.01
a1=(amax-a0)/zmax
#Calculo de la matriz e impresion de la matriz

SK=smoothmatrixn(z,a0,a1,100)
print ( SK )
allprf=np.dot(SK,allprf)
at0=0.1
ST=smoothmatrixn(tarr,at0,0,10)
allprf=np.dot(allprf,ST)
### para plot
idx=[i for i,zi in enumerate(z) if zi < zmax]
z=z[idx]
allprf=allprf[idx,:]
amin=np.min(allprf)
allprf=allprf #-amin
#allprf=np.log(allprf)
#tarr,zz,
#Colorbar maximum color level y ticks range
maxcollevel = 510
#Un color cada colorss niveles (Valores sugeridos para que el colorbar tenga continuidad). 
colorss= (maxcollevel-10)/80
tickrange = maxcollevel+10
#Tick every tickt number of levels
tickt = 100
#Levels of plot
levels=range(0,maxcollevel,colorss)
fname=a+filename[1:-6]
#Guardar archivo de matrix
carpetica=finaldir #+runv+'/'+fname
print carpetica
#os.system('mkdir '+carpetica)
if flag:
	writematrix( carpetica + fname + "_" +estacion+ "_matrix.txt",allprf,z,tarr,estacion,filename,runv)
	quit()
#Configuracion para plotear sin valores en blanco, si un valor sale del rango aparece el valor maximo o minimo segun el caso
for i in range(len(allprf[0,:])):
	for j in range(len(allprf[:,0])):
		if allprf[j,i] > max(levels):
			allprf[j,i] = max(levels)
		elif allprf[j,i] < min(levels):

			allprf[j,i] = min(levels)
#Hacer plot de contorno del perfil.

print fname
cloudate,nbs=cloudfilter(allprf,tarr,z,fname)

c1=plt.contourf(tarr,z,allprf,levels)

# Colorbarticks range y labels
cticks=range(0,tickrange,tickt) 
cb=plt.colorbar(c1,ticks=cticks)
cb.set_label('Backscattering [a.Units]')
plt.xlabel('Time [UT-6]')
plt.ylabel('Height [m a.g.l.]')
plt.title('Ceilometer ' +estacion + a +filename[1:-6])
ttext=np.max(tarr)/3

plt.xlim(0,24)
plt.ylim(0,zmax)
uplim=200
lowlim=10

#Para obtener mlh. 
mlh=np.zeros(len(tarr),dtype=float)
for i,t in enumerate(tarr):
	mlh[i]=algmlh(allprf,'Gradient',mlh,i,z,tarr,t,185)
#Plotear mlh
makehdf(fname,z,tarr,allprf,cloudate,mlh,estacion,carpetica)
plt.scatter(tarr,mlh,color='white')
#Guardar archivo de mlh
writemlh( carpetica + '/'+fname+ "_" +estacion+ "_mlh.txt",tarr,mlh,estacion)
#writenumofprof(matrixdir +'numprof/'+ a + filename[1:-6] + "_" +estacion+ "_prf.txt",numprof,tarr,estacion,filename)
#Guardar figura
plt.savefig( carpetica+ '/'+ a +filename[1:-6]+ "_" + estacion +".png")
plt.show()	
