import toolbox as tb
import numpy as np
import cv2 

img = cv2.imread('images/test_1.jpg', 1)
pixel_position, contourArea = tb.detectSpeaker(img)
print(pixel_position)
print(contourArea)

if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows() 