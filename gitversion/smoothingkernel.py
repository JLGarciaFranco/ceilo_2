# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 22:12:03 2013

@author: wolf
"""
import numpy as np
nz=3
na=1
daz=0.1
da=0.1
da0=0.1


z=range(nz)

def smoothmatrix(z,da0,da):
	nz=len(z)
	smoothkernel=np.zeros((nz,nz))
	for i in range(nz):
		 for j in range(nz):
		     if i ==j:
		         smoothkernel[i,j]=1.0
	for i in range(nz):
		 for j in range(nz):
		     if i ==j-1:
		         smoothkernel[i,j]=smoothkernel[i,j]+(da*z[i]+da0)
		         smoothkernel[i,i]=smoothkernel[i,i]-(da*z[i]+da0)     
		     if i ==j+1:
		         smoothkernel[i,j]=smoothkernel[i,j]+(da*z[i]+da0)
		         smoothkernel[i,i]=smoothkernel[i,i]-(da*z[i]+da0)
	return smoothkernel

def smoothmatrixn(z,da0,da,na):
    nz=len(z)
    smoothkernel=np.zeros((nz,nz))
    for i in range(nz):
        for j in range(nz):
            if i ==j:
                smoothkernel[i,j]=1.0
    for i in range(nz):
        for j in range(nz):
            if i ==j-1:
                smoothkernel[i,j]=smoothkernel[i,j]+(da*z[i]+da0)
                smoothkernel[i,i]=smoothkernel[i,i]-(da*z[i]+da0)     
            if i ==j+1:
                smoothkernel[i,j]=smoothkernel[i,j]+(da*z[i]+da0)
                smoothkernel[i,i]=smoothkernel[i,i]-(da*z[i]+da0)
    sm=smoothkernel
    for i in range(na-1):
        smoothkernel=np.dot(smoothkernel,sm)
    return smoothkernel


#z=xrange(nz)*20.0
#dz=xrange(nz)*5.0
#dzmax=100

def smoothmatrixexp(z,dz,dzmax):
    nz=len(z)
    smoothkernel=np.zeros((nz,nz))
    for i in range(nz):
        for j in range(nz): 
            if np.abs(z[i]-z[j]) < dzmax:
                #print i,j
                smoothkernel[i,j]=np.exp(-(z[i]-z[j])*(z[i]-z[j])/(dz[i]*dz[j]))
    for i in range(na):
                matrix=np.dot(smoothkernel,smoothkernel)
	#    smoothkernel=matrix           
    for i in range(nz):
        vec=smoothkernel[i,:]
        fnormal=vec.sum()
        for j in range(nz):
            smoothkernel[i,j]=smoothkernel[i,j]/fnormal  
    return smoothkernel


nz=10
def L1(nz):
    grad=np.zeros((nz,nz)) 
    for i in range(nz-1):
        for j in range(nz):
            if i ==j:
                grad[i,j]=-1
            if i ==j-1:
                grad[i,j]=1
    for i in range(nz):
        for j in range(nz-1):
            if i ==j:
                grad[i,j]=grad[i,j]+1
            if i ==j+1:
                grad[i,j]=grad[i,j]-1
    for i in range(1,nz-2,1):
        #print i
        for j in range(nz-1):
            grad[i,j]= grad[i,j]/2.0
    return grad


   
