import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from os import listdir
from sys import argv

offset=1 #number of points to ignore near origin

#get itStep to calculate t/M
wfiles=[]
for fil in listdir("w_data"):
	if (fil[0]=='w'):
		wfiles.append(fil)
wfiles.sort(key=lambda x: int(x[2:-4]))
itStep=int(wfiles[1][2:-4])-int(wfiles[0][2:-4])


#This program plots all files at once and saves one image

M=float(argv[1])
dt=float(argv[2])
files_temp=listdir("t_ave/")
files=[]
for i in files_temp:
	if(i[:5]=="w_ave"):
		files.append(i)
files.sort()
n=len(files)

data=[]
times1=[]
for num,i in enumerate(files):
	data.append(np.loadtxt("t_ave/"+i))
	data[num]=data[num][data[num][:,0].argsort()]
	times1.append(i[5:-4])

times=[str(int(int(t)*(dt/itStep)/M)).zfill(7) for t in times1]

def setPlot():
	plt.xlim(0,20)
	plt.ylim(0,.05)
	plt.xlabel(r'$r/M$')
	plt.ylabel(r'$\Omega \times M$')
	plt.title("Evolution of Omega")
	plt.legend()

x=np.linspace(600,1200,601)
def AnnotatePlot():
	plt.plot(x/M,M*.000025*(x/1000)**(-3/2), '--', lw=6, color=(0,0,0,.9))
	plt.annotate(r'$\sim r^{-3/2}$',xy=(900/M,.000035*M),fontsize=18)

for i in range(0,n,1):
	blues=[float(3*(n-i))/(5*n),float(4*(n-i))/(5*n),float((n-i))/n]
	plt.figure(1) #Plot for one time
	plt.plot(data[i][offset:,0]/M,data[i][offset:,1]*M,lw=2, color=blues, label="t/M="+str(int(times[i])))
	setPlot()
	plt.savefig("png_ave/w_"+times[i]+".png")
	plt.clf()
	plt.figure(2) #Plot for all times
	if(i%int(n/8)==0): #Only Show 8 labels so its not too crowded
		plt.plot(data[i][offset:,0]/M,data[i][offset:,1]*M,lw=2, color=blues, label="t/M="+str(int(times[i])))
	else:
		plt.plot(data[i][offset:,0]/M,data[i][offset:,1]*M,lw=2,color=blues)


setPlot()
plt.savefig("png_ave/AllTimes.png")
