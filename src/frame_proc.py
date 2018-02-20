import numpy as np 
import cv2 

def nothing(self): 
	pass 

# Original Processing: 
img = cv2.imread('images/test_1.jpg', 1)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

cv2.namedWindow('output_edged', cv2.WINDOW_NORMAL)

# Canny Edge Trackbar 
cv2.createTrackbar('MinVal', 'output_edged', 0, 255, nothing)
cv2.createTrackbar('MaxVal', 'output_edged', 0, 255, nothing)

cv2.namedWindow('output_original', cv2.WINDOW_NORMAL)

# Canny Edge Values: 
sigma = 0.33
v = np.median(img)
lower = int(max(0, (1.0 - sigma) * v))
upper = int(min(255, (1.0 + sigma) * v))
# maxv = cv2.getTrackbarPos('MaxVal', 'output_edged') # 57

# Image Pre-processing: 
blurred = cv2.GaussianBlur(img, (5,5), 0)

while(1): 
	minv = cv2.getTrackbarPos('MinVal', 'output_edged') # 25 

	ret, th1 = cv2.threshold(blurred, minv, 255, cv2.THRESH_BINARY_INV)

	edged = cv2.Canny(th1, lower, upper)
	edged = cv2.dilate(edged, None, iterations=1)
	edged = cv2.erode(edged, None, iterations=1)

	# Contour Search 
	output, contours, hierarchy = cv2.findContours(
										edged, 
										cv2.RETR_EXTERNAL, 
										cv2.CHAIN_APPROX_NONE
										)

	#contours = sorted(contours, key = cv2.contourArea, reverse= True)[:5]
	for c in contours: 
		perimeter = cv2.arcLength(c, True)
		epsilon = 0.01*perimeter
		approx = cv2.approxPolyDP(c, epsilon, True)

		if len(approx) == 4:
			(x,y,w,h) = cv2.boundingRect(approx) 
			aspect_ratio = w/float(h) 
			area = cv2.contourArea(c)
			hullArea = cv2.contourArea(cv2.convexHull(c))
			solidity = area/float(hullArea)

			keepSolidity = solidity > 0.9 
			keepAspectRatio = aspect_ratio >= 0.8 and aspect_ratio <=1.2
			keepDims = w > 10 and h > 10

			if keepAspectRatio and keepSolidity and keepDims:
				cv2.drawContours(img, [approx], -1, (0,0,255),2)


	cv2.resizeWindow('output_edged', 1000, 800)
	cv2.imshow('output_edged', edged)

	cv2.resizeWindow('output_original', 1000, 800)
	cv2.imshow('output_original', img)

	if cv2.waitKey(1) & 0xFF == ord('q'): 
		break

cv2.destroyAllWindows() 


# Need to create a frame that is very high contrast 



