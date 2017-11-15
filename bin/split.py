from sys import argv


v_file=argv[1]
direction=str(argv[2])
t=-1
outfile=open(".tmp.txt", 'w')
with open(v_file, 'r') as infile:
	for line in infile:
		#print(len(line))
		#print(line[0])
		if (line=='\n' or line[0]=='#'):
			continue
		data=line.strip().split()
		#print(data)
		#print(len(data))
		if (int(data[0])!=t):
			outfile.close()
			t=int(data[0])
			outname="vel_data/v"+direction+"."+str(t)+".txt"
			outfile=open(outname, 'a')
		outfile.write('\t'.join(data)+'\n')
	outfile.close()

