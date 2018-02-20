#!/bin/bash/env bash 

echo "Image Captures Initiated: "
cd images 
gphoto2 --capture-image-and-download
gphoto2 --capture-image-and-download
gphoto2 --capture-image-and-download


count=0 
for file in *.JPG 
do 
	mv ${file} test_${count}.jpg 
	count=$($count + 1)
done 