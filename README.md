## Operating Instructions: 
Coded for use in Linux Ubuntu 16.04 terminal 
1. Run camera_script.sh using `bash camera_script_mapping.sh` in bash terminal 
    - Resulting images are located in /images 
    - True Azimuth is given 

## Current Progress: (23 March 18)  
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
8. Ran tests of array calibration procedure 
9. Integrated array calibration with optical system 
10. Trimed and Aligned Impulse response measurements 
11. Did a first trial interpolation of measurements in Clear Lab
12. Added a 'Cube Map' warp function inside toolbox.py to unwrap equirectangular image to cube map efficiently https://pastebin.com/Eeki92Zv
13. Found that Cube Mapping has difficulty detecting speaker at top left, right and bottom left, right of sphere due to splitting of image
14. Used perspective shift to successful detect speaker at out of horizontal plane measurements https://github.com/fuenwang/Equirec2Perspec, getting around 13. 
15. Conduct proper horizontal plane calibration measurements in large room and Interpolate 

### To Do: 
1. Catch up on theoretical evaluation of interpolation 
2. Improve detection robustness by adding condition to check last known position in y coordinates (so can detect if accidentally detect another square shape in the room) - simple tracker
3. Verify accuracy of optical system with azimuth tracker (Plot error) 
4. Write different scripts and use different detection parameters for horizontal and out of horizontal detection. i.e If speaker is roughly in horizontal plane, use basic algorithm in equirect format, else if in top half of plane, use perspective shift and scan top half, else if bottom half of plane, use perspective shift and scan bottom half - This will improve effectiveness and efficient of the detection and mapping 
5. Out of horizontal plane mapping
6. Plot interpolation results for different intervals (i.e 30 degrees instead of 10) - show how varying the number of measurements taken will change the outcome - i.e taking more measurements at smaller intervals is better, since this is the objective of the project: to take high resolution positions 
7. Plot 3D graph of a single channel: y axis is response, x axis is sample, with each line a different direction (check iphone image) 
8. Plot error rate of optical measure vs the InertiaCube4 method 
9. Read Dr Moore's paper on evaluating interpolation - find metrics to use to evaluate 
10. Use results to do direction of arrival estimation (Dr Moore's youtube video) - request for the paper he was talking about
11. Add in orientation detection to do out of plane detection

### Useful References: 
1. Description of Canny Edge Detection http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_canny/py_canny.html
2. Description of Thresholding https://docs.opencv.org/2.4/doc/tutorials/imgproc/threshold/threshold.html#basic-threshold
3. Canny Edge parameters selection https://stackoverflow.com/questions/21324950/how-to-select-the-best-set-of-parameters-in-canny-edge-detection-algorithm-imple

#### Image Warping: 
1. https://stackoverflow.com/questions/29678510/convert-21-equirectangular-panorama-to-cube-map  
2. https://github.com/fuenwang/Equirec2Perspec
