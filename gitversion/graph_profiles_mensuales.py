import numpy as np
import matplotlib.pyplot as plt
import math
import os,glob
import sys 
carpeta='/home/D1_CEILO/UNAM/PRCL/Results/Perfiles/meses/'
outputdir='/home/D1_CEILO/UNAM/PRCL/Results/Plots/article/'
os.chdir(carpeta)
dirs = filter(os.path.isdir, os.listdir('.'))  
months=['Jan-Feb','Mar-Apr','May-Jun','Jul-Aug','Sep-Oct','Nov-Dic']
plt.figure(1,figsize=(15,10),dpi=100)
m=1
for directorio in months:
	print directorio
	os.chdir(carpeta+directorio)
	
	flist=glob.glob(carpeta+directorio+"/avg*.txt")
	
	flist=np.sort(flist)
	z=range(50,5000,10)
	l=700
	print flist
	plt.subplot(230+m)
	for i,filename in enumerate(flist):
		vec=np.genfromtxt(filename,skip_header=3)
		vec=vec[5:]
		vec=vec+l
		print len(z), len(vec)
		plt.plot(vec,z,color='k',linestyle='-')
		l=l+700

	plt.xlabel('Time (h) UT-6')
	plt.xticks(np.linspace(700, 4900, 7),['6','8','10','12','14','16','18'])
	plt.ylabel('Height [m a.g.l.]')
	plt.title(months[m-1]+' Backscattering profiles [a.Units] ')
	m=m+1
plt.tight_layout()
plt.savefig( outputdir +  'evolutionbimestral'+".png")
	
