"""
Ceilo tools module
*********************************
.. toctree::
   :maxdepth: 2

This is the main toolbox designed to aid main processsing by reading and writing to files and processing data.

"""

import numpy as np
import math
import os
from wavelets import *
import datetime
###########################################################################################################
def histogram(x,N):
	ntot=len(x)
	xmax=np.max(x)
	xmin=np.min(x)
	dx=float(xmax-xmin)/N
	bins=np.arange(N)*dx+xmin
	hist=[]
	for unbin in bins:
		index=np.where(np.logical_and(x >= unbin , x < unbin+dx))[0]
		hist.append(float(len(index))/ntot)
	return bins,np.array(hist)
###########################################################################################################
def frange(start,stop,step):
	vec=np.zeros((stop-start)/step)
	num=start
	for i,t in enumerate(vec):
		vec[i]=num
		num=num+step
	return vec
###########################################################################################################
def roundt(minutos,segundos):
	dif=minutos-10
	count=0
	minutseg=minutos+(float(segundos)/60.0)
	while dif > 0:
		dif=dif-10
		count=count+1
	if minutseg >=9 + (count*10):
		minutos=(count+1)*10
	else:
		minutos=count*10
	return minutos
###########################################################################################################
def writemlh(outputfile,horas,mlhs,station):
	r"""

	Write of mixed-layer file to txt file, using standard heading. For instance:

	**Parameters**

	**outputfile**: `string`
	    Output filename. Usually a 'txt'.
	**horas** : `numpy.narray-float`
	    Time vector as hourly decimals. 0., 0.166, ..., 23.83.
	**mlhs** : `numpy.narray-float`
	    Mixed-layer heights vector.
	**station*: `string`
		Station string

	:rtype: None

	*See Also*

	:ref:`secondary`.

	"""
	fout=open(outputfile,'w')
	fout.write("Ceilometer Vaisala CL31. 10 min averages in "+station+"\n")
	fout.write("MLH from Gradient method. Espectroscopia y Percepcion Remota, CCA-UNAM\n")
	fout.write("Version: 201801  "  )
	fout.write("http://www.atmosfera.unam.mx/espectroscopia/ceilo/\n")
	fout.write("Decimal.hour  MLH(m)\n")
	for i,unamlh in enumerate(mlhs):
		timeh=horas[i]
		fout.write("%.3f         %i \n" % (timeh,unamlh))
	fout.close()
###########################################################################################################
def writematrix(outputfile, matrix,zeta,hour_vec,station,date,runv):
	r"""

	Write of backscattering matrix to txt file, using standard heading. For instance:

	**Parameters**

	**outputfile**: `string`
	    Output filename. Usually a 'txt'.
	**matrix**: `numpy.nadarray`
	    Backscattering matrix mxn where m is the length of time vector, or number of decimal hours in the particular day and n is the length of height vector, usually 500 (10-5000 m every 10 m).
	**hour_vec** : `numpy.narray-float`
	    Time vector as hourly decimals. 0., 0.166, ..., 23.83.
	**date** : `string`
	    Date of measurement (typically %Y%m%d)
	**station*: `string`
		Station string

	:rtype: None

	*See Also*

	:ref:`writemlh`

	"""
	fout=open(outputfile,'w')
	fout.write("Datos de retrodispersion en "+ station + date+"\n" )
	fout.write("Ceilometro Vaisela CL31 \n")
	fout.write("Version del codigo: 201605\n"  )
	fout.write("http://www.atmosfera.unam.mx/espectroscopia/ceilo/\n")
	fout.write("Contacto: Espectroscopia y Percepcion Remota, CCA-UNAM\n")
	fout.write("Corrida de nombre "+str(runv)+'\n' )
	zstring="niveles:"
	for zval in zeta:
		zstring=zstring+" %i" % (zval)
	tstring ="horas: "
	for tval in hour_vec:
		tstring=tstring+" %.3f" % (tval)
	fout.write(zstring + "\n")
	fout.write(tstring +"\n")
	for i,vec in enumerate(matrix):
		for j,val in enumerate(vec):

			fout.write(str(val)+" ")
		fout.write("\n")
	fout.close()


