#!/usr/bin/python/env
# -*- coding: utf8 -*-
#Version 201605
#import matplotlib
#matplotlib.use('Agg')
import os 
import numpy as np
import glob 
import sys
import math
import pandas as pd
import time 
import subprocess
import matplotlib.pyplot as plt
import datetime
from ceilotools import *
from dftools import * 
carpeta1='/home/D1_CEILO/UNAM/PRCL/Angel/'
outputdir='/home/D1_CEILO/UNAM/PRCL/Results/'
outfile=outputdir+'jqro.csv'
os.system('rm '+outfile)
#newfile=outputdir+'c2_article_db.csv'
#cloudfile=outputdir+'angel_cloud.csv'
dirnames=['Raw']
dirlist=['MLH']
#dirlist=dirnames
base=1.0/6.0
darange=pd.date_range(start=datetime.datetime(2008,12,2,0,0),end=datetime.datetime(2016,6,4,23,55),freq='5min')
ndex=pd.to_datetime(darange)
df=pd.DataFrame(index=ndex)
df.index=pd.to_datetime(df.index)
def readmlh(filename):
	profil=np.genfromtxt(filename,skip_header=4)
	return profil
for h,direct in enumerate(dirlist):
	label=dirnames[h]
	date=[]
	mlh=[]
	carpeta=carpeta1+direct+'/'
	print carpeta
	flist1=glob.glob(carpeta+'*mlh*.txt')
	flist1=np.sort(flist1)
	print flist1
	for i,filename in enumerate(flist1):
		f=readmlh(filename)
		fname1=filename.split('/')[-1]
		fname=fname1[0:8]
		ano=int(fname[0:4])
		mes=int(fname[4:6])
		dia=int(fname[6:8])
		try: 
			tarr1=f[:,0]
			mlh1=f[:,1]
		except IndexError: 
			continue 
		for j,tt in enumerate(tarr1):
			horas=int(math.floor(tt))
			minutos=int(round((tt-horas)*60))
			if minutos >= 60:
				print str((tt-horas)*60),minutos, filename
			
			cdatime=datetime.datetime(ano,mes,dia,horas,minutos)
			#if labe[h]=='15' and int(minutos)%15!=0:
			#	print tt,cdatime
			mlh.append(mlh1[j])
			date.append(cdatime)
#Function to adjust UT-5 a UT-6
#       if flname[0:4]=='2009' and (int(flname[4:6])>4 or (int(flname[4:6])==4 and int(flname[6:8])>=20)):
	print len(mlh)
	mlh1=np.asarray(mlh,dtype=int)
	dh=pd.DataFrame(date)
	df1=pd.DataFrame(mlh,index=date)
	df1.columns=[label]
	df1.index=pd.to_datetime(df1.index)
	df=df.join(df1,how='outer')
#for column in df:
	df[label+'_filtered']=pullclouds(df[label],cloudfile)
df.index=pd.to_datetime(df.index)
df=df.dropna(how='all')
df=ut_5tout_6(df)
#df['Delice']=pullclouds(df['C2'],cloudfile)
#nuevodf=pd.DataFrame(data=grad,index=df.index)
#nuevodf.columns=['G-F2']
#']
#nuevodf['C1']=df['Compuesto']
#df['Std w Clouds']=newdf
#df2.index=pd.to_datetime(df2.index)
#df2=ut_5tout_6(df2)
#df=df.join(df2,how='outer')
df.to_csv(outfile)


