#!/usr/bin/python/env
import matplotlib
matplotlib.use('GtkAgg')
import numpy as np
import glob,os
import fileinput
import sys
import csv
import math
from ceilotools import *
outputdir= '/home/D1_CEILO/JQRO/Results_day/MLH_c2/'
#os.system('mkdir '+outputdir)
carpeta='/home/D1_CEILO/JQRO/Results_day/Angel/'
filelist=[]
rango=range(3,7)
#3for name in rango:
#	name=str(name)
#flist=glob.glob(carpeta+"*matrix*.txt")
#	filelist+=flist
#print os.walk(carpeta)
#for x in os.walk(carpeta):
#	print x
dirlist=[x[0] for x in os.walk(carpeta)]
print dirlist
for dir in dirlist:
	fname=glob.glob(dir+"/*matrix*")
	filelist.append(fname)	
flist=np.sort(filelist[1:])
#flist=glob.glob(carpeta+"20160302*.txt")
print flist
def calmlh(fl,method):
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
	t=tarr
	fle.close()
	mlh=np.zeros(len(tarr),dtype=float)
	grad=np.zeros(len(tarr),dtype=float)
	uplims=np.zeros(len(tarr),dtype=int)
	uplim=210
	nn=0
	method='C2'
	if len(z)==250: 
		uplim=uplim/2

	while t[nn]<=7.0:
		if nn % 2 == 0 and len(z) ==250:
			uplim=uplim-1
		elif len(z)>250:
			uplim-=1  
		uplims[nn]=uplim 
		nn+=1
	#print t[nn],z[uplim]
	while nn<len(tarr) and t[nn]<=14.5:
		if len(z)==250:
			uplim+=2
		else:
			uplim+=4
		uplims[nn]=uplim
		nn+=1
		if nn==len(tarr):
			break 
	#print t[nn],z[uplim]
	while nn<len(tarr) and t[nn]<=16.5:
		uplims[nn]=uplim
		nn+=1
	#print t[nn],z[uplim]
	while nn<len(tarr):
		if len(z)==250:
			uplim=uplim-1
		else:
			uplim-=3
		uplims[nn]=uplim 
		nn+=1
	#print t[nn-1],z[uplim]
	#PARAMETERS
	#print lowlim
	#print lowlim/2
	for i,t in enumerate(tarr):
#		grad[i]=algmlh(allprf,uplim,lowlim,'WT',mlh,i,z,tarr,t)
		#print 'Ipm = ', algmlh(allprf,uplim,lowlim,'Ipm',mlh,i,z,tarr)
		#print 'WT = ', algmlh(allprf,uplim,lowlim,'WT',mlh,i,z,tarr)
		#print 'Compuesto 1= ',algmlh(allprf,uplim,lowlim,'Composite 1',mlh,i,z,tarr)
		try:
			#print t, z[uplims[i]]
			mlh[i]=algmlh(allprf,method,mlh,i,z,tarr,t,uplims[i])
			if mlh[i] < 300:
				print "Fakeeeee"+ str(mlh[i])
		except:
			continue
		#print mlh[i]
#	x=yy
	return 	 mlh,tarr
def remaking(outputdir,flist,method):
	for filename in flist:
		print filename
		filename=filename[0]
		[mlh,tarr]=calmlh(filename,method)
		files= filename.split('/')[-1]
		writemlh(outputdir+files[0:8]+"_UNAM_mlh.txt",tarr, mlh, 'UNAM')
		#writemlh(files[0:8]+"_UNAM_mlh.txt",tarr, mlh, 'UNAM')
		#except:
		#	continue
#for param in uplim:
folder=['WT/','Gradient/','C2/']
folder=['C2_WT/']
#for fld in folder: 
outdir=outputdir
#	os.system('mkdir '+outdir)
remaking(outdir,flist,'C2')