#Funcion para calcular promedios horarios para un dia, o para un archivo.
#MLHAVERAGE.
def onedayavg(filename,horas):
	data= np.genfromtxt(filename,skip_header=4)
	time = data[:,0]
	mlh = data[:,1]
	indices=[]
	#Definicion de tiempo minimo, leido del archivo.
	tmin=math.floor(min(time))
	tmax=tmin+1
	#Definicion de tiempo maximo en el archivo.
	maximo=max(time)
	promedios=[]
	files= filename.split('/')[-1]
	promedios.append(files[0:8])
	for i,h in enumerate(horas):
		if tmin>horas[i]:
			promedios.append('')

	for i,tt in enumerate(time):

		if tt>=tmin and tt <tmax:
			indices.append(mlh[i])
			if tt == maximo and len(indices) !=0:
				avg=sum(indices)/len(indices)
				promedios.append(avg)

		else :
			if len(indices) !=0:
				avg=sum(indices)/len(indices)
			else:
				avg=' '
			promedios.append(avg)
			indices = []
			tmin= tmin+1
			tmax= tmax+1
			indices.append(mlh[i])



	return promedios
def readmlh(filename):
    r"""

    Write of backscattering matrix to txt file, using standard heading. For instance:

    **Parameters**

    **filename**:`string`
        Input filename. Usually a 'txt'.

    :rtype:time-array, mlh-array:  time and MLH vector.

    *See Also*

    :meth:`writemlh` , :meth:`readmatrixfile`

    """
    profil=np.genfromtxt(filename,skip_header=4)
    return profil[:,0],profil[:,1]
###########################################################################################################
def readmatrixfile(filename):
    r"""

    Write of backscattering matrix to txt file, using standard heading. For instance:

    **Parameters**

    **filename**: `string`
        Input filename. Usually a 'txt'.

    :rtype: z,tarr,allprf height and time vector and backscattering matrix.

    *See Also*

    :meth:`writemlh`

    """
    m=6
    y=8
    f = open(filename, 'r')
    for i in range(m):
        f.readline()

    z=np.array(f.readline().split()[1:],dtype=float)
    tarr=np.array(f.readline().split()[1:],dtype=float)
    allprf=np.genfromtxt(filename,skip_header=y)
    #	print tarr
    #	print allprf.shape
    return [z,tarr,allprf]
###########################################################################################################
def insertmatrix(filename,t):
	data= np.genfromtxt(filename,skip_header=4)
	time = data[:,0]
	mlh = data[:,1]
	height=0
	for i,tt in enumerate(time):
		if tt==t:

			height=mlh[i]
			break

	return height
###########################################################################################################
def runningMeanFast(x, N):
	r"""

	Running mean of array x over a window of size N.

	**Parameters**

	**x**: `np.array`
	    Numpy array, usually 1D, to average over a moving or running mean.
	**N**: `numpy.nadarray`
	    Size of moving average window.

	:rtype: `np.array` averaged with running mean.

    .. note::
        This script makes use of numpy.convolve.

	"""
	ravg=np.convolve(x, np.ones((N,))/N,mode='valid')[(N-1):]
	size=len(ravg)
	dif=len(x)-len(ravg)
	apendix=np.zeros(dif)
	counter=0
	for i,j in enumerate(apendix):
		if i == 0:
			apendix[i]=x[i]
		elif i == 1:
			apendix[i]=np.sum(x[i-counter:i+1])/2.0
		else:
			apendix[i]=np.sum(x[i-counter:i+1])/float(i+1)
		counter+=1
		#apendix[i]=np.sum(x[i-2:i+1])/3.0
	ravg=np.insert(ravg,0,apendix)
	#print len(ravg),len(x)
	#print ravg
	return ravg
