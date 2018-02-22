import numpy as np 
import cv2 

def prepareFrame(input_frame, HSVLOW, HSVHIGH): 
	blurred = cv2.GaussianBlur(input_frame, (5,5), 0)
	mask = cv2.inRange(cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV), HSVLOW ,HSVHIGH)
	edged = cv2.Canny(mask, 50, 150)
	edged = cv2.dilate(edged, None, iterations=1)
	edged = cv2.erode(edged, None, iterations=1)
	return edged

def findSpeaker(frame, HSVLOW, HSVHIGH):
	edged = prepareFrame(frame, HSVLOW, HSVHIGH)
	output, contours, hierarchy = cv2.findContours(
										edged, 
										cv2.RETR_EXTERNAL, 
										cv2.CHAIN_APPROX_SIMPLE
										)
	# Sort largest 5 contours
	contours = sorted(contours, key = cv2.contourArea, reverse= True)[:5]

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

			keepSolidity = solidity > 0.9 
			keepDims = w > 50 and h > 50 # Speaker should be larger than 50x50 pixels in room
			keepAspectRatio = aspect_ratio >= 0.8 and aspect_ratio <=1.2 # Approximately square

			M = cv2.moments(c) 

			if keepAspectRatio and keepSolidity and keepDims:
				return c, approx, M 

			else:
				return [], [], [] # Return empty arrays
		else: 
			return [], [], []

def getPosition(imageMoment):
	if imageMoment['m00'] != 0: 
		cX = int(imageMoment['m10']/imageMoment['m00'])
		cY = int(imageMoment['m01']/imageMoment['m00'])
	else: 
		cX, cY = 0, 0

	speakerPosition = cX, cY

	return speakerPosition

def displayText(frame, detected_text, position_text): 
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(frame, detected_text, (20,30), font, 0.5, (0,0,255), 1)
	cv2.putText(frame, position_text, (20,60), font, 0.5, (0,255,0), 1)
