import toolbox as tb
import numpy as np
import cv2 

# Variables: 
pixel_threshold = 10 
font = cv2.FONT_HERSHEY_SIMPLEX

# Input Image: 
img = cv2.imread('images/test_5.jpg', 1)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray_img, (5,5), 0)

canny_low, canny_high = tb.setEdgeParameters(img)

# Set Up Windows: 
cv2.namedWindow('output_edged', cv2.WINDOW_NORMAL)
cv2.namedWindow('output_img', cv2.WINDOW_NORMAL)

while(1): 
	# Binary intensity sweep
	ret, th1 = cv2.threshold(blurred, pixel_threshold, 255,
		cv2.THRESH_BINARY_INV)
	
	# Canny Edge Detection post-binary sweep
	edged = cv2.Canny(th1, canny_low, canny_high)
	edged = cv2.dilate(edged, None, iterations = 1)
	edged = cv2.erode(edged, None, iterations = 1)

	output, contours, hierarchy = cv2.findContours(
										edged, 
										cv2.RETR_EXTERNAL, 
										cv2.CHAIN_APPROX_SIMPLE
										)
	for c in contours: 
		foundSpeaker, approx = tb.findSpeaker(c) 

		if foundSpeaker: 
			cv2.drawContours(img, approx, -1, (0,0,255), 2)
			tb.displayText(img, c, pixel_threshold)


	if pixel_threshold < 255: 
		pixel_threshold += 1

	cv2.resizeWindow('output_edged', 1000, 800)
	cv2.imshow('output_edged', edged)

	cv2.resizeWindow('output_img', 1000, 800)
	cv2.imshow('output_img', img)

	if cv2.waitKey(1) & 0xFF == ord('q'): 
		break

cv2.destroyAllWindows() 