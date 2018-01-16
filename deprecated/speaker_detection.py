import numpy as np 
import cv2 

# User defined variables 
font = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(0) 

# Mask Colour Ranges:
hul, huh = 119, 179 # Hue 
sal, sah = 51, 243 # Saturation
val, vah = 0, 255 # Value

# Convert ranges into arrays for masking 
HSVLOW=np.array([hul,sal,val])
HSVHIGH=np.array([huh,sah,vah])

while (True): 
	ret, original_frame = cap.read() 

	# Status and printouts
	detected_status = "No Speaker Detected"
	aspect_ratio_text = "Aspect Ratio Unavailable"
	size_text = "Size Unavailable"
	position_text = "Position Unavailable"

	# Image Processing 
	blurred = cv2.GaussianBlur(original_frame,(5,5),0)
	mask = cv2.inRange(cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV), HSVLOW ,HSVHIGH) 

	edged = cv2.Canny(mask, 50, 150)
	edged = cv2.dilate(edged, None, iterations=1)
	edged = cv2.erode(edged, None, iterations=1)

	# Find Contours 
	output, contours, hierarchy = cv2.findContours(
											edged, 
											cv2.RETR_EXTERNAL, 
											cv2.CHAIN_APPROX_SIMPLE
											)
	
	# Sort contours with the 5 largest areas
	contours = sorted(contours, key = cv2.contourArea, reverse= True)[:5]

	# Loop over contours to find appropriate 
	for c in contours: 
		perimeter = cv2.arcLength(c, True)
		epsilon = 0.05*perimeter # Larger value allows for higher tolerances for bad shapes
		approx = cv2.approxPolyDP(c, epsilon, True)
 
		if len(approx) >= 4 and len(approx) <= 6: # Checks for number of vertices 
		# Due to gaussian and motion blur, although looking for a square, may not actually get a square
			(x,y,w,h) = cv2.boundingRect(approx) 
			aspect_ratio = w/float(h) 

			area = cv2.contourArea(c)
			hullArea = cv2.contourArea(cv2.convexHull(c))
			solidity = area/float(hullArea)
			M = cv2.moments(c) 

			# Calculate Center of Contour/Speaker's Position in Pixels
			if M['m00']!=0: 
				cX = int(M['m10']/M['m00'])
				cY = int(M['m01']/M['m00'])
			else: 
				cX, cY = 0, 0

			# To Calibrate: 
			# https://docs.opencv.org/trunk/da/dc1/tutorial_js_contour_properties.html
			keepSolidity = solidity > 0.9 
			keepDims = w > 50 and h > 50 # Speaker should be larger than 50x50 pixels in room
			keepAspectRatio = aspect_ratio >= 0.8 and aspect_ratio <=1.2 # Approximately square
			speakerPosition = cX, cY 

			if keepAspectRatio and keepSolidity and keepDims: 
				cv2.drawContours(original_frame, [approx], -1, (0,0,255),2) 
				detected_status = "Speaker Detected"
				aspect_ratio_text = "Aspect Ratio: " + str(aspect_ratio)
				size_text = "Area: " + str(area) 
				position_text = "Speaker Position: " + str(speakerPosition) 
				cv2.putText(original_frame, "x", speakerPosition, font, 0.5, (0, 255, 0), 1) 

	# Display 
	cv2.putText(original_frame, detected_status, (20,30), font, 0.5,(0,0,255), 1)
	cv2.putText(original_frame, aspect_ratio_text, (20,60), font, 0.5,(255,0,0), 1)
	cv2.putText(original_frame, size_text, (20, 90), font, 0.5, (0, 255, 0), 1)
	cv2.putText(original_frame, position_text, (20, 120), font, 0.5, (255, 255, 255), 1)

	cv2.imshow('Original', original_frame)
	cv2.imshow('Edged', edged)
	
	if cv2.waitKey(1) & 0xFF == ord('q'): 
		break

cap.release() 
cv2.destroyAllWindows() 