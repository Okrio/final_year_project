import toolbox as tb
import numpy as np
import cv2 

img = cv2.imread('images/test_1.jpg', 1)
pixel_position, contourArea = tb.detectSpeaker(img)

cX, cY = pixel_position

# Printout with "," to write output to next column in csv 
print(str(cX) + "," + str(cY) + "," + str(contourArea))

# print("x: " + str(cX))
# print("y: " + str(cY))
# print("area: " + str(contourArea))

if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows() 