# Clean data beforehand! Remove all lines that don't contain data
# For example, try: grep -v -e "^$" -e "#" vy.xy.asc > vy.xy.clean

import numpy as np
from os import listdir
from os.path import exists
from sys import argv


delta_r=float(argv[1])
vxfiles=[]
vyfiles=[]
for fil in listdir("vel_data"):
	if (fil[1]=='x'):
		vxfiles.append(fil)
	if (fil[1]=='y'):
		vyfiles.append(fil)

#Sort
vxfiles.sort(key=lambda x: int(x[3:-4]))
vyfiles.sort(key=lambda x: int(x[3:-4]))

cmdata=np.loadtxt("cm.txt")

for cmIdx, (xfile,yfile) in enumerate(zip(vxfiles,vyfiles)):

	#if(int(xfile[3:-4])<241664):
	#	#Only do late times
	#	continue

	vx_data = np.loadtxt("vel_data/"+xfile)
	vy_data = np.loadtxt("vel_data/"+yfile)

	#Bad data
	if(vx_data.size != vy_data.size):
		print("Skipping iteration "+xfile[3:-4])
		print("sizeof("+xfile+")!=sizeof("+yfile+")")
		continue

	time=xfile[3:-4]
	savename="w_data/w_"+time.zfill(6)+".txt"

	#Already done this time
	if(exists(savename)):
		print("Skipping iteration "+xfile[3:-4]+", already done")
		continue

	x = vx_data[:,9]-cmdata[cmIdx,0]
	y = vy_data[:,10]-cmdata[cmIdx,1]
	vx = vx_data[:,12]-cmdata[cmIdx,2]
	vy = vy_data[:,12]-cmdata[cmIdx,3]
	
	d = x**2 + y**2

	omega_x = (-y*vx)/d
	omega_y = (x*vy)/d

	omega = omega_x + omega_y

	w=np.zeros(300)
	weights=np.zeros(300)

	for i in range(x.size):
		idx1=int(np.sqrt(d[i])/delta_r)
		idx2=idx1+1
		weight2=float(np.sqrt(d[i])%delta_r)/delta_r
		weight1=1.0-weight2
		if(idx2<300):
			w[idx1]+=omega[i]*weight1
			w[idx2]+=omega[i]*weight2
			weights[idx1]+=weight1
			weights[idx2]+=weight2

	#Save w data
	savefile=open(savename, 'w')
	for i, (omega, weight) in enumerate(zip(w,weights)):
		rad=delta_r*i
		if (weight==0):
			weight=1
		savefile.write(str(rad)+'\t'+str(omega/weight)+'\n')
	savefile.close()
