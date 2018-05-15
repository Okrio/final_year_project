echo "Image Capturing Initiated: "
cd images 
cd process 

gphoto2 --capture-image-and-download

for file in *.JPG 
do 
	mv ${file} raw_image.jpg 
done 

cd .. 
cd ..

python main.py 