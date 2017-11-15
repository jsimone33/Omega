import numpy as np
from sys import argv
from os import listdir

cmfile=argv[1]
dt=float(argv[2])

cmdata=np.loadtxt(cmfile)
t=cmdata[:,0]
x=cmdata[:,1]
y=cmdata[:,2]

#Remove bad data
#some times are duplicated
i=1
while(i<t.size):
	if(t[i]<=t[i-1]):
		t=np.delete(t,i)
		x=np.delete(x,i)
		y=np.delete(y,i)
	i+=1
#Find first time, it step
vxfiles=[]
for fil in listdir("vel_data"):
	if(fil[1]=='x'):
		vxfiles.append(fil)
vxfiles.sort(key=lambda x: int(x[3:-4]))
it0=int(vxfiles[0][3:-4])
itStep=int(vxfiles[1][3:-4])-it0
t0=it0/itStep*dt
dt_cmfile=t[1]-t[0]

#dIdx says how many time steps are in cmfile per 1 timestep in ascii file
dIdx=int(dt/dt_cmfile)

#Idx0 is idx of first ascii time
Idx0=np.argwhere(t==t0)



vy=np.zeros_like(y)
vx=np.zeros_like(x)
for i in range(1,x.size-1):
	vx[i]=(x[i+1]-x[i-1])/(t[i+1]-t[i-1])
	vy[i]=(y[i+1]-y[i-1])/(t[i+1]-t[i-1])

vx[-1]=(x[-1]-x[-2])/(t[-1]-t[-2])
vy[-1]=(y[-1]-y[-2])/(t[-1]-t[-2])


outfile=open("cm.txt",'w')
for i in range(Idx0,x.size,dIdx):
	outfile.write(str(x[i])+'\t'+str(y[i])+'\t'+str(vx[i])+'\t'+str(vy[i])+'\n')
outfile.close()
