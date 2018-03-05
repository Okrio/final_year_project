#!/bin/bash/env bash 
# bash -x camera_script_mapping.sh
# bash camera_script_mapping.sh (to remove the commands)

# Remember to zero the camera! 
echo "Image Capturing Initiated: "
cd images 

gphoto2 --capture-image-and-download

count=1 
for file in *.JPG 
do 
	mv ${file} test_${count}.jpg 
	((count++))
done 

cd .. 

python experiment.py


# Appends python output to a csv file
# python experiment.py >> map_experiment.csv
# temp=$(python experiment.py) 
#echo ${temp}