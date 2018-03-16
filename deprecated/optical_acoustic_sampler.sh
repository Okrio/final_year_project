# !/bin/bash/env bash 
# bash camera_sampler.sh

echo "Capturing Image..."
cd images

gphoto2 --capture-image-and-download

count=1
for file in *.JPG 
do 
	mv ${file} test_${count}.jpg 
	((count++))
done 

cd .. 

read -p "Press any key to continue"

# Obtains optical position
python main.py 

### Measures Acoustic Impulse Response 

# Hardware Initialisation: 
REC_DEVICE=alsa_input.usb-RME_OctaMic_XTC__23640801__14F52E381D72BC8-00.multichannel-input
NUM_REC_CHANNELS=5

PLAY_DEVICE=alsa_output.usb-RME_OctaMic_XTC__23640801__14F52E381D72BC8-00.multichannel-output
NUM_PLAY_CHANNELS=4

STIMULUS_FILE=audio/sample/sweptsine_20_24000_0.6_48000.wav
PLAY_CHANNELMAP=front-left,front-right,rear-left,rear-right

# Output Directory 
# if [ $# -lt 1 ]; then
#     OP_DIR='.'
# else 
#     OP_DIR=$1
#     mkdir -p $OP_DIR
# fi

# Record Sweep Response: 
echo "Starting Recording..."
#parecord --device=$REC_DEVICE --channels=$NUM_REC_CHANNELS --no-remix --no-remap --rate=48000 $OP_DIR/rvrb_bng_sweep.wav &
parecord --device=$REC_DEVICE --channels=$NUM_REC_CHANNELS --no-remix --no-remap --rate=48000 audio/rvrb_bng_sweep.wav &
echo "Started Recording"

echo "Starting Sweep..."
paplay --device=$PLAY_DEVICE --channels=1 --channel-map=rear-left --volume=49152 $STIMULUS_FILE
echo "Sweep Completed"

sleep 2
echo "Killing parecord"
pkill parecord 
