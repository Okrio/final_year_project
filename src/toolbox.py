############### Toolbox ############## 
import numpy as np
import cv2 

def setEdgeParameters(img):
	# Input: Image frame 
	# Output: Adaptive thresholds for Canny Edge Detection 
	sigma = 0.33 
	v = np.median(img) 
	lower_threshold = int(max(0, (1.0 - sigma) * v))
	upper_threshold = int(min(255, (1.0 + sigma) * v))

	return lower_threshold, upper_threshold 

def getPosition(contour):
	# Input: Contour
	# Output: Pixel position of contour center
	M = cv2.moments(contour) 
	if M['m00']!=0: 
		cX = int(M['m10']/M['m00'])
		cY = int(M['m01']/M['m00'])
	else: 
		cX, cY = 0, 0
	return cX, cY 

def displayText(img, contour, pixel_threshold):
	# Input: Image frame, contour, current_pixel_threshold 
	font = cv2.FONT_HERSHEY_SIMPLEX 
	cX, cY = getPosition(contour) 
	position_text = "Speaker Position: " + str(getPosition(contour))
	cv2.putText(img, position_text, (cX, cY - 15), font, 0.5, (0,0,255), 2)
	cv2.putText(img, "x", (cX, cY), font, 0.5, (0, 255, 0), 1) 
	cv2.putText(img, str(pixel_threshold), (cX, cY - 30), font, 0.5, (0,0,255), 2)

def findSpeaker(c): 
	perimeter = cv2.arcLength(c, True)
	epsilon = 0.01*perimeter 
	approx = cv2.approxPolyDP(c, epsilon, True)

	if len(approx) == 4: 
		(x,y,w,h) = cv2.boundingRect(approx) 
		aspect_ratio = w/float(h) 
		area = cv2.contourArea(c)
		hullArea = cv2.contourArea(cv2.convexHull(c))
		solidity = area/float(hullArea)

		# Check for Flags: 
		keepSolidity = solidity > 0.8 
		keepAspectRatio = aspect_ratio >= 0.8 and aspect_ratio <=1.2
		keepDims = w > 50 and h > 50 # If cannot detect, adjust this! 
 
		# Found Speaker: 
		if keepAspectRatio and keepSolidity and keepDims:
			return True, [approx]
		else: 
			return False, [] 
	else: 
		return False, []

def detectSpeaker(img): 
	pixel_threshold = 10 
	font = cv2.FONT_HERSHEY_SIMPLEX
	foundSpeaker = False 

	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray_img, (5,5), 0)

	canny_low, canny_high = setEdgeParameters(img)

	# Set Up Windows: 
	# cv2.namedWindow('output_edged', cv2.WINDOW_NORMAL)
	cv2.namedWindow('output_img', cv2.WINDOW_NORMAL)

	while(foundSpeaker == False): 
		# Binary intensity sweep
		ret, th1 = cv2.threshold(blurred, pixel_threshold, 255,
			cv2.THRESH_BINARY_INV)
		
		# Canny Edge Detection post-binary sweep
		edged = cv2.Canny(th1, canny_low, canny_high)
		edged = cv2.dilate(edged, None, iterations = 1)
		edged = cv2.erode(edged, None, iterations = 1)

		# Display Canny Edge Changes 
		# cv2.resizeWindow('output_edged', 1000, 800)
		# cv2.imshow('output_edged', edged)

		# contours = sorted(contours, key = cv2.contourArea, reverse= True)[:5] 
		# Cannot use this here else the outer frame will be the only one which is found 

		# Finding and Drawing Contour: 
		output, contours, hierarchy = cv2.findContours(
											edged, 
											cv2.RETR_EXTERNAL, 
											cv2.CHAIN_APPROX_SIMPLE
											)

		for c in contours: 
			foundSpeaker, approx = findSpeaker(c) 

			if foundSpeaker: 
				cv2.drawContours(img, approx, -1, (0,0,255), 2)
				displayText(img, c, pixel_threshold)
				cv2.resizeWindow('output_img', 1000, 800)
				cv2.imshow('output_img', img)

				return getPosition(c), cv2.contourArea(c)
				
		if pixel_threshold < 255: 
			pixel_threshold += 2

		if pixel_threshold == 255: 
			print('Speaker not found')

		if cv2.waitKey(1) & 0xFF == ord('q'): 
			break

def getTruePosition(pixel_position):
	x, y = pixel_position 

	# Zero this before starting measurements 
	# Do this by taking arbitrary measured 0 point and key value in here
	pixel_center = 2692

	pixel_azimuth = x - pixel_center 

	# 14.93 pixels = 1 azimuth degree 
	if pixel_azimuth > 0: # Right half of image
		return round((pixel_azimuth/14.93),2) 

	elif pixel_azimuth < 0: # Left half of image
		return round((pixel_azimuth/14.93),2) + 360

	else: 
		return 0  

def extendImage(original_img):
	# Used to account for speaker image split across the two fish eyes lenses
	# getTruePosition still works since speaker will not be detected in x pixels > 5376

	left_extension = original_img[0:2688, 0:1000]
	extended_image = np.concatenate((original_img, left_extension), axis=1)
	return extended_image

	# References: 
	# http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
	# https://stackoverflow.com/questions/7589012/combining-two-images-with-opencv
		



# https://electronics.stackexchange.com/questions/36874/would-anyone-know-how-to-use-the-intersense-navchip-sensor-with-linux