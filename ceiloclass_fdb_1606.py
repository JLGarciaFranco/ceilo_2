# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 11:46:37 2013

@author: wolf
Modified: 08/05/16 
Jorge L. Garcia.
"""
  
import  numpy as np
filename='' 
import  numpy as np
import glob,os
import fileinput
import sys
class ceilo:
    ipos0=0
    iposd=0
    dpos=0
    tarr=[]
    filename=''
    def __init__(self,filename):
        self.filename=filename
        print ( 'initialize' )
    def init(self):
        filename=self.filename
        print ( filename )
        fceilo=open(filename,'rb')
        for counter in range(2):
            line1=fceilo.readline()
        self.iposd=fceilo.tell()	
        line1=fceilo.readline()
        print ( line1 )
        self.ipos0=fceilo.tell()
        line1=fceilo.readline()
        ##print line1
        line2=fceilo.readline()
        ##print line2
        ###print line1
        for counter in range(2):
        	line=fceilo.readline()
        	###print line
        self.ipos1=fceilo.tell()
        ##print ipos100
        line=fceilo.readline()
        ###print line
        for counter in range(12):
        	iposa=fceilo.tell()
        	linemore=fceilo.readline() 
        	if linemore.strip() == line1.strip():
        	  ###print line1
        	  ipos2=iposa
		  break 
        	  ##print ipos2 
        self.dpos=ipos2-self.ipos0
        print ('dpos',self.dpos)
        fceilo.seek(self.ipos1+10*self.dpos,0)
        line2=fceilo.readline()
        self.tarr=self.gettimes(fceilo)
        fceilo.close()
        ##print ipos0
        ##print ipos1
        ##print ipos2
        ##print dpos
    def altitudes(self):
        a=range(self.nz)
        z=np.zeros(self.nz)
        for i in a:
            z[i]=self.dz*i
        return z
    # funcion para corregir la interpretacion del  los numeros hex negativos
    def signcorr(self,x):
    	icounter=0
    	for xx in x:
    	  if xx > 1048576/2: 
    	    xx=xx-1048576
    	    x[icounter]=xx
    	  icounter=icounter+1
    	return x
     
                
    ##################################################################
    
    # funccion para leer el date time n
    def gotondate(self,n,filename):
    	fc=open(filename,'rb')
    	fc.seek(iposd+n*dpos,0)
    	sdatetime=fc.readline()
    	fc.close()
    	return sdatetime
    
    def ogotondate(self,n,fc):
    	fc.seek(self.iposd+n*self.dpos,0)
    	sdatetime=fc.readline()
    	return sdatetime
    
    # retrurn time as decimal number from string
    	
    
    # funccion para leer el perfil n 
    def gotonprf(self,n,filename):
    	fc=open(filename,'rb')
    	fc.seek(ipos1+n*dpos)
    	line=fc.readline()
    	fc.close()
    	line=line.strip()
    	prf=[int(line[i:i+5],16) for i in range(0,self.nz*5,5)]
    	prf=signcorr(prf)
    	return prf
    
    def ogotonprf(self,n,fc):
    	fc.seek(self.ipos1+n*self.dpos)
    	line=fc.readline()
    	line=line.strip() 
    	prf=[int(line[i:i+5],16) for i in range(0,self.nz*5,5)]
    	prf=self.signcorr(prf)
    	fprf=np.array(prf)      
    	return fprf
    
    def gettimes(self,fc):
         fc.seek(0,2)
         iend=fc.tell()
         ntimes=int((iend-self.iposd)/self.dpos)
         tarr=np.zeros(ntimes)
         for i in range(1,ntimes):
             ##print i
             sdatetime=self.ogotondate(i,fc)
             darr=sdatetime.split()
             stime=str(darr[1])
             #print stime
             #stime=stime[2:10]
             stimearr=stime.split(':')
             #print stime
             #print stimearr
             t=float(stimearr[0])+float(stimearr[1])/60+float(stimearr[2])/3600
             tarr[i]=t
         return tarr
         ##print ntimes*dpos+iposd
         ##print ntimes
         
    def avrg(self,idx,fc):
        #print (idx)
        ##print type(idx)
        nele=len(idx)
        if nele == 0:
            nele=-1
        #print (nele)
        prf=np.zeros(self.nz)
	
        for i in idx:
            ##print i
            prfnew=self.ogotonprf(i,fc)
            for j in range(self.nz):
                prf[j]=prf[j]+prfnew[j]
        for j in range(self.nz):
            prf[j]=prf[j]/nele
        return [prf,nele]
    
    ##################################################################
    
    def idx(self,ti,te,tarr):
        idxarr=[i for i,t in enumerate(tarr) if ti <= t < te]
        return idxarr
    #################################################################
     
    def avrgprf(self,ti,te,fc):
        self.tarr=self.gettimes(fc)
        idxarr=self.idx(ti,te,self.tarr)
	if len(idxarr) != 0:
	        prf=self.avrg(idxarr,fc)
		return prf
    ################################################################
    def readceilofile(self,filename,dt,nz,dz):
        self.init()
	self.nz=nz
	self.dz=dz
        z=self.altitudes()
        nzp=len(z)
        zz=z[0:nzp]
        ff=open(filename,'rb')
        tarr=self.gettimes(ff)
        tarr=tarr[1:]
        #dt=0.1
        #tmin=0.0 # jorge 20160420
        tmin=np.min(tarr)
	tmax=np.max(tarr)
	base=1.0*dt/6.0
	tbuenos=np.arange(24*6)/6.0
	#print tbuenos
	itmin= np.argmin(np.abs(tbuenos-tmin))
	tmin=tbuenos[itmin]
	itmax=np.argmin(np.abs(tbuenos-tmax))
	tmax=tbuenos[itmax]
	#tmin=round(tmin,base)
	tmax=24.0        
	#print tmin, tmax
        nt=int(round((tmax-tmin)/dt))
        allprf=np.zeros((nzp,nt))
        dallprf=np.zeros((nzp,nt))
        numprof=np.zeros(nt)
        t0=tmin
        t1=t0+dt
        ts=np.zeros(nt)
        
        for i in range(nt):
        	t=tmin+i*dt
        	prf_num=self.avrgprf(t,t+dt,ff)
		prf=prf_num[0]
		numprof[i]=prf_num[1]
		ts[i]=t
            	for j in range(nzp):
			try:               
						
				allprf[j,i]=prf[j]
			except:
				print 'no datos'
        ff.close()
        return [ts,zz,allprf,numprof]
        
    
