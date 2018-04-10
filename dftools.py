"""
Data-Frame tools module
*********************************

.. toctree::
    :maxdepth: 2

    ut_5tout_6

This is the main toolbox designed to aid main processsing the Mixed-layer height data frames through the use of
the Python Module `Pandas <https://pandas.pydata.org/>`_.

"""
# -*- coding: utf8 -*-
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import pandas as pd
import glob
import os
import sys
import datetime
from ceilotools import *
#from growth_rates import *
#filename='/home/jorge/Documentos/Python/Tesis/Results/201607_10min_db.csv'
#output='/home/jorge/Documentos/Python/Tesis/Results/Plots/'
#df=pd.read_csv(filename,index_col='Fecha y hora')
#df.index=df.index.rename('Fecha y hora')
#df.index=pd.to_datetime(df.index)
#df=df[df > 100]
#Function to reset index of data frame, changing from UT-5 to UT-6 the dates needed.
def ut_5tout_6(df):
    r"""

    Convert times in UTC-5 to UTC-6 and make database time-homogeneus.

    **Parameters**

    **df**: `pandas.dataframe`
        Pandas Data-Frame object containing a datetime index and columns of MLH.

    :rtype: `df` pandas dataframe

    *See Also*

    :ref:`mlhtodf`.

    """
    # Index values
    indice=df.index.values
    for i,dt in enumerate(df.index):
            if ((dt.month==4 and dt.day<=6)):
                    indice[i]=dt-datetime.timedelta(hours=1)
    df.index=indice
    return df
def hourly(df,show,save,name,wstd):
	yerror=None
	hourly=df.groupby(df.index.hour).std()
	tvec=range(1,25)
	hourly=np.asarray(hourly)
	bsicplot(u'Desviación estándar horaria',hourly,tvec,show,save,name,wstd,yerror)
def corrplot(dx,carpeta):
	df=dx['C2']
	odf=dx['Delice']
	minavg=df.groupby([df.index.hour,df.index.minute]).mean()
	total=odf.groupby([odf.index.hour,odf.index.minute]).mean()
	minavg=np.asarray(minavg)
	filtered=np.asarray(total)
	r=np.corrcoef(minavg,filtered)
	r0=np.around(r[0,1],4)
	plt.scatter(minavg,filtered,s=5,c='k')
	plt.xlabel('Raw MH [m]',fontsize=16)
	plt.ylabel('Filtered MH [m]',fontsize=16)
	plt.title('Mean MH daily evolution comparison',fontsize=18)
#	plt.xlim([500,2500])
	plt.text(800,3000,r'$r= '+str(r0)+'$'+'\n$n= '+str(len(minavg))+'$',fontsize=15)
	plt.grid()
	plt.savefig(carpeta+'scatcomparison_2.eps')
	plt.show()
def minutes(df,odf,show,rmean,save,name,wstd,c):
    r"""

    Plot mean diurnal evolution of MLH

    **Parameters**

    **df**: `pandas.dataframe`
        Pandas Data-Frame object containing a datetime index and columns of MLH.
    **odf**: `pandas.dataframe`
        Second Pandas Data-Frame object containing a datetime index and columns of MLH if anomaly is to be plotted.
    **show**: `Boolean`
        True or False if you wish the plot to be shown.
    **rmean**: `Boolean`
        True or False if you wish to see the plot smoothed by our own function of runnin mean :ref:`runningMeanFast`.
    **save**:`Boolean`
        True or False if you wish to save the plot.
    **name**:`str`
        String of saved plot
    **wstd**:`Boolean`
        True or False if intention is to plot standard deviaiton and not mean.
    **c**:`string`
        Color string: choose from `colors <https://matplotlib.org/examples/color/named_colors.html>`_

    :rtype: `df` pandas dataframe

    *See Also*

    :ref:`bsicplot`.

    """
	#print minavg
    if wstd:
    	minavg=df.groupby([df.index.hour,df.index.minute]).std()
    	title=u'Desviación estándar'
    	ylabel=r'$\sigma$ (m)'
    else:
    	minavg=df.groupby([df.index.hour,df.index.minute]).mean()
    	total=odf.groupby([odf.index.hour,odf.index.minute]).mean()
    	anomal=minavg-total
    	#minavg=minavg-total
    	#title=u'Term diurnal evolution (anomaly)'
    	title=u'MH mean diurnal evolution'
    	ylabel=r'MH (m)'
    minarray=np.asarray(minavg)
    if rmean:
    	minarray=runningMeanFast(minarray,4)
    tvec=frange(0,24,float(10)/60.0)
    bsicplot(title,minarray,tvec,show,save,name,ylabel,c)
