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
import matplotlib.pyplot as plt
import datetime
from ceilotools import runningMeanFast
from dftools import *
def minimum(mlh,dat):
	#First check 
	fc=np.min(mlh)
	#Second check 
	sc=mlh[np.argmax(np.diff(mlh))]
	if fc == sc:
		#print 'first try'
		return sc
	else: 
		st=[]
		diff=0
		for j in range(len(mlh)-3):
			dife=mlh[j+3]-mlh[j]
			if dife > diff: 
				diff=dife
				savej=j
		if mlh[savej]==fc or mlh[savej]==sc:
		#	print 'second try'
			return mlh[savej]
		else: 
			dif2=0
			dif4=0
			for j in range(len(mlh)-4):
				df4=mlh[j+4]-mlh[j]
				df2=mlh[j+2]-mlh[j]
				if df2 > dif2 and df4 >dif4:
					dif4=df4
					dif2=df2
					fj=j
			if mlh[fj]==fc or mlh[fj]==sc or fj == savej:
		#		print '3rd try' 
				return mlh[fj]
			else:
		#		print 'missing'
		#		print savej,fj,np.argmin(mlh),np.argmax(np.diff(mlh))
				if np.abs(savej - np.argmax(np.diff(mlh))) <=3:
					nj=int((savej+np.argmax(np.diff(mlh)))/2.)
					return mlh[nj]
				else:
					avgn=int((savej+np.argmax(np.diff(mlh))+fj)/3.)
					return mlh[avgn]
def growth(dates,mlh):
	mlh=np.array(mlh)
	xdate=[]
	for dt in dates:
		m=dt.minute
		h=dt.hour
		add=m/60.
		xdate.append(h+add)
	#print np.polyfit(xdate,mlh,1)
	r= np.corrcoef(xdate, mlh)[0,1]
	r2= r**2.
	stindex=len(mlh)
	while 1-r2>=0.05 and len(mlh)>=20:
		xdate=xdate[:-1]
		mlh=mlh[:-1]
		if np.corrcoef(xdate,mlh)[0,1]<r and r>0.85:
			break
		r=np.corrcoef(xdate,mlh)[0,1]
		r2=r**2.		
	maxindex=stindex-len(mlh)
	m,b=np.polyfit(xdate,mlh,1)
	xdate=np.array(xdate)
	nmlh=xdate*m+b
	return m,maxindex
				
def grwthrate(dates,mlh):
	onemax=np.argmax(np.diff(mlh))
	nmlh=[]
	nmlh2=[]
	dat=[]
	dat2=[]
	meses=[]
	mesesito=dates[0].month
	meses.append(mesesito)	
	for i,dt in enumerate(dates):
		if dt.hour > 6.0 and dt.hour < 14.0:
#			print dt.minute
			nmlh.append(mlh[i])
			dat.append(dates[i])
			if dt.hour < 11.0:
				nmlh2.append(mlh[i])
				dat2.append(dates[i])	
	dindex=np.where(mlh==nmlh[0])	
	indice=minimum(nmlh2,dat2)
	indice=np.where(nmlh==indice)
	
	indice=indice[0][0]
	#print dat2[indice],nmlh2[indice]
	nlmh=nmlh[indice:]
	dat=dat[indice:]
	m,maxindex=growth(dat,nlmh)
	return m,dindex+indice,maxindex
print 'Entering Growth rates'		
carpeta1='/home/D1_CEILO/UNAM/PRCL/FDB_10/Remake/AVG'
outputdir='/home/D1_CEILO/UNAM/PRCL/Results/'
outf=outputdir+'all_avgperiods.csv'
outfile=outputdir+'c2_article_db.csv'
dirlist=[]
labe=['Gradient','Wavelet']
base=1.0/6.0
df=pd.read_csv(outfile)
df.index=df[df.columns[0]]
#print df.columns
df.index=pd.to_datetime(df.index)
#print df.head()
lista=['Delice']
data=df[lista]
data=data.dropna()
#print data
name='one'
#meses, maxi, mini= mlhmax(data,name)
#data=data['2011':'2016']
#meanly=data.groupby([data.index.month]).mean()
monthly=data.groupby([data.index.year,data.index.month,data.index.hour,data.index.minute]).mean()
meanly=data.groupby([data.index.year,data.index.month]).mean()
meanly=np.asarray(meanly)
ano=monthly.index[0][0]
mes=monthly.index[0][1]
fdatey=2016
fdatem=6
j=0
#print monthly.index[0:4]
m=[]
dt=[]
while ano != fdatey or mes !=fdatem:
	date=[datetime.datetime(monthly.index[j][0],monthly.index[j][1],1,monthly.index[j][2],monthly.index[j][3])]
	x=np.array(monthly.loc[monthly.index[j]])
	while mes  == monthly.index[j][1]:
		mes=monthly.index[j][1]
		date.append(datetime.datetime(monthly.index[j][0],monthly.index[j][1],1,monthly.index[j][2],monthly.index[j][3]))
		x=np.append(x,monthly.loc[monthly.index[j]])
		j+=1
