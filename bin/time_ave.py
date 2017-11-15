from os import listdir
from sys import argv
from math import pi

timeToAverage=float(argv[2])

def calc_N(w_0):
	#N is number of files in a period
	#N=2pi/w(t=0, r=0)/(dt*iterationsPerFile)
	first_w="w_data/"+w_0
	fil=open(first_w, 'r')
	line=fil.readline()
	w=abs(float(line.strip().split()[1]))
	#print("w=",w)
	dt=float(argv[1])
	itStep=int(times[1]-times[0])
	#print("itStep=",itStep)
	period_t=2.0*pi/w
	ret=int(timeToAverage*period_t/dt)+1
	return ret

w_files=[]
files_temp=listdir("w_data/")
for i in files_temp:
	if(i[0]!='w'):
		continue
	w_files.append(i)
w_files.sort(key=lambda x: x[2:-4])

times=[int(i[2:-4]) for i in w_files]
times.sort()

N=calc_N(w_files[0])
print("Averaging over "+str(N)+" files")
#print(w_files)
#w_files is list of all files
while(len(w_files)>=N):#
	to_ave=w_files[:N]
	#print(to_ave)
	w_files=w_files[N:]
	data={}
	for i in to_ave:
		#print(i)
		fil=open("w_data/"+ i, 'r')
		for line in fil:
			lin=line.strip().split()
			r=lin[0]
			w=lin[1]
			if r in data:
				data[r]+=float(w)
			else:
				data[r]=float(w)
		fil.close()
	r_vals=[i for i in data]
	r_vals.sort()
	name=to_ave[int(N/2)][2:-4]
	for i in r_vals:
		data[i]/=N
	out_name="w_ave"+str(name)+".dat"
	outfile=open("t_ave/"+out_name, 'w')
	for i in r_vals:
		outfile.write(str(i)+'\t'+str(data[i])+'\n')
	outfile.close()
