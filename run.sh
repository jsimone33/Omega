######################### PARAMS #########################
vxfile=../vx.xy.asc
vyfile=../vy.xy.asc
delta_r=.05 #will collect omega data for multiples of this r value, should be around spacing of grid
M=0.1678 #ADM Mass of system
dt=1 #difference in time between files
timeToAverage=1.0 #How long to average over in periods
cmdata=../bhns.xon
####################### END PARAMS #######################

##Split Ascii files##

if [ -e vel_data ]
then
	#Skip if already done
	echo "Ascii file already split"
else
	mkdir vel_data
	echo "Splitting vx..."
	date
	python bin/split.py $vxfile x
	echo "...done"
	echo "Splitting vy..."
	date
	python bin/split.py $vyfile y
	echo "...done"
fi
echo
##Read CoM file##

if [ -f $cmdata ]
then
	echo "Calculating CoM..."
	python bin/cm_make.py $cmdata $dt
	echo "...done"
else
	echo "Assuming CoM=(0,0)"
fi
echo
##Convert to Omega##

if [ -e w_data ]
then
	echo "Omega files already made"
else
	mkdir w_data
	echo "Creating w data..."
	date
	python bin/vel_to_omega.py $delta_r
	echo "...done"
	date
fi
echo
##Time average over nearby files##

if [ -e t_ave ]
	then
	rm -rf t_ave
fi
mkdir t_ave

echo "Time averaging..."
python bin/time_ave.py $dt $timeToAverage
echo "...done"
echo
##Make Images##

if [ -e png_ave ]
	then
	rm -rf png_ave
fi
mkdir png_ave

echo "Making images..."
python bin/plot.py $M $dt
echo "...done"
