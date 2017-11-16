import numpy as np 
import cv2 

cap = cv2.VideoCapture(0) 

# HSV Color Sensitivity Ranges 
# hul, huh = 147, 179 # Hue 
# sal, sah = 61, 191 # Saturation
# val, vah = 29, 205 # Value

hul, huh = 119, 179 # Hue 
sal, sah = 51, 243 # Saturation
val, vah = 0, 255 # Value

# Convert ranges into arrays for masking 
HSVLOW=np.array([hul,sal,val])
HSVHIGH=np.array([huh,sah,vah])

while (True): 
	ret, original_frame = cap.read() 
	status = "No Speaker Detected"

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
	
	# Sort contours by area 
	contours = sorted(contours, key = cv2.contourArea, reverse= True)[:5]

	# Loop over contours to find appropriate 
	for c in contours: 
		perimeter = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.1*perimeter, True)

		if len(approx) >= 4 and len(approx) <=6: 
			(x,y,w,h) = cv2.boundingRect(approx) 
			aspect_ratio = w/float(h) 

			area = cv2.contourArea(c)
			hullArea = cv2.contourArea(cv2.convexHull(c))
			solidity = area/float(hullArea)

			keepSolidity = solidity > 0.9 
			keepDims = w > 25 and h > 25
			keepAspectRatio = aspect_ratio >= 0.5 and aspect_ratio <=1.7 

			if keepAspectRatio and keepSolidity and keepDims: 
				cv2.drawContours(original_frame, [approx], -1, (0,0,255),2)
				status = str(aspect_ratio)


	# Display 
	cv2.putText(original_frame, status, (20,30), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)
	cv2.imshow('Original', original_frame)
	cv2.imshow('Edged', edged)
	
	if cv2.waitKey(1) & 0xFF == ord('q'): 
		break

cap.release() 
cv2.destroyAllWindows() 