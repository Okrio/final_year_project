import toolbox as tb
import numpy as np
import cv2 
import glob


source_img = 'images/process/raw_image.jpg'
img = cv2.imread(source_img, 1)

cv2.namedWindow('output_img', cv2.WINDOW_NORMAL)
cv2.resizeWindow('output_img', 1000, 800)

cv2.imshow('output_img', img)

if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows() 