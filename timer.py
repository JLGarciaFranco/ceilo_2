import threading
import os
import sys

time=float(sys.argv[1])
global batscript
batscript=sys.argv[2]
def h():
    print ("It is time for to call: "+batscript)
    os.system('call '+batscript)
    lanza()  
 
def lanza():
    t=threading.Timer(time,h)
    t.start() 

lanza()
