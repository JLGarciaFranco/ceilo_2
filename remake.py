import matplotlib.pyplot as plt
import numpy as np
import glob,os
import fileinput
import sys
from ipf import ipf
import csv
import math
from ceilotools import *
outputdir='/home/D1_CEILO/UNAM/MLH18/'
#10os.system('mkdir '+outputdir)
carpeta='/home/D1_CEILO/UNAM/perfiles/'
#outputdir=carpeta=''
filelist=[]
rango=range(2011,2019)
for name in rango:
	name=str(name)
	flist=glob.glob(carpeta+"*14*TOLU*.txt")
	filelist+=flist
#print os.walk(carpeta)
#for x in os.walk(carpeta):
#	print x
#dirlist=[x[0] for x in os.walk(carpeta)]
#print dirlist
#for dir in dirlist:
#	fname=glob.glob(dir+"/*matrix*")
#	filelist.append(fname)
#flist=np.sort(filelist[1:])
station='UNAM'
filelist=glob.glob(carpeta+"*matrix*.txt")
print np.sort(filelist)
def calmlh(fl,method,outputdir):
	fle=open(fl,'r')
	fle.readline()
	fle.readline()
	fle.readline()
	fle.readline()
	fle.readline()
	files= fl.split('/')[-1]
	fle.readline()
	allprf=np.genfromtxt(fl,skip_header=8)
	z=np.array(fle.readline().split()[1:],dtype=float)
	tarr=np.array(fle.readline().split()[1:],dtype=float)
	t=tarr
	fle.close()
	mlh=np.zeros(len(tarr),dtype=float)
	grad=np.zeros(len(tarr),dtype=float)
	uplims=np.zeros(len(tarr),dtype=int)
	uplim=500
	nn=0
	method='C2'
	try:
		rlh=ipf(allprf,z,t)
	except:
		return mlh,tarr
	writemlh(outputdir+files[0:8]+"_"+station+"_rlh.txt",tarr, rlh, station)
	#uplims=rlh
	if len(z)==250:
		uplim=uplim/2

	while t[nn]<=7.5:
	#	if nn % 2 == 0 and len(z) ==250:
	#		uplim=uplim-1
	#	elif len(z)>250:
	#		uplim-=1
		if np.isnan(rlh[nn]):
			if nn>2:
				uplims[nn]=(uplims[nn-1]+1500)/2.
			else:
				uplims[nn]=1750
		elif rlh[nn]<800 or rlh[nn]>3000:
			if nn>4:
				if np.isnan(np.nanmean(uplims[nn-4:nn])):
					uplims[nn]=1750
				else:
					uplims[nn]=int(np.nanmean(uplims[nn-4:nn-1]))
			else:
				if np.isnan(np.nanmean(rlh[nn:nn+4])):
					uplims[nn]=1750
				else:
					uplims[nn]=int(500+(np.nanmean(rlh[nn:nn+4])/2.))
		else:
			uplims[nn]=int(rlh[nn])
		nn+=1
		#uplims[nn]
	#print t[nn],z[uplim]
	while t[nn]<=12.:
		#if len(z)==250:
		#	uplim+=2
		#else:
		#	uplim+=4
	# Calculate the coefficients. This line answers the initial question. 
		coefficients = np.polyfit([7.5,12], [1750,3250], 1)

	# Print the findings
#	print 'a =', coefficients[0]
#	print 'b =', coefficients[1]

	# Let's compute the values of the line...
		polynomial = np.poly1d(coefficients)
#		print t[nn],polynomial(t[nn])
#		x_axis = np.linspace(0,500,100)
#		y_axis = polynomial(x_axis)
		if np.isnan(rlh[nn]):
			try:
				uplims[nn]=int((1250)/4.+(3*polynomial(t[nn])/4.))
			except:
				uplims[nn]=1750
		else:
#			try:
#				uplims[nn]=500+rlh[nn])/4.
#			except:
			if rlh[nn]<2700:
				uplims[nn]=int((rlh[nn]+polynomial(t[nn]))/2.)
			else:
				uplims[nn]=int(polynomial(t[nn]))
