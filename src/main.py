import toolbox as tb
import numpy as np
import cv2 



img = cv2.imread('images/raw_image.jpg', 1)

img = tb.extendImage(img)

pixel_position, contourArea = tb.detectSpeaker(img)

cX, cY = pixel_position

# Printout with "," to write output to next column in csv 
# print("x: " + str(cX) + "," + "y: " + str(cY) + "," + "Area: " + str(contourArea))

#print("True Azimuth: " + str(tb.getTruePosition(pixel_position)))
#print(cX, cY)
print(tb.getTruePosition(pixel_position))

if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows() 



# equirectangular_img = cv2.imread('images/raw_image.jpg')
# cv2.namedWindow('equirectangular_img', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('equirectangular_img', 1000, 800)
# cv2.imshow('equirectangular_img', equirectangular_img)


# img = tb.remapImage('images/raw_image.jpg')