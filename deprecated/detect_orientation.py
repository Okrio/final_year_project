import toolbox as tb
import numpy as np
import cv2 

font = cv2.FONT_HERSHEY_SIMPLEX

def filterColour(img): 
	# Description: Applies a colour mask to filter out similar objects in image 
	# Input: Image 
	# Output: Mask 

	# Filter Values: 
	low_blue = 0
	low_green = 0
	low_red = 0
	high_blue = 075
	high_green = 052
	high_red = 143 

	BGRLOW=np.array([low_blue, low_green, low_red])
	BGRHIGH=np.array([high_blue, high_green, high_red])

	#img = cv2.GaussianBlur (img, (5,5),0) # Blur image before masking 
	mask = cv2.inRange(img, BGRLOW, BGRHIGH) # Threshold the RGB image to get desired colours

	output_img = cv2.bitwise_and(img, img, mask = mask) # Bitwise-AND mask the original image 

	return output_img

def displayText(img, contour):
	# Description: Displays speaker's pixel position on screen 
	# Input: Image, contour, current_pixel_threshold 
	
	cX, cY = getPosition(contour) 
	position_text = "Speaker Position: " + str(getPosition(contour))
	cv2.putText(img, position_text, (cX, cY - 15), font, 0.5, (0,0,255), 2)
	cv2.putText(img, "x", (cX, cY), font, 0.5, (0, 255, 0), 1) 

def getPosition(contour):
	# Description: Obtains the x and y pixel of center of contour 
	# Input: Contour
	# Output: Pixel position of contour's center 

	M = cv2.moments(contour) 
	if M['m00']!=0: 
		cX = int(M['m10']/M['m00'])
		cY = int(M['m01']/M['m00'])
	else: 
		cX, cY = 0, 0
	return cX, cY 

def setEdgeParameters(img):
	# Description: Adaptive thresholds for Canny Edge Detection
	# Input: Image 
	# Output: Upper and Lower thresholds for Canny Edge Detection 

	sigma = 0.33 
	v = np.median(img) 
	lower_threshold = int(max(0, (1.0 - sigma) * v))
	upper_threshold = int(min(255, (1.0 + sigma) * v))

	return lower_threshold, upper_threshold 

source_img = 'images/process/raw_image.jpg'

img = cv2.imread(source_img, 1)
filtered = filterColour(img)
cv2.imwrite('images/process/filtered_image.jpg', filtered)

filtered_img = 'images/process/filtered_image.jpg'
filtered_imgIn = cv2.imread(filtered_img, 1)

gray_img = cv2.cvtColor(filtered_imgIn, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray_img, (5,5) , 0)

canny_low, canny_high = setEdgeParameters(filtered_imgIn)

pixel_threshold = 10

cv2.namedWindow('edged', cv2.WINDOW_NORMAL)
cv2.resizeWindow('edged', 1000, 800)

while(pixel_threshold != 256):
	print(pixel_threshold) 
	ret, th1 = cv2.threshold(filtered, pixel_threshold, 255, cv2.THRESH_BINARY_INV)

	edged = cv2.Canny(th1, canny_low, canny_high)
	edged = cv2.dilate(edged, None, iterations = 1)
	edged = cv2.erode(edged, None, iterations = 1)

	cv2.imshow('edged', filtered_imgIn)

	output, contours, hierarchy = cv2.findContours(
											edged, 
											cv2.RETR_EXTERNAL,
											cv2.CHAIN_APPROX_SIMPLE
											)
	for c in contours: 
		perimeter = cv2.arcLength(c, True)
		epsilon = 0.01*perimeter
		approx = cv2.approxPolyDP(c, epsilon, True)

		if len(approx) == 4: 
			(x,y,w,h) = cv2.boundingRect(approx)
			area = cv2.contourArea(c)
			aspect_ratio = w/float(h)
			hullArea = cv2.contourArea(cv2.convexHull(c))
			solidity = area/float(hullArea)

			keepSolidity = solidity > 0.9
			keepDims = w > 50 and h > 50
			keepAspectRatio = aspect_ratio >= 0.01 and aspect_ratio <= 0.7

			if keepSolidity and keepDims and keepAspectRatio: 
				cv2.drawContours(img, approx, -1, (0,0,255), 2)
				displayText(img, c) 
				cv2.namedWindow('imgOut', cv2.WINDOW_NORMAL)
				cv2.resizeWindow('imgOut', 1000, 800)
				cv2.imshow('imgOut', img)

	if pixel_threshold < 256: 
		pixel_threshold += 2

if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows() 