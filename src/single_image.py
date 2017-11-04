import numpy as np 
import cv2 

# HSV Color Sensitivity Ranges 
hul, huh = 145, 164 # Hue 
sal, sah = 58, 182 # Saturation
val, vah = 165, 255 # Value

# Convert ranges into arrays for masking 
HSVLOW=np.array([hul,sal,val])
HSVHIGH=np.array([huh,sah,vah])

# Load image: 
source_img = cv2.imread('source_img.jpg')

### Image Processing: 

# Colour Mask 
blurred = cv2.GaussianBlur(source_img, (5,5),0)
hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, HSVLOW, HSVHIGH) 

# Edge Detetction
edged = cv2.Canny(mask, 50, 150)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# Find and Draw Contours 
output, contours, hierarchy = cv2.findContours(edged,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cnt = contours[0] # Choosing the first set of contours 
(x,y),radius = cv2.minEnclosingCircle(cnt)
print("x,y coordinates: ", x, y)
print("area of contour: ", cv2.contourArea(cnt))

# Draw approx-circle
center = (int(x),int(y))
radius = int(radius)
cv2.circle(source_img, center,radius,(0,255,0),2) 


# Can find area to number of non 0 pixels of contrasting it against a black background 

#cv2.drawContours(source_img, contours, 0, (0,255,0), 2)

#cv2.drawContours(source_img, contours, 3, (0,0,255), 2)
# arg 1: Draw contours on frame 
# arg 2: List of contours found 
# arg 3: -1: All contours 
# arg 4: Colour of contours 
# arg 5: Thickness of contours 

# Determine size of area inside contour 
#area = cv2.contourArea(contours)

# # Determine the pixels inside contour 
# for c in contours: 
# 	#(x, y), radius = cv2.minEnclosingCircle(c)
# 	print ('contours detected are: ', c)
# 	print ('contour area: ', cv2.contourArea(c))

### Displays 
cv2.imshow('contours', source_img)
cv2.imshow('edged', edged)

### End Output 
cv2.waitKey(0)
cv2.destroyAllWindows()
