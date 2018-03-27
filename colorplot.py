import matplotlib.pyplot as plt 
import numpy as np
def colorplot(maxim,m0,jump,allprf,tarr,z,mlh,filename):
#Colorbar maximum color level y ticks range
	maxcollevel = maxim
        #Un color cada colorss niveles (Valores sugeridos para que el colorbar tenga continuidad). 
        colorss= (maxcollevel-100)/m0
        tickrange = maxcollevel+10
        #Tick every tickt number of levels
        tickt = jump
        #Levels of plot
        levels=range(0,maxcollevel,colorss)
	print levels
	x=yy
        #Configuracion para plotear sin valores en blanco, si un valor sale del rango aparece el valor maximo o $
        for i in range(len(allprf[0,:])):
                for j in range(len(allprf[:,0])):
                        if allprf[j,i] > max(levels):
                                allprf[j,i] = max(levels)
                        elif allprf[j,i] < min(levels):
                                allprf[j,i] = min(levels)
     #contour plot. 
        c1=plt.contourf(tarr,z,allprf,levels)

        # Colorbarticks range y labels
        cticks=range(0,tickrange,tickt)
        cb=plt.colorbar(c1,ticks=cticks)
        cb.set_label('Retrodispersion [a.Units]')
        plt.xlabel('Time [UT-6]')
        plt.ylabel('Height [m a.g.l.]')
        plt.title('Ceilometer Data')
        ttext=np.max(tarr)/3
        zmax=4000
        plt.xlim(0,24)
        plt.ylim(0,zmax)
        #Plotear mlh
        plt.scatter(tarr,mlh,color='white',s=12)
        #plt.savefig(filename)
        #plt.show()
        #plt.savefig('mlh.eps',format='eps',dpi=1000)

