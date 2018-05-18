echo "Image Capturing Initiated: "
cd images 
cd process 

echo "Running Out of Plane Optical Calibration..."

for azimuth in `seq 0 72`
do 
	echo "Taking Picture for azimuth = $azimuth: "
	echo " "

	### Image Capture
	echo "Capturing Image..."
	gphoto2 --capture-image-and-download

	for file in *.JPG 
	do 
		mv ${file} out_of_plane_calibration_results/raw_image${azimuth}.jpg 
	done 

	read -p "Press any key to continue to next measurement"
done


#python main_perspective.py 