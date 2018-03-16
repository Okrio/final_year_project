## Operating Instructions: 
Coded for use in Linux Ubuntu 16.04 terminal 
1. Run camera_script.sh using `bash camera_script_mapping.sh` in bash terminal 
    - Resulting images are located in /images 
    - True Azimuth is given 

## Current Progress: (05 March 18)  
### Completed: 
1. Basic script to trigger capture of 5 images from RICOH THETA V and automatic download to /images folder 
2. Improved on frame detection algorithm 
    - Incremental thresholding feature that scans the images and draws out the relevant frame contours along with pixel position 
3. Redo physical frame by improving contrast using a larger border and white structure to aid thresholding and canny edge detection
    - White frame surrounding speaker, draw thick black border lines around speaker on the white frame
4. Map pixel values to azimuth in horizontal plane (Accurate to 5 degrees) 
5. Installed RICOH THETA V official extension, improved stability of system
6. Interfaced with Intersense IntertiaCube4's azimuth tracker. 
7. Duplicate pixels from one end of image to the other so that system can detect all 360 degrees without the square being halved in between sides (Implemented in extendImage function in toolbox) 

### To Do: 
1. Run dummy tests of array calibration procedure 
2. Catch up on theoretical evaluation of interpolation 
3. Improve detection robustness by adding condition to check last known position in y coordinates (so can detect if accidentally detect another square shape in the room) - simple tracker
5. Verify accuracy of optical system with azimuth tracker 
6. Integrate array calibration with optical system 

### Useful References: 
1. Description of Canny Edge Detection http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_canny/py_canny.html
2. Description of Thresholding https://docs.opencv.org/2.4/doc/tutorials/imgproc/threshold/threshold.html#basic-threshold
3. Canny Edge parameters selection https://stackoverflow.com/questions/21324950/how-to-select-the-best-set-of-parameters-in-canny-edge-detection-algorithm-imple
