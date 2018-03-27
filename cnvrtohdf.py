#!/usr/bin/python/env
# -*- coding: utf8 -*-
import numpy as np
import glob,os
import sys
import csv
import datetime
import pandas as pd
from ceilotools import *
import h5py
carpeta='/home/D1_CEILO/UNAM/PRCL/FDB_10/Perfiles/'
cloudfile='/home/D1_CEILO/UNAM/PRCL/Results/angel_cloud.csv'
rmstr='rm ../../PRCL/FDB_10/Perfiles/HDF/*.hdf'
os.system(rmstr)
os.system('rm *.hdf')
flist=glob.glob(carpeta+"*.txt")
flist=np.sort(flist)
startingdate=datetime.datetime(2008,12,1,0,0)
cd=startingdate
cf=str(cd.year)+'_'+str(cd.month)+'_UNAM.hdf'
cloudf=pd.read_csv(cloudfile)
indx=cloudf.columns[1]
cloudate=pd.to_datetime(cloudf[indx])
cloudate=cloudate.tolist()
#print cloudate
for filename in flist: 
	print filename
	z,tarr,allprf=readmatrixfile(filename)
	flname=filename.split('/')[-1]
	flyear=int(flname[0:4])
	flm=int(flname[4:6])
	fld=int(flname[6:8])
	ut6=[]
	utc=[]
	cloudlist=np.zeros(len(tarr))
        if flm<10:
                mes='0'+str(flm)
        else:
                mes=str(flm)
	if fld <10: 
		dia='0'+str(fld)
	else: 
		dia=str(fld)
	for t,tt in enumerate(tarr):
		hour=int(np.floor(tt))
		minute=int(round((tt-hour)*60,-1))
		datobj=str(datetime.datetime(flyear,flm,fld,hour,minute))
		dat=datetime.datetime(flyear,flm,fld,hour,minute)
		if dat in cloudate:
			cloudlist[t]=int(1)
		else:
			cloudlist[t]=int(0)
		ut6.append(datobj)
	#ut6=np.asarray(ut6, dtype='datetime64')
	if flm == cd.month and flyear == cd.year: 
		with h5py.File(cf,'a') as hf:
			grp=hf.create_group(str(flyear)+mes+dia)
			dset=grp.create_dataset("Backscattering matrix",data=np.transpose(allprf))
			d2=grp.create_dataset("Datetime",data=ut6)
			cloudset=grp.create_dataset("Clouds",data=cloudlist)
			cloudset.attrs['Description']='Cloud index indicating if cloud was present at any given time.'
			cloudset.attrs['Key']='If cloud is present a value of 1 is reported, otherwise the given value is 0.' 
			cloudset.attrs['Cloud filter']='Cloud filter is adapted from Teschke 2008, to assess cloud or precipitation signals in the backscattering matrix using statistical information from the profile. Further information remit to PI_EMAIL'
			d2.attrs['DATA_TIME_ZONE']='UTC-06'
			grp.create_dataset("Height",data=z+10)
			#MLH=grp.create_dataset("MLH")
			#MLH.attrs['VAR_DESCRIPTION']='Mixing layer height (m) computed with the minimum-gradient method. No cloud filter applied'
			dset.attrs['Date']=str(fld)+'/'+mes+'/'+str(cd.year)
			dset.attrs['Row/Column']='Time/MLH'
			dset.attrs['VAR_DESCRIPTION']='Backscatter signal (arb. units) averaged every 10 min and smoothed vertically.'
	else:
		if len(z)>251:
			zresol=10
		else:
			zresol=20
		with h5py.File(cf,'a') as f:
			f.attrs['PI_NAME']='Grutter;Michel'
			f.attrs['PI_AFFILIATION']='Universidad Nacional Autonoma de Mexico; UNAM'
			f.attrs['PI_ADDRESS']='Centro de Ciencias de la Atmosfera UNAM;04510 Mexico City, Mexico'
			f.attrs['PI_EMAIL']='grutter@unam.mx'
			f.attrs['DO_NAME']='Garcia;Jorge'
			f.attrs['DATA_DESCRIPTION']='Ceilometer Backscatter signal'
			f.attrs['DATA_INSTRUMENT']='Ceilometer Vaisal CL31, S/N 134640006'
			f.attrs['DATA_LOCATION']='UNAM'
			f.attrs['DATA_LATITUDE']=19.3261
			f.attrs['DATA_LONGITUDE']=-99.1761
			f.attrs['DATA_TIME_ZONE']='UTC-06'
			f.attrs['DATA_TIME_RES']='10 min'
			f.attrs['DATA_RANGE']='10-5000 m'
			f.attrs['DATA_VERTICAL_RES']='10 m'
			f.attrs['DATA_GENERATION_DATE']='20161016T1200'
			
			f.attrs['DATA_AKNOWLEDGEMENT']='Data is made publicly available by the RUOA network (Red Universitaria de Observatorios Atmosfericos) operated by UNAM at www.ruoa.unam.mx'

		if flm<10:
			mes='0'+str(flm)
		else:
			mes=str(flm)
		cd=datetime.datetime(flyear,flm,fld,0,0)
		cf=str(flyear)+'_'+mes+'_UNAM.hdf'
		with h5py.File(cf, 'a') as hf:
			grp=hf.create_group(str(flyear)+mes+dia)
                        dset=grp.create_dataset("Backscattering matrix",data=np.transpose(allprf))
                        d2=grp.create_dataset("Datetime",data=ut6)
                        d2.attrs['DATA_TIME_ZONE']='UTC-06'
                        h=grp.create_dataset("Height",data=z+10)
			h.attrs['VAR_DESCRIPTION']= 'Height above ground level [m]'
                        #MLH=grp.create_dataset("MLH")
                        #MLH.attrs['VAR_DESCRIPTION']='Mixing layer height (m) computed with the minimum-gradient method'
                        dset.attrs['Date']=str(fld)+'/'+str(flm)+'/'+str(cd.year)
                        dset.attrs['Row/Column']='Time/MLH'
                        dset.attrs['VAR_DESCRIPTION']='Backscatter signal (arb. units) averaged every 10 min and smoothed vertically'

			
		
mstr='mv *.hdf ../../PRCL/FDB_10/Perfiles/HDF/'
os.system(mstr)
			
