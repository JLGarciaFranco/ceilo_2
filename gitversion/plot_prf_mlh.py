#!/usr/bin/python/env
# -*- coding: utf8 -*-
import numpy as np
import matplotlib.pyplot as plt
import math
import os,glob
import sys
from ceilotools import readmatrixfile
from colorplot import *
prfdir='/home/D1_CEILO/UNAM/PRCL/FDB_10/Perfiles/'
gradir='/home/D1_CEILO/UNAM/PRCL/FDB_10/MLH/'
c2dir='/home/D1_CEILO/UNAM/PRCL/FDB_10/Remake_2/C2/'
plotdir='/home/D1_CEILO/UNAM/PRCL/Results/Cplots/'
files=glob.glob(prfdir+'*2016*.txt')
files=np.sort(files)
#files=[prfdir]
def readmlh(filename):
	profil=np.genfromtxt(filename,skip_header=4)
	return profil
for filename in files:
	print filename
	z,tarr,allprf=readmatrixfile(filename)
	print len(z), len(tarr)
	print allprf.shape
#	x=yy
	fname=filename.split('/')[-1]
	fname=fname[0:8]
	gradname=gradir+fname+'_UNAM_mlh.txt'
	f=readmlh(gradname)
	mlh1=f[:,1]
	f2=readmlh(c2dir+fname+'_UNAM_mlh.txt')
	mlh2=f2[:,1]
	colorplot(400,100,allprf,tarr,z,mlh1,'trial1.png')
	plt.scatter(tarr,mlh2,color='red',s=12)
#	plt.show()
	plt.savefig(plotdir+fname+'.eps')
	plt.close()
