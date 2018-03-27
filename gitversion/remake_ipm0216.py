 
import numpy as np
import glob,os
import fileinput
import sys
import csv
import math
outputdir= '/home/D1_CEILO/UNAM/MLH/log_CL3/'
carpeta='/home/D1_CEILO/UNAM/matrices/v201510_10_matrix/'
os.chdir(carpeta)
flist=glob.glob(carpeta+"*.txt")
flist=np.sort(flist)
def calmlh(fl):
	fle=open(fl,'r')
	fle.readline()
	fle.readline()
	fle.readline()
	fle.readline()
	fle.readline()
	allprf=np.genfromtxt(fl,skip_header=7)
	z=np.array(fle.readline().split()[1:],dtype=float)
	tarr=np.array(fle.readline().split()[1:],dtype=float)
	mlh=np.zeros(len(tarr),dtype=float)
	for i,t in enumerate(tarr):
		if len(allprf) > 255:
			allprf1=np.log(allprf)
			vec=allprf1[15:400,i]-allprf1[14:399,i]
			#vec_2=np.diff(vec)
			imin=np.argmin(vec)
			mlh[i]=z[imin+14]
		elif len(allprf) <=250:
			allprf1=np.log(allprf)
			vec=allprf1[8:250,i]-allprf1[7:249,i]
			#vec_2=np.diff(vec)
			imin=np.argmin(vec)
			mlh[i]=z[imin+7]		
	fle.close()
	return 	 mlh
def writemlh(outputfile,horas,mlhs,estacion):
	fout=open(outputfile,'w')
	fout.write("Ceilometer Vaisala CL31. 5 min averages in "+estacion+"\n")
	fout.write("MLH from Gradient method. Espectroscopia y Percepcion Remota, CCA-UNAM\n")
	fout.write("Version del codigo: 201510"  )
	fout.write("http://www.atmosfera.unam.mx/espectroscopia/ceilo/\n")
	fout.write("Hora.decimal  MLH(m)\n")
	for i,unamlh in enumerate(mlhs):
		timeh=horas[i]
		fout.write("%.3f         %i \n" % (timeh,unamlh))
	fout.close()	
for filename in flist:
	fle=open(filename,'r')
	fle.readline()
	fle.readline()
	fle.readline()
	fle.readline()
	fle.readline()
	fle.readline()
	tarr=np.array(fle.readline().split()[1:],dtype=float)
	mlh=calmlh(filename)

	files= filename.split('/')[-1]
	writemlh(outputdir+files[0:8]+'_UNAM_vipm.txt',tarr, mlh, 'UNAM')