#USOS EN CEILOV
def writenumofprof(outputfile,numofprof,t, estacion,date):
	r"""

	Write number of backscattering profiles used for every 10-min averaged window.

	**Parameters**

	**outputfile**: `string`
	    Output filename. Usually a 'txt'.
	**numofprof**: `int`
	    Number of profiles used for average
	**t** : `numpy.narray-float`
	    Time vector as hourly decimals. 0., 0.166, ..., 23.83.
	**date** : `string`
	    Date of measurement (typically %Y%m%d)
	**estacion*: `string`
		Station string

	:rtype: None

	*See Also*

    :meth:`writematrix`

	"""
	fout=open(outputfile,'w')
	fout.write("Datos de perfiles promediados "+ estacion + date[1:-6]+"\n" )
	fout.write("Ceilometro Vaisala CL31 \n")
	fout.write("Version del codigo: 2016 05 \n"  )
	fout.write("http://www.atmosfera.unam.mx/espectroscopia/ceilo/\n")
	fout.write("Contacto: Espectroscopia y Percepcion Remota, CCA-UNAM\n")
	tstring ="horas: "
	for tval in t:
		tstring=tstring+" %.3f" % (tval)
	fout.write(tstring +"\n")
	for i,prof in enumerate(numofprof):
		timeh=t[i]
		fout.write("%.3f         %i \n" % (timeh,prof))
	fout.close()
###########################################################################################################
def writeavgmatrix(outputfile,tvec,estacion,matrix,runv,averages):
	fout=open(outputfile,'w')
	fout.write('Matriz de datos diarios a promediar' +'\n')
	fout.write('Ceilometro Vaisala CL31 '+estacion+'\n')
	fout.write('Corrida correspondiente a '+str(runv)+'\n')
	tstring='Tiempo (horas):'
	avg=''
	for h,t in enumerate(tvec):
		tstring=tstring+" %.3f" % (t)
		avg=avg+str(averages[h])+' '
	fout.write(tstring + "\n")
	flistsize=matrix.shape
	tvec=flistsize[0]
	fvec=flistsize[1]
	for i in range(fvec):
		for j in range(tvec):
			point=matrix[j,i]
			fout.write(str(point)+' ')
		fout.write('\n')
	fout.write(avg+'\n')
	fout.close()
###########################################################################################################
#Usados en Avgmlh REDONDEANDO.
def insrtmatrxrnd(filename,t,trthval):
	data= np.genfromtxt(filename,skip_header=4)
	time = data[:,0]
	mlh = data[:,1]
	height=0
	for i,tt in enumerate(time):
		if tt > 23.3:
			base=2.0/6.0
		else:
			base=1.0/6.0
		if myround(tt,base)==t:
			if trthval is not False and int(mlh[i])<=60:
				height=0
			else:
				height=mlh[i]
			break
	return height
###########################################################################################################
def addtovecrnd(filename,tvec):
	data= np.genfromtxt(filename,skip_header=4)
	time = data[:,0]
	mlh = data[:,1]
	for i,tt in enumerate(time):
		if tt > 23.3:
			base=2.0/6.0
		else:
			base=1.0/6.0
		if myround(tt,base) not in tvec:
	 		tvec.append(myround(tt,base))

	return tvec
###########################################################################################################
def myround(x, base):
    return base * round(float(x) / base)
def ipmthd(vec,lowlm,z):
	ipm=np.diff(vec)
	newmlh=np.argmin(ipm)
	mlh=z[newmlh+lowlm]
	return mlh
def algmlh(allprf,method,mlh,i,z,tarr,t,uplim):
	r"""

	Algorithms used for Mixed-layer Height determination.This script computes the mlh through an iterative approach and calls the relevant method.

    A combined approach, named C2, due to the fact that it was the second version of a Combined algorithm uses both the gradient method and the wavelet method to find the boundary layer top. This was the algorithm used in :cite:`jlgf2018`.

	**Parameters**

	**allprf**: `np.nadarray`
	    backscattering matrix
    **method**: `string`
	    String calling a MLH determination method, either of the following strings are accepted: 'WT', 'Gradient', 'IPM', 'C2'.
	**tarr** : `np.array`
	    Time-array, usually decimal hours.
	**mlh** : `numpy.nadarray`
	    Mixed-layer height array, usually len(mlh)=144.
    **i** : `int`
  	   Integer of current time-step. Ranging from 0-143.
	**z** : `np.array`
		Height-array usually length 500, start=10, end=5000, t_step=10 [m]
	**t** : `numpy.narray-float`
	    Time float of this specific computation.
	**uplim** : `string`
	    Upper-limit of maximum MLH possible.

	:rtype: mlh: float

    .. note::
    	**See Also functions to estimate and write mlh**

        :meth:`writemlh`
        :meth:`ipf`
        :meth:`wavelets`

	"""
	jk=i
	lowlim=20
	uplim=uplim
