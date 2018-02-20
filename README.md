## Operating Instructions: 
Coded for use in Linux Ubuntu 16.04 terminal 
1. Run camera_script.sh using `bash -x camera_script.sh` in bash terminal 
    - Resulting images are located in /images 
2. Run auto_frame_proc.py 
    - Output: Red highlighting of frame and its pixel position 

## Current Progress: (20 Feb 18)  
### Completed: 
1. Basic script to trigger capture of 5 images from RICOH THETA V and automatic download to /images folder 
2. Improved on frame detection algorithm 
    - Incremental thresholding feature that scans the images and draws out the relevant frame contours along with pixel position 

### To Do: 
1. Redo physical frame by improving contrast using a larger border and white structure to aid thresholding and canny edge detection 
    - White frame surrounding speaker, draw thick black border lines around speaker on the white frame 
2. Map pixel values to azimuth 
3. Run dummy tests of array calibration procedure 

### Useful References: 
1. Description of Canny Edge Detection http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_canny/py_canny.html
2. Description of Thresholding https://docs.opencv.org/2.4/doc/tutorials/imgproc/threshold/threshold.html#basic-threshold
3. Canny Edge parameters selection https://stackoverflow.com/questions/21324950/how-to-select-the-best-set-of-parameters-in-canny-edge-detection-algorithm-imple
