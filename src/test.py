import cv2 
import numpy as np 

pink = np.uint8([[[255, 192, 203]]])
hsv_pink = cv2.cvtColor(pink,cv2.COLOR_BGR2HSV)

hot_pink = np.uint8([[[244, 194, 194]]])
light_pink = np.uint8([[[179, 27, 27]]])

hsv_hot_pink = cv2.cvtColor(hot_pink, cv2.COLOR_BGR2HSV)
hsv_light_pink = cv2.cvtColor(light_pink, cv2.COLOR_BGR2HSV)

print ("pink: ",hsv_pink) 
print ("hot pink: ", hsv_hot_pink)
print("light pink: ", hsv_light_pink)
