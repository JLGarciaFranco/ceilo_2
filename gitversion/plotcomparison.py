import numpy as np
import matplotlib.pyplot as plt
import math
import os,glob
import sys 
minfile='/home/D1_CEILO/UNAM/MLH/MLH_averages/matrix.txt'
carpeta='/home/D1_CEILO/UNAM/MLH/MLH_averages/'
matrix='/home/D1_CEILO/UNAM/MLH/MLH_averages/hourly.txt'
hour=np.genfromtxt(matrix)
time1=np.asarray(range(0,24))
minute=np.genfromtxt(minfile)
time=minute[0]
minut=minute[1]
print time.size,hour.size,time1.size, minut.size
plt.plot(time1,hour,label='Hourly Avg')
plt.plot(time,minut,label='10 min Avg')
plt.xlim([0, time[141]])
plt.legend(loc='upper left',title='Avg',fontsize=11)
plt.xlabel('Time (h) UT-6')
plt.xticks(range(0,23,4))
plt.ylabel('Height [m a.g.l.]')
plt.title( 'Comparison Hourly Avg vs 10 min avg')
plt.savefig( carpeta +  'comparison_allperiod'+".png")
plt.show()

