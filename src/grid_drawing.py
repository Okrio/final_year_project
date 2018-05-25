# Draws a grid at each azimuth and inclination 

import numpy as np 
import cv2 

source_img = 'images/process/157_az_35.9_el.jpg'
red = [0, 0, 255]
blue = [255, 0, 0]
green = [0, 255, 0]
thickness = 2

# RICOH Theta Resolution: 5376x2688 pixels 

img = cv2.imread(source_img, 1)
center_x = 5376/2
center_y = 2688/2 

# Origin Line: 
cv2.line(img, (center_x,0), (center_x, 2688), red, 5)
cv2.line(img, (0, center_y), (5376, center_y), red, 5)

# Draw grids every 5 degrees: 
for x_grid in range(0, 360, 10):
	x_pixels = int(round(x_grid*14.93, 1))
	cv2.line(img, (x_pixels, 0), (x_pixels, 2688), blue, thickness)

for y_grid in range(0, 180, 10): 
	y_pixels = int(round(y_grid*14.93, 1))
	cv2.line(img, (0, y_pixels), (5376, y_pixels), green, thickness)


cv2.namedWindow('output_img', cv2.WINDOW_NORMAL)
cv2.resizeWindow('output_img', 1000, 500)
cv2.imshow('output_img', img)

if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows() 