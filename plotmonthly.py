import numpy as np
import matplotlib.pyplot as plt
import math
import os,glob
import sys 
carpeta='/home/D1_CEILO/UNAM/MLH/MLH_averages/'
os.chdir(carpeta)
flist=glob.glob(carpeta+"matrix_*.txt")
flist=np.sort(flist)
timefile='/home/D1_CEILO/UNAM/MLH/MLH_averages/time.txt'
time=np.genfromtxt(timefile)
print flist
plt.figure(1,figsize=(8,6),dpi=100)
meses=['Jan-Feb','Mar-Apr','May-Jun','Jul-Aug','Sep-Oct','Nov-Dec']
for i,fi in enumerate(flist):
	day=fi.split('/')[-1]
	vec=np.genfromtxt(fi)
	if vec.size >142:
		vec=vec[:142]
	plt.plot(time,vec, label=meses[i] )
plt.xlim([0, time[141]])
plt.legend(loc='upper left',title='Periods',fontsize=11)
plt.xlabel('Time (h) UT-6')
plt.xticks(range(0,23,4))
plt.ylabel('Height [m a.g.l.]')
plt.title( 'Bimonthly averages')
plt.savefig( carpeta +  'bimonthly_10minavg'+".png")
plt.show()