#		print uplims[nn]
		nn+=1
		if nn==len(tarr):
			break
	#print t[nn],z[uplim]
	while nn<len(tarr) and t[nn]<=18.25:
		try:
			zeroheight=int(z[np.where(allprf[:,nn]<=1)[0][0]])
		except:
			zeroheight=3500
		if zeroheight <= 3500:
			uplims[nn]=zeroheight
		else: 
			uplims[nn]=3500
		nn+=1
	#while t[nn]<=19.5:
			#if len(z)==250:
			#	uplim+=2
			#else:
			#	uplim+=4
	#		if np.isnan(rlh[nn]):
	#			uplims[nn]=3000
	#		else:
	#			uplims[nn]=(3000+rlh[nn])/2.
	#		nn+=1
	#		if nn==len(tarr):
	#			break
		#print t[nn],z[
	#print t[nn],z[uplim]
	while nn<len(tarr):
		#if len(z)==250:
		#	uplim=uplim-1
		#else:
		#	uplim-=3
		if np.isnan(rlh[nn]):
			if np.isnan(np.nanmean(uplims[nn-5:nn])):
				uplims[nn]=1750
			else:
				uplims[nn]=int(np.nanmean(uplims[nn-5:nn]))
		elif rlh[nn]<1000 or rlh[nn]>3000:
			if nn>len(t)-2:
				if np.isnan(np.nanmean(uplims[nn-4:nn])) and np.isnan(int(z[np.where(allprf[:,nn]<=1)[0][0]])) or int(z[np.where(allprf[:,nn]<=1)[0][0]])>2800:
					uplims[nn]=1750
				elif int(z[np.where(allprf[:,nn]<=1)[0][0]])<3000:
					uplims[nn]=(1750+int(z[np.where(allprf[:,nn]<=1)[0][0]]))/2.
				else:
					uplims[nn]=int((np.nanmean(uplims[nn-4:nn])+1750)/2.)
			else:
				if np.isnan(np.nanmean(rlh[nn-6:nn+1])):
					uplims[nn]=1750
				else:
					uplims[nn]=int((np.nanmean(uplims[nn-6:nn])+1750)/2.)
		else:
			uplims[nn]=int(rlh[nn])
		nn+=1
#	print uplims[0:15]
	for i,t in enumerate(tarr):
#		grad[i]=algmlh(allprf,uplim,lowlim,'WT',mlh,i,z,tarr,t)
		#print 'Ipm = ', algmlh(allprf,uplim,lowlim,'Ipm',mlh,i,z,tarr)
		#print 'WT = ', algmlh(allprf,uplim,lowlim,'WT',mlh,i,z,tarr)
		#print 'Compuesto 1= ',algmlh(allprf,uplim,lowlim,'Composite 1',mlh,i,z,tarr)
			#print t, z[uplims[i]]
#		print i,t,uplims[i]
		mlh[i]=algmlh(allprf,'WT',mlh,i,z,tarr,t,uplims[i])
		if mlh[i] < 230:
			print "Fakeeeee"+ str(mlh[i])
		#print mlh[i]
	return mlh,tarr
def remaking(outputdir,flist,method):
	for filename in flist:
		files= filename.split('/')[-1]
		if outputdir+files[0:8]+"_"+station+"_rlh.txt" in glob.glob(outputdir+"*_"+station+"_rlh.txt"):
			continue
		print filename
		#filename=filename[0]
		print(filename)
		[mlh,tarr]=calmlh(filename,method,outputdir)
		writemlh(outputdir+files[0:8]+"_"+station+"_mlh.txt",tarr, mlh, station)
		#writemlh(files[0:8]+"_UNAM_mlh.txt",tarr, mlh, 'UNAM')
		#except:
		#	continue
#for param in uplim:
folder=['WT/','Gradient/','C2/']
folder=['C2_WT/']
#for fld in folder:
outdir=outputdir
print filelist[0:12]
#	os.system('mkdir '+outdir)
remaking(outdir,filelist,'C2')
