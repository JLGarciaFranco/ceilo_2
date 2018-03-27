#!/usr/bin/python/env
# -*- coding: utf8 -*-
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt 
import os,glob
radiosonde='/home/D1_CEILO/UNAM/PRCL/Radiosonde/'
manana=radiosonde+'12Z.csv'
tarde=radiosonde+'00Z.csv'
ceilo='/home/D1_CEILO/UNAM/PRCL/Results/final_db.csv'
dfam=pd.read_csv(manana,index_col='Fecha y hora')
dffm=pd.read_csv(tarde,index_col='Fecha y hora')
dfam.index=pd.to_datetime(dfam.index)
dffm.index=pd.to_datetime(dffm.index)
dfceilo=pd.read_csv(ceilo,index_col='Fecha y hora')
dfceilo.index=pd.to_datetime(dfceilo.index)
df=dfceilo['C2-F2']
df=df.dropna()
ceilomlham=[]
ceilomlhfm=[]
ceilotot=[]
radioam=[]
radiofm=[]
radiotot=[]
for indice in dfam.index:
	if indice in dfceilo.index:
		radioam.append(dfam.loc[indice])
		date=indice
		startd=indice-datetime.timedelta(minutes=30)	
		endd=indice+datetime.timedelta(minutes=30)
		st=df.index.searchsorted(startd)
		et=df.index.searchsorted(endd)
		dfm=df[st:et]
		ceilomlham.append(dfm.mean())
		ceilotot.append(dfm.mean())
		radiotot.append(dfm.mean())
ceilomlham=np.asarray(ceilomlham).reshape((len(ceilomlham),))
radioam=np.asarray(radioam).reshape((len(radioam),))
newceilo=[]
newradio=[]
for i,j in enumerate(ceilomlham): 
	if np.isnan(j):
		print 'nan'
	else:
		newceilo.append(j)
		newradio.append(radioam[i])
r1=np.corrcoef(newceilo,newradio)
r0=r1[1,0]
print r0
print np.mean(newceilo), np.mean(newradio)
#print ceilomlham.ma.mean(), radioam.mean()
texstr=r'$r Pearson = $'+str(r0)
#plt.figure(figsize=(12,9))
fig,ax=plt.subplots(1)
props=dict(boxstyle='round',facecolor='wheat', alpha=0.5)
ax.scatter(newceilo,newradio)
plt.text(2000,750,texstr,transform=ax.transAxes,fontsize=13,verticalalignment='top',bbox=props)
plt.xlabel('Radiosondeos (m)',fontsize=14)
plt.ylabel(u'Ceilómetro-Gradiente (m)',fontsize=14)
plt.xlim([0,2500])
plt.ylim([0,4000])
plt.grid()
plt.show()

for indice in dffm.index:
        if indice in df.index:
                radiofm.append(dffm.loc[indice])
                date=indice
                startd=indice-datetime.timedelta(minutes=30)
                endd=indice+datetime.timedelta(minutes=30)
                st=df.index.searchsorted(startd)
                et=df.index.searchsorted(endd)
                dfm=df[st:et]
                ceilomlhfm.append(dfm.mean())
                ceilotot.append(dfm.mean())
                radiotot.append(dfm.mean())
ceilomlhfm=np.asarray(ceilomlhfm).reshape((len(ceilomlhfm),))
radiofm=np.asarray(radiofm).reshape((len(radiofm),))
r1=np.corrcoef(ceilomlhfm,radiofm)
r0=r1[1,0]
print r0
print np.mean(ceilomlhfm), np.mean(radiofm)
print len(ceilomlhfm)
#print ceilomlham.ma.mean(), radioam.mean()
texstr=r'$r Pearson = $'+str(r0)
#plt.figure(figsize=(12,9))
fig,ax=plt.subplots(1)
props=dict(boxstyle='round',facecolor='wheat', alpha=0.5)
ax.scatter(radiofm,ceilomlhfm)
plt.xlabel('Radiosondeos (m)',fontsize=14)
plt.ylabel(u'Ceilómetro-Gradiente (m)',fontsize=14)
plt.xlim([0,4000])
plt.ylim([0,4000])
plt.text(500,500,texstr,transform=ax.transAxes,fontsize=13)
plt.grid()
plt.show()

plt.close()
plt.boxplot(radiofm,label='Radiosondeo')
plt.boxplot(ceilomlhfm,label=u'Ceilómetro')
plt.ylabebl('Altura de capa de mezcla (m)')
plt.title(u'Comparación estadística')
plt.legend()
plt.grid()
plt.show()
