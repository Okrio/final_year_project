# !/bin/bash/env bash 
# bash optical_acoustic_measurements.sh

echo "Running Optical Acoustic Measurements..."
# Run program for intervals of 5 degrees 

for azimuth in `seq 0 72`
do 
	#azimuth=$(($counter*5)) 
	echo "Starting measurements for azimuth = $azimuth: "
	echo " "

	### Image Capture 
	echo "Capturing Image..."
	cd images

	gphoto2 --capture-image-and-download

	for file in *.JPG 
	do 
		mv ${file} raw_image.jpg 
	done 

	cd .. 

	### Measure Azimuth 
	python main.py >> audio/azimuth_909b.csv

	cd images 


	mv raw_image.jpg 909b_images_results/raw_image${azimuth}.jpg
	 

	cd .. 

	echo " "


	### Measure Acoustic Impulse Response 
	# Hardware Initialisation: 
	REC_DEVICE=alsa_input.usb-RME_OctaMic_XTC__23640801__14F52E381D72BC8-00.multichannel-input
	NUM_REC_CHANNELS=5

	PLAY_DEVICE=alsa_output.usb-RME_OctaMic_XTC__23640801__14F52E381D72BC8-00.multichannel-output
	NUM_PLAY_CHANNELS=4

	STIMULUS_FILE=audio/sample/sweptsine_20_24000_0.6_48000.wav
	PLAY_CHANNELMAP=front-left,front-right,rear-left,rear-right

	# Record Sweep Response:
	echo "Starting Recording..."
	parecord --device=$REC_DEVICE --channels=$NUM_REC_CHANNELS --no-remix --no-remap --rate=48000 audio/rvrb_sweep_azimuth_$azimuth.wav &
	echo "Started Recording"

	echo "Starting Sweep..."
	paplay --device=$PLAY_DEVICE --channels=1 --channel-map=rear-left --volume=49152 $STIMULUS_FILE
	echo "Sweep Completed"

	sleep 2
	echo "Killing parecord"
	pkill parecord 

	read -p "Press any key to continue to next measurement"

	echo " "
	echo " "
	echo " "
done 

echo "Measurements Completed"





