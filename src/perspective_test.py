import toolbox as tb
import numpy as np
import cv2 

source_img = 'images/process/raw_image.jpg'
img = cv2.imread(source_img, 1)

cv2.namedWindow('output_img', cv2.WINDOW_NORMAL)
cv2.resizeWindow('output_img', 1000, 800)

equ = tb.Equirectangular(source_img) 
img = equ.GetPerspective(90, 90, 30, 800, 1000) # Specify parameters(FOV, theta, phi, height, width)
cv2.imshow('output_img', img)

if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows() 