#	x=yy
	m1,minimo,maxi=grwthrate(date,x)
	m.append(m1)
	dt.append(datetime.datetime(date[0].year,date[0].month,1))
#	plt.plot(date,x)
#	plt.show()
#	plt.close()
#	print len(x)#,date
	ano=monthly.index[j][0]
	mes=monthly.index[j][1]
	j+=1
dt=np.array(dt)
global m1
m1=runningMeanFast(m,5)
m2=runningMeanFast(m1,5)
#plt.figure(figsize=(15,10))
#plt.plot(dt,m2,'k',linewidth=1.5)
#plt.xlabel('Time (years)',fontsize=18)
#plt.ylabel('Growth rate m/hr',fontsize=18)
#plt.xticks(fontsize=16)
#plt.yticks(fontsize=16)
#plt.grid()
#plt.savefig(outputdir+'Plots/article/growthrateseries.png')
#plt.show()
#plt.close()
#fig, ax1=plt.subplots(figsize=(12,10))
#ax1.plot(dt,m1,'k')
#plt.plot(dt,m1,'b')
#plt.xlabel('Date',fontsize=15)
#ax1.set_ylabel(r'Growth rate $m/hr$')
#plt.title('Growth rate time series')
#plt.grid()
#plt.show()
#df=pd.DataFrame(data=m1,index=dt)
#df.plot()
#plt.show()
#plt.close()
monthly=df.groupby([df.index.year,df.index.month]).mean()
monthly=np.asarray(monthly)
print 'Exiting Growth Rates' 
#monthly=runningMeanFast(monthly,3)
#meanly=runningMeanFast(meanly,3)
#plt.plot(meanly)
#for i,m in enumerate(meanly):
#	monthly[i]=(monthly[i]+monthly[i-1]+monthly[i-2])/3.
#	meanly[i]=(meanly[i]+meanly[i-1]+meanly[i-2])/3.
#	print meanly[i]
#f,axarr=plt.subplots(3,sharex=True,figsize=(15,12))
#axarr[0].set_title('Serie de MLH $max$ y $min$ ',fontsize=22)
#print len(maxi),len(meses)
#axarr[0].plot(meses,maxi,'b')
#plt.yticks(fontsize=16)
#axarr[0].grid()
#plt.xlabel(u'Año',fontsize=20)
#axarr[0].set_title(r'MLH$_{max}$ time series',fontsize=16)
#axarr[0].set_ylabel(r'MLH max (m)',fontsize=20)
#plt.yticks(fontsize=16)
#ax2=ax1.twin)
#axarr[1].plot(meses,mini,'r')
#	axarr[1].set_yticklabels(mini,size=16)
#axarr[1].set_ylabel(r'MLH min (m)',fontsize=20)
#plt.xticks(fontsize=16)
#plt.yticks(fontsize=16)
#plt.grid()
#plt.show() 
#x=yy
#fig, ax1=plt.subplots(figsize=(12,10))
#ax1.plot(monthly,'k')
#plt.xlabel('Month',fontsize=15)
#ax1.set_ylabel(r'Growth rate $(m/hr)$',fontsize=15)
#ax2=ax1.twinx()
#ax2.plot(meanly,'r--')
#ax2.set_ylabel('Mean MLH',fontsize=15)
#plt.title('MLH Mean-Growth rate',fontsize=17)
#plt.xticks(np.arange(0,12),['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dic'])
#plt.xlim([0,11])
#plt.grid()
#plt.savefig('/home/D1_CEILO/UNAM/PRCL/Results/Plots/article/grwthrate_1.eps')
#plt.show()