#	if t <8. and t >4.:
#		uplim=90
#	elif t<=4. or (t>=21. and t<=24.):
#		uplim=120
#	elif (t>=8. and t<12.) or (t>18. and t<21.):
#		uplim=140
#	elif (t>=12. and t<= 14.):
#		uplim=150
#	else:
#		uplim=200
	if len(z) > 255:
#		uplm=2*uplim
		#print uplim, lowlim,i
		lowlm=lowlim
		a1=2
		a2=10
		fi=a2
		nn=1
		try:
			vec=allprf[lowlim+1:uplim+1,jk]-allprf[lowlim:uplim,jk]
		except IndexError:
			return
	elif len(z) <=250:
		lowlm=int(lowlim/2.)
		vec=allprf[lowlm+1:uplim+1,jk]-allprf[lowlm:uplim,jk]
		a1=1
		a2=20
		fi=5
		nn=2
	if method == 'Gradient' or method == 'Composite 1' or method =='C2':
		imin=np.argmin(vec)
		mlh[jk]=z[imin+(lowlm)]
		#if method=='C2':
		#	print t,mlh[jk]
	elif method == 'Ipm':
		mlh[jk]=ipmthd(vec,lowlm,z)
	elif method == 'WT':
		a=120/a1

		bot,mlh[jk],top=haarcovtransfm(allprf,z,jk,'Auto',fi,t,uplim*10*nn,lowlim*10)
	if method == 'Composite 1':
		if mlh[jk]<=120 or (jk>1 and mlh[jk] - mlh[jk-1] > 1000) :
			ipm=ipmthd(vec,lowlm,z)
			if ipm<=120 or (jk>1 and ipm - mlh[jk-1] > 700):
				#print '!!!! Valor anomalo en la hora', tarr[jk]
				#print 'Gradiente =', mlh[jk]
				#print 'Ipm = ', ipm
				a=120/a1
				b=range(100,4000,a2)
				newmlh=haarcovtransfm(allprf,z,jk,a,b,fi)
				bottom=120
				low=100
				while newmlh<= bottom:
						low=low+fi
						bottom=low
						b=range(low,4000,a2)
						newmlh=haarcovtransfm(allprf,z,jk,a,b,fi)
						if bottom >= 1000:
							break
				if mlh[jk] >= 120:
					mlh[jk]=np.sum(ipm+newmlh+mlh[jk])/3.
				elif ipm - mlh[jk-1] < 1300:
					mlh[jk]=np.sum(ipm+newmlh)/2.
				else:
					mlh[jk]=newmlh

				#print 'WT iterative =', newmlh
			elif mlh[jk]>120:
				mlh[jk]=(ipm+mlh[jk])/2.

			#print 'Anterior, Final ',mlh[jk-1], mlh[jk]
	elif method == 'C2':
		#print mlh[jk]
		if mlh[jk]<=(lowlim*10+50) or (jk>1 and mlh[jk] - mlh[jk-1] > 200):
			a=120/a1
			bot,newmlh,top=haarcovtransfm(allprf,z,jk,'Auto',fi,t,uplim*10*nn,lowlim*10)
		#	print t, mlh[jk],newmlh
			if newmlh -mlh[jk-1] > 200:
				upper=uplim*10*nn
				while upper - newmlh < 500. and upper > 2500.:
					upper=upper-100
					bot,newmlh,top=haarcovtransfm(allprf,z,jk,'Auto',fi,t,upper,lowlim*10)
					#print newmlh
			if mlh[jk]>(lowlim*10+50) or newmlh<=(lowlim*10+50):
				mlh[jk]=(newmlh+mlh[jk])/2.
			else:
				mlh[jk]=newmlh

		#	print 'MLH FINAL  :::',mlh[jk]
			#print 'Anterior, Final ',mlh[jk-1], mlh[jk]
	#print 'FINAL', mlh[jk]
	return mlh[jk]
