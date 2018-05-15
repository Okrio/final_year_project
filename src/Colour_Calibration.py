import cv2
import numpy as np; 

# NIL argument used for trackbar creation 
def nothing(self): 
	pass 

# Initialise video feed
# Arg = 1 for alternative webcam 
cap = cv2.VideoCapture(0) 
source_img = 'images/process/cube_map.jpg'
cv2.namedWindow('Colourbars', cv2.WINDOW_NORMAL) 
cv2.resizeWindow('Colourbars', 1000, 800)

# String assignment
hb = "High Blue"
lb = "Low Blue"
hg = "High Green"
lg = "Low Green"
hr = "High Red"
lr = "Low Red"
wnd = "Colourbars"

# Create trackbars for each HSV 
# H: 0-180
# S: 0-255
# V: 0-255
cv2.createTrackbar(lr, wnd, 0, 255, nothing)
cv2.createTrackbar(hr, wnd, 0, 255, nothing)
cv2.createTrackbar(lg, wnd, 0, 255, nothing)
cv2.createTrackbar(hg, wnd, 0, 255, nothing)
cv2.createTrackbar(lb, wnd, 0, 255, nothing)
cv2.createTrackbar(hb, wnd, 0, 255, nothing)

while(True): 
	# Capture frame by frame 
	ret, frame = cap.read() 
	#frame = cv2.imread(source_img, 1)

	# Apply blur and convert from BGR to HSV
	# blurred = cv2.GaussianBlur (frame, (5,5),0)
	# hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 

	# Read trackbar values: 
	rl=cv2.getTrackbarPos(lr, wnd)
	rh=cv2.getTrackbarPos(hr, wnd)
	gl=cv2.getTrackbarPos(lg, wnd)
	gh=cv2.getTrackbarPos(hg, wnd)
	bl=cv2.getTrackbarPos(lb, wnd)
	bh=cv2.getTrackbarPos(hb, wnd)

	# Array for final values: 
	BGRLOW=np.array([bl,gl,rl])
	BGRHIGH=np.array([bh,gh,rh])

	# Threshold the RGB image to get desired colours
	mask = cv2.inRange(frame, BGRLOW, BGRHIGH)

	# Bitwise-AND mask the original image 
	res = cv2.bitwise_and(frame, frame, mask = mask)

	#Display resulting frame 
	#cv2.imshow('frame', frame)
	#cv2.imshow('mask', mask)
	cv2.imshow(wnd, res)
	if cv2.waitKey(1) & 0xFF == ord('q'): 
		break

# Release capture when done 
cap.release() 
cv2.destroyAllWindows() 
