# !/bin/bash/env bash 

for azimuth in `seq 1 10` 
do 
	echo $(($azimuth*5)) 
	echo "hi $azimuth"
done
