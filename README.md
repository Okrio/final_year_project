# Final Year Project Repository 
# Tasks: 
Phase 1: 
~~1. Set up relevant environments (Autumn Term, Week 3)
2. Set up version control environment (Git) (Autumn Term, Week 3) 
3.Isolate coloured dots in OpenCV (Autumn Term, Week 3) 
4. Track coloured dots using contours (Autumn Term, Week 4) 
5. Replaced dots with a surrounding coloured border (Autumn Term, Week 6) 
6. Used both masking colours and canny edge detection to better isolate the desired image (Autumn Term, Week 6) 
7. Designed a simple algorithm to differentiate desired/appropriate contours (Autumn Term, Week 6) 
8. Detects coloured border and able to obtain size of bounded object in pixels (Autumn Term, Week 6) ~~
9. Map pixel size to relative distance from a normal webcamera 
10. Determine pixel location of contours 

Need to figure out a way to account for angle problems with the circles! 
Use a reference contour and compare the area to the area obtained by minenclosingcircle to zero the program? 
Will use a square instead to detect out targets and determine if they are in the correct aspect ratio! Then you can estimate whether the camera is looking at them straight, or how the degree of change is like! 

# Strategies:
## Strategy 1: Using a Circle Target
### Tactics
Basically, this method aimed to approximate the detected spots with circle contours. In doing so, we can easily obtain the area and pixel location of the centre of the circle. 

1. Use a bit mask to isolate the HSV values of a pink circle 
2. Apply canny edge detection on it 
3. findContour and drawContour 
4. Apply minEnclosingCircle function on image to get approximated centre and radius of the circle 
    - This will provide us with both the area and pixel position of the target 
5. Apply contourArea() 
### Review:
Experimenting with such an approach revealed numerous shortcomings with this strategy: 
1. Such a method is not robust enough in a noisy environment where referencing the circle will be difficult. For example, unless the circle is directly parallel to the camera, the circle size approximated may change according to the tilt of the image. 
2. A possible solution was to conduct referencing of a circle area exactly parallel and keep a library of the pixel-area-to-distance map and have a loop to check if the paper was tilted but such a solution isn't elegant nor robust enough for actual use on the speakers and on a 360 camera. 
3. Additionally, using a cv2.Circle function would simply draw an approximated circle and have no output. Alternatively, we could fill in the circle and superimpose onto a black screen and mask it to get the number of pixels within the circle. 

Conclusion: Using a circle shape along with using a bit mask may not be the best way to solve the given problem. 

## Strategy 2: Using a Square Target
### Tactics: 
This may address certain robustness issues with Strategy 1. For example, since a square ideally has equally width and height, we can calculate its aspect ratio to ensure that it remains 1 and account for tilts should its aspect ratio change. This will help with mapping when the targets on the speakers are moved around in 3D. 

## Strategy 3: Using a bounded border around the speaker (speaker_detection.py)
### Tactics: 
This successfully address the aspect ratio problem and provides a simpler shape for OpenCV to detect and border using its contours

# Project Management Timeline: 

## References: 

## Coding Help: 
### Git References: 
Branching Tips: http://nvie.com/posts/a-successful-git-branching-model/

### OpenCV: 
Overall Tutorial: http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html

Creating slider bars in openCV: https://botforge.wordpress.com/2016/07/02/basic-color-tracker-using-opencv-python/

Measuring size of objects: https://www.pyimagesearch.com/2016/03/28/measuring-size-of-objects-in-an-image-with-opencv/

Contour Features: https://docs.opencv.org/3.3.0/dd/d49/tutorial_py_contour_features.html

Contour Hierarchy: https://docs.opencv.org/trunk/d9/d8b/tutorial_py_contours_hierarchy.html

Shape Descriptors: https://docs.opencv.org/2.4.13.2/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html

https://www.pyimagesearch.com/2016/02/15/determining-object-color-with-opencv/

https://www.pyimagesearch.com/2015/05/04/target-acquired-finding-targets-in-drone-and-quadcopter-video-streams-using-python-and-opencv/

