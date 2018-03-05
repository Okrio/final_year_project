#!/bin/bash/env bash 
# bash -x mapping_script.sh

echo "Image Captures Initiated: "
cd mapping_images

count=1 
for file in *.jpg 
do 
	mv ${file} test_${count}.jpg 
	((count++))
done 

cd .. 

python main.py