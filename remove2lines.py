import sys
file=sys.argv[1]
f1=open(file,'r')
line1=f1.readline()
line2=f1.readline()
data=f1.read()
f1.close()
print (line1)
print (line2)
f2=open(file,'w')
f2.write(data)
f2.close()
