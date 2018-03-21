#!/bin/bash/env bash 
# bash -x camera_script_mapping.sh
# bash camera_script_mapping.sh (to remove the commands)

# Remember to zero the camera! 
# for i in `seq 1 3`
# do
# 	echo "Countdown: $i"
# 	sleep 1
# done

echo "Image Capturing Initiated: "
cd images 

gphoto2 --capture-image-and-download

for file in *.JPG 
do 
	mv ${file} raw_image.jpg 
done 

cd .. 

python main.py 


# Appends python output to a csv file
# python experiment.py >> map_experiment.csv


# count=1 
# for file in *.JPG 
# do 
# 	mv ${file} test_${count}.jpg 
# 	((count++))
# done 

# Ref for converting to cube: 
# https://github.com/flash286/sphere2cube

# sphere2cube images/raw_image.jpg -r1550 -f JPEG -V
# convert360 -i images/raw_image.jpg -o images/low_res.jpg -s 1792 1344