import numpy as np
import glob,os
import fileinput
import sys
import csv
import math
from ceilotools import *
from wavelets import *
outputdir= '/home/D1_CEILO/UNAM/PRCL/FDB_10/Remake/'
carpeta='/home/D1_CEILO/UNAM/PRCL/FDB_10/Perfiles/'
os.chdir(carpeta)
flist=glob.glob(carpeta+"*.txt")
flist=np.sort(flist)
def calmlh(fl,a0):
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
	if len(z) > 250: 
		a=60
		b=range(100,4000,10)
		fi=10
	else: 
		a=120
		b=range(100,4000,20)
		fi=5
	fle.close()
	mlh=haarcovtransfm(allprf,z,tarr,a,b,fi)
	#PARAMETErs
	return 	 mlh,tarr
def remaking(outputdir,flist,parameters):
	for filename in flist:
		print filename
		try: 
			[mlh,tarr]=calmlh(filename,parameters)
		except: 
			continue

		files= filename.split('/')[-1]
		writemlh(outputdir+files[0:8]+"_UNAM_mlh.txt",tarr, mlh, 'UNAM')
#for param in uplim:
outdir=outputdir+'WT/'
os.system('mkdir '+outdir)
remaking(outdir,flist,20)
