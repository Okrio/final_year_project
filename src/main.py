import toolbox as tb
import numpy as np
import cv2 

img = cv2.imread('images/test_1.jpg', 1)
img = tb.extendImage(img)

pixel_position, contourArea = tb.detectSpeaker(img)

cX, cY = pixel_position

# Printout with "," to write output to next column in csv 
# print("x: " + str(cX) + "," + "y: " + str(cY) + "," + "Area: " + str(contourArea))

#print("True Azimuth: " + str(tb.getTruePosition(pixel_position)))
print(tb.getTruePosition(pixel_position))

if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows() 