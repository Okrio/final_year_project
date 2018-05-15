import toolbox as tb
import numpy as np
import cv2

def extendCubeImage(img_input):
	rotation270 = 270
	rotation90 = 90

	# Top Shifts
	upper_extension = img_input[0:1343, 2688:4031]
	(hu,wu) = upper_extension.shape[:2] 
	center_u = (wu/2, hu/2)

	# https://www.tutorialkart.com/opencv/python/opencv-python-rotate-image/

	M_R = cv2.getRotationMatrix2D(center_u, rotation270, 1)
	UR = cv2.warpAffine(upper_extension, M_R, (hu,wu))

	M_L = cv2.getRotationMatrix2D(center_u, rotation90, 1)
	UL = cv2.warpAffine(upper_extension, M_L, (hu,wu))

	# Bottom Shifts
	bottom_extension = img_input[2687:4031, 2688:4031]
	(hb, wb) = bottom_extension.shape[:2]
	center_b = (wb/2, hb/2)

	M_BL = cv2.getRotationMatrix2D(center_b, rotation270, 1)
	UBL = cv2.warpAffine(bottom_extension, M_BL, (hb,wb))


	img_input[1:1344, 4033:5376] = UR
	img_input[1:1344, 1345:2688] = UL

	img_input[2688:4031, 1344:2688] = UBL
	#https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html


	# cv2.namedWindow('extension', cv2.WINDOW_NORMAL)
	# cv2.resizeWindow('extension', 1000, 800)
	# cv2.imshow('extension', upper_extension)

	cv2.namedWindow('rotated_extension', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('rotated_extension', 1000, 800)
	cv2.imshow('rotated_extension', img_input)

# Cube Mapping: 
equirectangular_img = cv2.imread('images/raw_image.jpg')
img = tb.remapImage('images/raw_image.jpg')

# cv2.namedWindow('equirectangular_img', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('equirectangular_img', 1000, 800)
# cv2.imshow('equirectangular_img', equirectangular_img)

cube_map = cv2.imread('images/cube_map.jpg')

extendCubeImage(cube_map)

cv2.namedWindow('cube_map', cv2.WINDOW_NORMAL)
cv2.resizeWindow('cube_map', 1000, 800)
cv2.imshow('cube_map', cube_map)

if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows() 