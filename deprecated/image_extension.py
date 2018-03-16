import toolbox as tb
import numpy as np
import cv2 

# RICOH Theta Resolution: 5376x2688 pixels 
cv2.namedWindow('output_img', cv2.WINDOW_NORMAL)

img = cv2.imread('images/test_1.jpg', 1)
print (img.shape) # y, x

other_side = img[0:2688, 0:1000] # y, x
print(other_side.shape)

new = np.concatenate((img, other_side), axis=1)

cv2.resizeWindow('output_img', 1000, 800)
cv2.imshow('output_img', new)

if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows() 

# other_side = img[0:500, 0:2687]

# References: 
# https://stackoverflow.com/questions/7589012/combining-two-images-with-opencv
# http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_core/py_basic_ops/py_basic_ops.html