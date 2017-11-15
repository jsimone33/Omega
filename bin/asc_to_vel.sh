if [ -e  vel_data ];
	then
	echo "Ascii files already split"
	exit 1
fi

mkdir vel_data

vxfile=$1
vyfile=$2

echo "Splitting vx"
awk '!/^($|#)/{print > "vel_data/vx."$1".txt"; close("vel_data/vx."$1".txt")}' $vxfile

echo "Splitting vy"
awk '!/^($|#)/{print > "vel_data/vy."$1".txt"; close("vel_data/vy."$1".txt")}' $vyfile
~                                                           
