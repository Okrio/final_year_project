#!/bin/sh

# script to measure acoustic impulse response using hard coded devices and stumulus file
#REC_DEVICE=Channel_1__Channel_2__Channel_3__Channel_4__Channel_5__Channel_6__Channel_7__Channel_8
REC_DEVICE=alsa_input.usb-RME_OctaMic_XTC__23640801__14F52E381D72BC8-00.multichannel-input
NUM_REC_CHANNELS=4
#PLAY_DEVICE=Channel_1__Channel_2__Channel_3__Channel_4
PLAY_DEVICE=alsa_output.usb-RME_OctaMic_XTC__23640801__14F52E381D72BC8-00.multichannel-output
NUM_PLAY_CHANNELS=1
STIMULUS_FILE=sweptsine_20_24000_0.6_48000.wav

#	sample spec: s32le 16ch 44100Hz

# make output directory
if [ $# -lt 1 ]; then
    OP_DIR='.'
else 
    OP_DIR=$1
    mkdir -p $OP_DIR
fi

# record response to sweep
echo start recording...
parecord --device=$REC_DEVICE --channels=$NUM_REC_CHANNELS --no-remix --no-remap --rate=48000 $OP_DIR/rvrb_sweep.wav &
echo started recording.
echo starting playback...
#paplay --device=$PLAY_DEVICE --channels=$NUM_PLAY_CHANNELS --no-remap  --volume=49152 $STIMULUS_FILE
paplay --device=$PLAY_DEVICE --no-remap  --volume=49152 $STIMULUS_FILE

echo playback finished.
sleep 2
pkill parecord
echo killing parecord...