def bsicplot(titles,y,tvec,show,save,name,ylabel,c):
    r"""

    Basic plot function for a 24-hr plot

    **Parameters**

    **titles**: `string`
        String for title of plot
    **y**: `np.array`
        Array to plot
    **tvec**:`np.array`
        Time-vector.
    **show**: `Boolean`
        True or False if you wish the plot to be shown.
    **rmean**: `Boolean`
        True or False if you wish to see the plot smoothed by our own function of runnin mean :ref:`runningMeanFast`.
    **save**:`Boolean`
        True or False if you wish to save the plot.
    **name**:`str`
        String of saved plot
    **ylabel**:`string`
        Label of y-axis.
    **c**:`string`
        Color string: choose from `colors <https://matplotlib.org/examples/color/named_colors.html>`_

    :rtype: `df` pandas dataframe

    *See Also*

    :ref:`minutes`.

    """
    plt.plot(tvec,y,c,label=name,linewidth=1.5)
    plt.title(titles,fontsize=20)
    plt.xlabel(u'Time (UTC-6)',fontsize=18)
    plt.xticks(np.arange(0,25,2))
    plt.xticks(size=16)
    plt.yticks(size=16)
    plt.ylabel(ylabel,fontsize=18)
    plt.xlim([0,24])
    plt.grid()
    if save:
    	plt.savefig(name)
    if show:
    	plt.show()
    	plt.close()
def bimonthly(df,out):
	i=0
	#print i
	tvec=frange(0,24,float(10)/60.0)
	j=1
	plt.figure(figsize=(15,10))
	c=['b','r','g','c']
	while j<12:

		if j==100:
			ij=12
			mn=2
		else:
			ij=j+2
			mn=2
		newdf=df[(df.index.month==j)|(df.index.month==j+1)]
		j+=mn
		total=newdf.groupby([newdf.index.hour,newdf.index.minute]).mean()
		argu=df.groupby([df.index.hour,df.index.minute]).mean()
	#for date in newdf.index:
	#	print date
		total=np.asarray(total)
		dif=total-np.array(argu)

		dif=runningMeanFast(dif,6)
		plt.plot(tvec,dif)
		#minutes(newdf,df,False,True,False,'bimestral.png',False,'-')
		i+=1
	tot=df.groupby([df.index.hour,df.index.minute]).mean()
	difi=np.asarray(tot)
	#dif=np.diff(difi)
	#plt.plot(tvec,difi,'--')
	plt.grid()
	#minutes(df,df,False,True,False,'b',False,'-')
	plt.xlim([0,24])
	plt.xlabel('Time (UT-6)',fontsize=18)
	plt.ylabel(r'MLH anomaly (m)',fontsize=18)
	#minutes(df,df,False,True,False,'bimestral.png',False,'--')
	plt.grid()
#	legend=plt.legend(['Jan-Feb','Mar-Apr','May-Jun','Jul-Aug','Sep-Oct','Nov-Dec'],loc='upper left',title='Term',fontsize=13)
	legend=plt.legend(['JF','MA','MJ','JA','OS','ND','Annual mean'],loc='upper left',fontsize=14)
	plt.grid()
