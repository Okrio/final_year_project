#!/bin/bash/env bash 
# bash -x camera_script.sh

echo "Image Captures Initiated: "
cd images 

gphoto2 --capture-image-and-download
gphoto2 --capture-image-and-download
gphoto2 --capture-image-and-download
gphoto2 --capture-image-and-download
gphoto2 --capture-image-and-download


count=1 
for file in *.JPG 
do 
	mv ${file} test_${count}.jpg 
	((count++))
done 