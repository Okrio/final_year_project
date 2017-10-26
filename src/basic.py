import cv2
import numpy as np; 

# NIL argument used for trackbar creation 
def nothing(self): 
	pass 

# Initialise video feed
# Arg = 1 for alternative webcam 
cap = cv2.VideoCapture(0) 
cv2.namedWindow("Colourbars") 

# String assignment
hh = "High Hue"
lh = "Low Hue"
hs = "High Saturation"
ls = "Low Saturation"
hv = "High Value"
lv = "Low Value"
wnd = "Colourbars"

# Create trackbars for each HSV 
# H: 0-180
# S: 0-255
# V: 0-255
cv2.createTrackbar(lh, wnd, 0, 179, nothing)
cv2.createTrackbar(hh, wnd, 0, 179, nothing)
cv2.createTrackbar(ls, wnd, 0, 255, nothing)
cv2.createTrackbar(hs, wnd, 0, 255, nothing)
cv2.createTrackbar(lv, wnd, 0, 255, nothing)
cv2.createTrackbar(hv, wnd, 0, 255, nothing)

while(True): 
	# Capture frame by frame 
	ret, frame = cap.read() 

	# Apply blur and convert from BGR to HSV
	frame = cv2.GaussianBlur (frame, (5,5),0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 

	# Read trackbar values: 
	hul=cv2.getTrackbarPos(lh, wnd)
	huh=cv2.getTrackbarPos(hh, wnd)
	sal=cv2.getTrackbarPos(ls, wnd)
	sah=cv2.getTrackbarPos(hs, wnd)
	val=cv2.getTrackbarPos(lv, wnd)
	vah=cv2.getTrackbarPos(hv, wnd)

	# Array for final values: 
	HSVLOW=np.array([hul,sal,val])
	HSVHIGH=np.array([huh,sah,vah])

	# Threshold the HSV image to get desired colours
	mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)

	# Bitwise-AND mask the original image 
	res = cv2.bitwise_and(frame, frame, mask = mask)
	#res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

	# Detect circle 
	# circles = cv2.HoughCircles(res,cv2.HOUGH_GRADIENT, 1, 20, 
	# 			param1=50, param2=30, minRadius=0, maxRadius=0)

	# circles = np.uint16(np.around(circles)) 
	# for i in circles[0,:]: 
	# 	# Draw outer circle 
	# 	cv2.circle(res, (i[0],i[1]),i[2],(0,255,0),2)
	# 	# Draw centre of circle 
	# 	cv2.circle(res, (i[0],i[1]), 2, (0,0,255), 3)

	#Display resulting frame 
	cv2.imshow('frame', frame)
	cv2.imshow('mask', mask)
	cv2.imshow(wnd, res)
	#cv2.imshow('detected circles',res)
	if cv2.waitKey(1) & 0xFF == ord('q'): 
		break

# Release capture when done 
cap.release() 
cv2.destroyAllWindows() 




### References: 
# Creating slider bars in opencv:  
# https://botforge.wordpress.com/2016/07/02/basic-color-tracker-using-opencv-python/