#	legend.get_title().set_fontsize('14')
	#plt.grid()
	plt.savefig(out)
	plt.show()
	plt.close()

	#bimestre=df.groupby([df.index.hour,df.index.minute,df.index.month])
	#print	bimestre.get_group((0,0,1:2))
def longmaxmin(meses, maximo):
	counter=0
	cdate=meses[counter]
	startyear=2011
	mesesits=['Ene','Feb','Mar','Apr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
	while startyear!=2017:
		lista=[]
		while cdate.year==startyear:
			lista.append(maximo[counter])
			counter+=1
			cdate=meses[counter]
			if cdate == meses[-1]:
				break

		lista=np.array(lista)
		valmin=min(lista)
		value=max(lista)
		index=np.where(lista==value)
		indicit=np.where(lista==valmin)
		startyear+=1
def yearly(df,filtered,output,name):
	yr1=df.groupby([df.index.hour,df.index.minute,df.index.year]).mean()
	yrly=df.groupby([df.index.hour,df.index.minute,df.index.year]).mean().unstack()
#	print yrly
	columns=yrly.columns
	tvec=frange(0,24,10.0/60.0)
	index=range(2008,2016)
	figu=plt.figure()
	ax= figu.add_subplot(1,1,1)
	for i,j in enumerate(index):
		if filtered:
			if j==2008 or j==2010:# or j==2012 or j==2009:
				continue
		y=np.asarray(yrly[columns[i]])
		y=runningMeanFast(y,3)
		ax.plot(tvec,y,label=str(index[i]))
	plt.xticks(np.arange(0,24,2))

	plt.grid()
	ax=customax(ax,'Promedios anuales cada 10 minutos','lower right')
	plt.show()
	plt.savefig(output+name+'.png')
	#plt.show()
	plt.close()
def customax(ax,titles,legendloc):
	plt.legend(loc=legendloc)
	plt.title(titles)
	plt.xlim([0, 24])
	plt.xlabel('Horas')
	plt.ylabel('Altura de capa de mezcla (m)')
#minutes(df,True,True,True,output+'10minavg_rmean_filtered.png',False)
#yearly(df,True)
#bimonthly(df)
def pullclouds(df,cloudfile):
	cloudf=pd.read_csv(cloudfile)
	indx=cloudf.columns[1]
	dfsnubs=df.copy()
	cloudate=pd.to_datetime(cloudf[indx])
	cloudate=cloudate.tolist()
	for i,j in enumerate(cloudate):

		dfsnubs[j]=np.nan
	return dfsnubs
def cleanday(df):
	start=datetime.datetime(2008,1,1,12,0)
	end=datetime.datetime(2008,1,1,18,50)
	final=datetime.datetime(2016,5,1,0,0)
	newdates=[]
	index=0
	df=pd.DataFrame(data=df,index=df.index)
	df.index=pd.to_datetime(df.index)
	horas=[]
	maxi=[]
	mini=[]
	imin=[]
	imax=[]
	#print type(df.index)
	while start != final:
		startd=df.index.searchsorted(start)
		endd=df.index.searchsorted(end)
		newdf=df[startd:endd]
		if len(newdf.index) > (4*6):
			newdates.append(newdf.index[0])
			nwdf=newdf.groupby([newdf.index.hour]).mean()
			maxi.append(nwdf.max())
			mini.append(nwdf.min())
			imax.append(nwdf.idxmax())
			imin.append(nwdf.idxmin())
		index+=len(newdf.index)
		start=start+datetime.timedelta(days=1)
		end=end+datetime.timedelta(days=1)
	#df=df.groupby([df.index.hour,df.ixndex.month,df.index.year]).mean()
	#df=df.groupby([df.index.day,df.index.month,df.index.year]).max().unstack()
	#print df
	newdates=np.array(newdates)
	maxis=np.array(maxi)
	plt.plot(newdates,maxis)
	plt.show()
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
	fmlh=mlh
	imin=np.argmin(mlh)
	imax=np.argmax(mlh)
	if imin < imax:

		dates=dates[imin:imax]
		mlh=mlh[imin:imax]
	date0=dates
	xdate=[]
	for dt in dates:
		m=dt.minute
		h=dt.hour
		add=m/60.
		xdate.append(h+add)
	#print np.polyfit(xdate,mlh,1)
	r0= np.corrcoef(xdate, mlh)[0,1]
	r2= r0**2.
	date0=xdate
	stindex=len(mlh)
	r=r0
	x=True
	while x:
		back=mlh[:-1]
		front=mlh[1:]
		bdt=xdate[:-1]
		fdt=xdate[1:]
		backr=np.corrcoef(bdt,back)[0,1]
		fr=np.corrcoef(fdt,front)[0,1]
		if backr > r and backr> fr:
			xdate=xdate[:-1]
			mlh=mlh[:-1]
		elif fr > r and fr > backr:
			xdate=xdate[1:]
			mlh=mlh[1:]
		else:
			x=False
		r=np.corrcoef(xdate,mlh)[0,1]
		if len(mlh)<=20:
			x=False
#		print 'entering while'
		r0=r
#	print r
	maxindex=stindex-len(mlh)
	m,b=np.polyfit(xdate,mlh,1)
	xdate=np.array(xdate)
	nmlh=xdate*m+b
	#plt.figure(2)
	#plt.plot(date0,fmlh,label='original')
	#plt.plot(xdate,nmlh,label='model')
	#plt.legend()
	#plt.grid()
	#plt.show()
	#plt.close()
	return m,maxindex

def grwthrate(dates,mlh):
	onemax=np.argmax(np.diff(mlh))
	nmlh=[]
	nmlh2=[]
	dat=[]
	dat2=[]
	meses=[]
	#plt.figure(2)
	#plt.plot(dates,mlh)
	#plt.show()
	mesesito=dates[0].month
	meses.append(mesesito)
	for i,dt in enumerate(dates):
		if dt.hour > 6.0 and dt.hour < 15.0:
#			print dt.minute
			nmlh.append(mlh[i])
			dat.append(dates[i])
			if dt.hour < 11.5:
				nmlh2.append(mlh[i])
				dat2.append(dates[i])
	dindex=np.where(mlh==nmlh[0])
	indice=minimum(nmlh2,dat2)
	indice=np.where(nmlh==indice)

	indice=indice[0][0]
	#print dat2[indice],nmlh2[indice]

	nlmh=nmlh[indice:]
#	print nlmh
	dat=dat[indice:]
	m,maxindex=growth(dat,nlmh)
	return m,dindex+indice,maxindex
def mlhmax(df,c,f,axarr,lab,name):
    df.index=pd.to_datetime(df.index)
    #print df.tail
    #dx=df.truncate(after='2016-05-30 00:00:00',before='2011-01-01 00:00:00')
    #dx=df[(df.index.month<6)or(df.index.year<2017)]
    #	print dx.head, dx.tail
    dx=df
    xy=df.groupby([df.index.year,df.index.month,df.index.day,df.index.hour]).mean()
    xyz=xy.unstack()
    lista=[]
    data=df
    mes=xy.index[0][1]
    year=xy.index[0][0]
    day=xy.index[0][2]
    list2=[]
    maxday=[]
    minday=[]
    listmin=[]
    dates=[]
    maxi=[]
    dates=[]
    mini=[]
    meses=[]
    for i,j in enumerate(xy.index):
        if xy.index[i][2]!=day:
            if len(list2)>2:
                try:
                	maxday.append(np.nanmax(list2))
                except:
                	pass
            if len(listmin)>2:
                try:
                    minday.append(min(listmin))
                except:
                    print('Vacio')
                if xy.index[i][1]!= mes:
    		#print j
                    maxi.append(np.mean(maxday))
                    mini.append(np.mean(minday))
                    maxday=[]
                    minday=[]
                    m=datetime.datetime(xy.index[i-1][0],xy.index[i-1][1],1)

                    meses.append(m)
                    mes=xy.index[i][1]
                    listmin=[]
                    list2=[]
                    dates.append(datetime.datetime(xy.index[i-1][0],xy.index[i-1][1],xy.index[i-1][2]))
                    day=xy.index[i][2]
        if xy.index[i][3] >11 and xy.index[i][3]<19:
        	list2.append(xy.loc[j])
        elif xy.index[i][3] <10 and xy.index[i][3]>2:
        	listmin.append(xy.loc[j])
        if xy.index[i][0]==2016 and xy.index[i][1]==5:
        	break

    maxi=runningMeanFast(maxi,4)
    #	maxi=runningMeanFast(maxi,3)
    mini=runningMeanFast(mini,5)
    #	mini=runningMeanFast(mini,3)
    monthly=data.groupby([data.index.year,data.index.month,data.index.hour,data.index.minute]).mean()
    meanly=data.groupby([data.index.year,data.index.month]).mean()
    meanly=dx.groupby([dx.index.year,dx.index.month]).mean()
    #	print meanly
    meanly=np.asarray(meanly)
    #	meanly=runningMeanFast(meanly,4)
    meanly=runningMeanFast(meanly,3)
    ano=monthly.index[0][0]
    mes=monthly.index[0][1]
    fdatey=2017
    fdatem=5
    j=0
    #	print ano, mes
    #print meses, maxi
    #longmaxmin(meses,maxi)
    m=[]
    dt=[]
    while not(ano == fdatey and mes >= fdatem):

    	date=[datetime.datetime(monthly.index[j][0],monthly.index[j][1],1,monthly.index[j][2],monthly.index[j][3])]
    	x=np.array(monthly.loc[monthly.index[j]])
    	while mes  == monthly.index[j][1]:
    		mes=monthly.index[j][1]
    		date.append(datetime.datetime(monthly.index[j][0],monthly.index[j][1],1,monthly.index[j][2],monthly.index[j][3]))
    		x=np.append(x,monthly.loc[monthly.index[j]])
    		j+=1
    #	x=yy
    #		print x
    	m1,minimo,maxis=grwthrate(date,x)
    #		print m1
    	m.append(m1)
    	dt.append(datetime.datetime(date[0].year,date[0].month,1))
    	 #	plt.plot(date,x)
    	ano=monthly.index[j][0]
    	mes=monthly.index[j][1]
    	j+=1
    dt=np.array(dt)
    #global m1
    #m2=m
    m1=runningMeanFast(m,4)
    m2=runningMeanFast(m1,3)
    #longmaxmin(meses,m2)
    dates,areas=blhanomaly(df,'name')
    axarr[0].set_title('Time series ',fontsize=24)

    axarr[0].plot(meses,maxi,c,label=lab,linewidth=1.5)
    #label = axarr[0].yaxis.get_major_ticks(.label
    labels= axarr[0].yaxis.get_major_ticks()#.set_fontsize(16)
    for label in labels:
    	label=label.label
    	label.set_fontsize(16)
    #	axarr[0].set_yticklabels(size=16)
    axarr[0].set_ylabel('MH max [m]',fontsize=19)
    axarr[0].grid()
    #	plt.show()
    #axarr[0].set_title(r'MLH$_{max}$ time series',fontsize=16)
    #	axarr[1].set_ylabel(r'MH min (m)',fontsize=20)
    #	axarr[1].plot(meses,mini,c,label=lab,linewidth=1.5)
    #label = axarr[0].yaxis.get_major_ticks(.label
    #	labels= axarr[1].yaxis.get_major_ticks()#.set_fontsize(16)
    #	for label in labels:
    #		label=label.label
    #		label.set_fontsize(16)
    #	axarr[0].set_yticklabels(size=16)
    axarr[1].plot(dt,m2,c,label=lab,linewidth=1.5)
    axarr[1].set_ylabel(r'Growth rate (m/h)',fontsize=20)
    labels= axarr[1].yaxis.get_major_ticks()#.set_fontsize(16)
    for label in labels:
    	label=label.label
    	label.set_fontsize(16)
    axarr[1].grid()
    #	axarr[2].plot(meses,meanly,c,label=lab,linewidth=1.5)
    #	axarr[2].set_ylabel(r'MH mean [m]',fontsize=20)
    #	axarr[2].grid()
    #	labels= axarr[2].yaxis.get_major_ticks()#.set_fontsize(16)
    #	for label in labels:
    #		label=label.label
    #		label.set_fontsize(16)
    #	axarr[2].grid()
    axarr[2].plot(dates,areas,c,label=lab,linewidth=1.5)
    axarr[2].set_ylabel(r'Anomaly Area (-)',fontsize=20)
    axarr[2].grid()
    labels= axarr[2].yaxis.get_major_ticks()#.set_fontsize(16)
    for label in labels:
    	label=label.label
    	label.set_fontsize(16)
    axarr[2].grid()

    #axarr[1].set_title(r'MLH$_{min}$ series',fontsize	axarr[1].set_ylabel(r'MLH$_{min}$ (m)',fontsize=14)
    #bsicplot(u'Serie de tiempo de $MLH_{max}$',maxi,meses,False,False,name,'Altura de capa de mezcla')
    #plt.plot(dates,maxi)
    #plt.plot(dates,mini)
    #plt.show()
    plt.savefig(name)
    plt.show()#

    #xy.plot()
def blhanomaly(df,name):
    prom=df.mean()
    start=datetime.datetime(2008,12,1,1,0)
    df=df['2011':]
    total=df.groupby([df.index.hour,df.index.minute]).mean()
    year=2011
    mes=1
    tvec=frange(0,24,10.0/60.0)
    areas=[]
    dates=[]
    while not (year==2017 and mes == 5):
        newdf=df[(df.index.month==mes)&(df.index.year==year)]
        #print mes, year
        #print len(newdf)
        media=newdf.groupby([newdf.index.hour,newdf.index.minute]).mean()
        anomal=media-total
        anomal=anomal.dropna()
        #print np.array(anomal)
        #print np.trapz(np.array(anomal),dx=10.0/60.0)
        areas.append(np.trapz(anomal,dx=10.0/60.0))
        dates.append(datetime.datetime(year,mes,1))
        mes+=1
        if mes>12:
        	year+=1
        	mes=1
    bd=runningMeanFast(areas,3)
    bd=runningMeanFast(bd,3)
    #print areas
    return dates,bd
	#plt.plot(dates,bd)
	#plt.grid()
	#bd.plot()
# 	#plt.show()
# 	x=yy
# 	df[(df.index.month==j)|(df.index.month==j+1)]
# 	mes=df.index[0].month
# 	fechas=[df.index[0]]
# 	for date in df.index:
# 		if date.month != mes:
# 			fechas.append(date)
# 			mes=date.month
# 	bd=np.array(bd)
# #	for i,b in enumerate(bd):
# 		#bd[i]=bd[i]-prom
# 	bd=runningMeanFast(bd,3)
# #	bd=runningMeanFast(bd,3)
# 	print len(fechas), len(bd)
# 	plt.plot(bd,'k')
# #	plt.xlabel('Year',fontsize=13)
# #	plt.title('Time series')
# #	plt.ylabel('Mean MLH')
# 	plt.grid()
# #	plt.show()
# #	plt.savefig(name)
# #	x=yy
# 	plt.xticks(np.arange(0,12),['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dic'])
# 	plt.xlim([0,11])
# 	plt.xlabel('Month')
# 	plt.ylabel('MLH  (m)')
# 	plt.title('Time Series Anomaly')
# #	plt.grid()
# #	plt.show()
# 	plt.savefig(name)

def monthtable(df):
	total=df.groupby([df.index.hour,df.index.month]).mean().unstack()
	df=pd.DataFrame(total)
	df=np.around(df,0)
	df.columns=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
	df.index.name='Hora/Mes'
	df.to_csv('tablamensual.txt',sep='\t')
