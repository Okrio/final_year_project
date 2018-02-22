############### Toolbox ############## 
import numpy as np
import cv2 

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
		keepSolidity = solidity > 0.9 
		keepAspectRatio = aspect_ratio >= 0.8 and aspect_ratio <=1.2
		keepDims = w > 10 and h > 10

		print(keepSolidity, keepAspectRatio, keepDims) 

		# Found Speaker: 
		if keepAspectRatio and keepSolidity and keepDims:
			return True, [approx]
		else: 
			return False, [] 
	else: 
		return False, []

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