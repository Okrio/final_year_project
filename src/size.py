import numpy as np 
import cv2 

cap = cv2.VideoCapture(0)

# HSV Color Sensitivity Ranges 
hul, huh = 145, 164 # Hue 
sal, sah = 58, 182 # Saturation
val, vah = 165, 255 # Value

HSVLOW=np.array([hul,sal,val])
HSVHIGH=np.array([huh,sah,vah])

while(True): 
	ret, frame = cap.read() 
	frame = cv2.GaussianBlur (frame, (5,5),0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
	mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)

	imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(imgray, 127, 255,0 )

	edged = cv2.Canny(mask, 50, 100)
	edged = cv2.dilate(edged, None, iterations=1)
	edged = cv2.erode(edged, None, iterations=1)

	frame, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	output = cv2.drawContours(frame, contours, -1, (0,255,0), 3)

	cv2.imshow('edged', edged)
	cv2.imshow('frame', frame)



	#ret, thresh = cv2.threshold(imgray, 127, 255,0 )
	# frame, contours, hierarchy = cv2.findContours(edged,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# cv2.drawContours(output, contours, -1, (0,255,0), 3)
	# cv2.imshow('output', output)
	# cv2.imshow('frame', frame)


	# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# gray = cv2.GaussianBlur(gray, (7,7),0) 

	# edged = cv2.Canny(gray, 50, 100)
	# edged = cv2.dilate(edged, None, iterations=1)
	# edged = cv2.erode(edged, None, iterations=1)

	# #cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

	# cnts, hierarchy = cv2.findContours(edged, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	# output = cv2.drawContours(frame, cnts, -1, (0,255,0),3)

	# cv2.imshow('output', output)

	if cv2.waitKey(1) & 0xFF == ord('q'): 
		break

# Release capture when done 
cap.release() 
cv2.destroyAllWindows() 
