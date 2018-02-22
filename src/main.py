import toolbox as tb
import numpy as np
import cv2 

# Input Image: 
img = cv2.imread('images/test_1.jpg', 1)
img2 = cv2.imread('images/test_2.jpg', 1)
img3 = cv2.imread('images/test_3.jpg', 1)

print(tb.detectSpeaker(img)) 
print(tb.detectSpeaker(img2)) 
print(tb.detectSpeaker(img3)) 


if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows() 