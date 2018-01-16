import toolbox as tb
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

# Start Video Analysis
while (True):
	ret, frame = cap.read()
	 
	detected_text = "Speaker Not Found"
	position_text = "Position Unavailable"

	c, approx, moments = tb.findSpeaker(frame, HSVLOW, HSVHIGH)

	isDetected = len(c) and len(approx) 

	if isDetected: 
		cv2.drawContours(frame, [approx], -1, (0,0,255),2)
		speakerPosition = tb.getPosition(moments) 

		# Update Display
		detected_text = "Speaker Detected"
		position_text = "Speaker Position: " + str(speakerPosition) 
		cv2.putText(frame, "x", speakerPosition, font, 0.5, (0, 255, 0), 1)

	tb.displayText(frame, detected_text, position_text)
	cv2.imshow('Original', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'): 
		break

cap.release() 
cv2.destroyAllWindows() 