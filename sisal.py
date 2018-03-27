#!/usr/bin/python/env
# -*- coding: utf8 -*-
import numpy as np
import glob,os
import sys
import csv
import datetime
import pandas as pd
import colorplot 
from ceilotools import *
from netCDF4 import Dataset
carpeta='/home/D1_CEILO/SISAL/Results/07102016/Matrix/'
mlhgrad='/home/D1_CEILO/SISAL/Results/07102016/Gradient/'
flist=glob.glob(carpeta+"*.txt")
flist=np.sort(flist)
mlhlist=glob.glob(mlhgrad+"*.txt")
mlhlist=np.sort(mlhlist)
for filename in flist: 
	flname=filename.split('/')[-1]
	flname=flname.split('.')[0]
	grp=Dataset(carpeta+'NETCDF/'+grp+'.nc','w')
	grp.createDimension('t',len(tarr))
	grp.createDimension('z',len(z))
	z,tarr,allprf=readmatrixfile(filename)
	horizontal=grp.createVariable('time','f4',('t',))
	vertical=grp.createVariable('height','f4',('z',))
	retrodispersion=grp.createVariable('retrodispersion','f4',('t','z'))
	horizontal[:]=tarr
	vertical[:]=z+10
	retrodispersion[:]=allprf.transpose()
	grp.close()
	for fname in mlhlist: 
		if flname in mlhlist: 
			f=np.genfromtxt(fname,skip_header=4)
			mlh=f[:,1]	
			
	colorplot(1000,40,allprf,tarr,z,mlh,'/home/D1_CEILO/SISAL/Results/07102016/Plots/'+flname+'.eps')

	
	
	
	
