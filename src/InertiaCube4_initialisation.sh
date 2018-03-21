#!/bin/bash/env bash 

cd InertiaCube4
sudo stty -F /dev/ttyUSB0 921600 clocal
sudo chmod 0777 /dev/ttyUSB0

./ismain64

# https://electronics.stackexchange.com/questions/36874/would-anyone-know-how-to-use-the-intersense-navchip-sensor-with-linux