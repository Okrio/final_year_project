import cv2
import numpy as np; 

# NIL argument used for trackbar creation 
def nothing(self): 
	pass 

# Initialise video feed
# Arg = 1 for alternative webcam 
cap = cv2.VideoCapture(0) 

# HSV Color Sensitivity Ranges 
hul, huh = 145, 164 # Hue 
sal, sah = 58, 182 # Saturation
val, vah = 165, 255 # Value

HSVLOW=np.array([hul,sal,val])
HSVHIGH=np.array([huh,sah,vah])

while(True): 
	# Capture frame by frame 
	ret, frame = cap.read() 

	# Apply blur and convert from BGR to HSV
	frame = cv2.GaussianBlur (frame, (5,5),0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 

	# Threshold the HSV image to get desired colours
	mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)
	ret, thresh = cv2.threshold(mask, 127, 255, 0)
	image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	mask = cv2.drawContours(mask, contours, -1, (0,255,0), 3)
	cv2.imshow('mask', mask)
	cv2.imshow('thres', thresh)



	# # Bitwise-AND mask the original image 
	# res = cv2.bitwise_and(frame, frame, mask = mask)

	# #Display resulting frame 
	# cv2.imshow('frame', frame)
	# cv2.imshow('mask', mask)
	# cv2.imshow('res', res)


	if cv2.waitKey(1) & 0xFF == ord('q'): 
		break

# Release capture when done 
cap.release() 
cv2.destroyAllWindows() 
