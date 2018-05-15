import toolbox as tb
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
		keepAspectRatio = aspect_ratio >= 0.8 and aspect_ratio <= 1.2 # To account for warping outside horizontal plane
		keepDims = w > 50 and h > 50 # If cannot detect, adjust this! 

		# Found Speaker: 
		if keepAspectRatio and keepSolidity and keepDims:
			return True, [approx]
		else: 
			return False, [] 
	else: 
		return False, []

img = cv2.imread('images/cube_map.jpg', 1)
pixel_threshold = 10 

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray_img, (5,5), 0)

canny_low, canny_high = setEdgeParameters(img)

# Set Up Windows: 
cv2.namedWindow('output_edged', cv2.WINDOW_NORMAL)
cv2.namedWindow('output_img', cv2.WINDOW_NORMAL)

while (pixel_threshold != 255):
	# Binary intensity sweep
	ret, th1 = cv2.threshold(blurred, pixel_threshold, 255,
		cv2.THRESH_BINARY_INV)
	
	# Canny Edge Detection post-binary sweep
	edged = cv2.Canny(th1, canny_low, canny_high)
	edged = cv2.dilate(edged, None, iterations = 1)
	edged = cv2.erode(edged, None, iterations = 1)

	# Display Canny Edge Changes 
	cv2.resizeWindow('output_edged', 1000, 800)
	cv2.imshow('output_edged', edged)

	output, contours, hierarchy = cv2.findContours(
									edged, 
									cv2.RETR_EXTERNAL, 
									cv2.CHAIN_APPROX_SIMPLE
									)

	for c in contours: 
		foundSpeaker, approx = findSpeaker(c) 

		if foundSpeaker: 
			cv2.drawContours(img, approx, -1, (0,0,255), 2)
			cv2.resizeWindow('output_img', 1000, 800)
			cv2.imshow('output_img', img)

	pixel_threshold += 1

if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows() 