def cloudfilter(allprf,tarr,z,datestring):
	r"""
	Cloud filter
	--------------

	This function computes the cloud filter equations described in [Teschke (2008),Garcia-Franco (2017), Garcia-Franco et.al. (2018)]



	**Parameters**

	**allprf**: `np.nadarray`
	    backscattering matrix
	**tarr** : `np.array`
	    Time-array, usually decimal hours.
	**z** : `np.array`
		Height-array usually length 500, start=10, end=5000, t_step=10 [m]
	**datestring** : `string`
		String for date, typically %Y%m%d, e.g., 20160305

	:rtype: datetimearray, flag vector: temps returns all datetimes where cloud or precipitation
	has been found, flag vector is a numpy array with the dimensions of tarr where clouds are depicted
	as 1 and clear-sky conditions as 0.


	**Statistical filter**

	.. math:: \beta_\sigma (z,t)=B(z,t)\sigma(t)
	.. math:: \mu=\frac{1}{N_zN_t}\sum_z\sum_t\beta_\sigma(z,t)
	.. math:: \sum=\frac{1}{N_zN_t-1}\sum_z\sum_t[\beta_\sigma(z,t)-\mu]^2.
	.. math:: B_N=\mu+3\sqrt{\sum}

	* :math:`B(z,t)` Backscattering matrix
	* :math:`\sigma(t)` Variance over time $t$.
	* :math:`\mu` Global mean of \beta_\sigma(z,t)
	* :math:`\sum` Global variance of \beta_\sigma(z,t)
	* :math:`z_{max}` Maximum integration level [m]
	* :math:`B_N` Threshold for determining cloud or no cloud, function of both global mean and variance.

	`B_N` defines the threshold value used for determining whether or not a profile at time `t` presents
	cloud and precipiation or not. If B(z,t)>B_N then cloud and precipitation are present. Else, clear-sky conditions
	are considered.
	"""
	thrs=1750.0
	day=datestring
	dia=int(day[6:8])
	year=int(day[0:4])
	mes=int(day[4:6])
	zi=np.where(z==200.)
	zi=zi[0]
	zmax=np.where(z==4000.)
	zmax=zmax[0]
	#print zi,zmax
	a=allprf[zi:zmax,:]
	nbs=[]
	tmps=[]
	sigma_t=np.sigma(tarr)
	count=len(tarr)*len(z[zi:zmax])
	sumi=0
	for i,t in enumerate(tarr):

		for j,z1 in enumerate(z[zi:zmax]):
			try:
				sumi=sumi+a[j+zi,i]
			except IndexError:
	#			print fl
				continue
	mu=sumi/count
	deviat=0
	for i,t in enumerate(tarr):
		for j,z1 in enumerate(z[zi:zmax]):
			try:

				deviat=deviat+((a[j+zi,i]-mu)**2)
			except IndexError:
				continue

	sigma=deviat/(count-1)
	ec=mu+(3*np.sqrt(sigma))
#	print 'media','sigma','3','s'
#	print mu,sigma,three,two
	#if ec > 1400:
	#	print fl, ec

	for i,t in enumerate(tarr):
		cloud=False
		for j,z1 in enumerate(z[zi:zmax]):
			try:
				if a[j+zi,i]>ec or a[j+zi,i]>thrs:
					horas=int(math.floor(t))
					minutos=int(round((t-horas)*60,-1))
					tim=datetime.datetime(year,mes,dia,horas,minutos)
					tmps.append(tim)
					#nbs.append(1)
					cloud=True
					break
			except IndexError:
				continue
		if cloud:
			nbs.append(1)
		else:
			nbs.append(0)
#	print tmps
#	print nbs
	return tmps,nbs

##########################################################################################
###LECTURA ESTANDAR DE PERFILES DE RETRODISPERSION
def readprofile(fl,tim):
	fle=open(fl,'r')
	for i in range(6):
		fle.readline()
	filename=fl.split('/')[1]
	#Check if filename is in UT-5 months.
	allprf=np.genfromtxt(fl,skip_header=8)
	z=np.array(fle.readline().split()[1:],dtype=float)
	tarr=np.array(fle.readline().split()[1:],dtype=float)
	fle.close()
	tarr=np.round(tarr,3)
	i,=np.where(tarr==tim)
	if len(i) == 0:
		return
	try:
		perfil=allprf[:,int(i[0])]
	except IndexError:
		return
	#print perfil
	#print perfil
	#print len(perfil)
	if len(allprf) == 250:
		for i in range(1,501,2):
			#print i
			perfil=np.insert(perfil,i,int(0))

	#print perfil
	try:

		return perfil
	except:
		pass
