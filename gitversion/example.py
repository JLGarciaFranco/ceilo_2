import numpy as np
import glob,os
import fileinput
import sys
import csv
import math
from wavelets import *
outputdir= '/home/D1_CEILO/UNAM/PRCL/FDB_10/Remake/'
carpeta='/home/D1_CEILO/UNAM/PRCL/FDB_10/Perfiles/'
os.chdir(carpeta)
flist=glob.glob(carpeta+"*.txt")
#flist2=glob.glob(carpeta+"*.txt")
#flist=flist+flist2
flist=np.sort(flist)
filename=flist[30]
def calmlh(fl):
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
        fle.close()
	return allprf,z,tarr

allprf,z,tarr=calmlh(filename)
if len(z)>250:
	fi=10
elif len(z)==250:
	fi=20
mlh=np.zeros(len(tarr),dtype=float)
for i,j in enumerate(tarr):
	mlh[i]=haarcovtransfm(allprf,z,i,'Automated',fi)
print mlh


