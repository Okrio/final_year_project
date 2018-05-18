import toolbox as tb
import numpy as np
import cv2 

calibration_img = 'images/process/perspective_calibration.png' 
source_img = 'images/process/raw_image.jpg'

# cv2.namedWindow('output_img', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('output_img', 1000, 800)

# Single Shot: 
# equ = tb.Equirectangular(calibration_img) 
# img = equ.GetPerspective(90, 90, 0, 1344, 1344) # Specify parameters(FOV, theta (azimuth), phi (inclination), height, width)
# cv2.imshow('output_img', img)

### Multi Shot: # Take all faces, edges and corners of cube 
fov = 90 
height = 1344
width = 1344

equ = tb.Equirectangular(calibration_img)
# Faces, Edges and Corners:
for theta in range (0, 360, 45): 
	for phi in range (-45, 90, 45): 
		print('Generating theta:' + str(theta) + ' phi: ' + str(phi) + ': ')
		imgOut = equ.GetPerspective(fov, theta, phi, height, width)
		cv2.imwrite('images/process/perspective/theta_' + str(theta) + '_phi_' + str(phi) + '.jpg', imgOut)
		
# Top and Bottom: 
for phi in range (-90, 180, 90):
	theta = 0
	print('Generating theta:' + str(theta) + ' phi: ' + str(phi) + ': ')
	imgOut = equ.GetPerspective(fov, theta, phi, height, width)
	cv2.imwrite('images/process/perspective/theta_' + str(theta) + '_phi_' + str(phi) + '.jpg', imgOut)

if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows() 

# Platonic Solid
# Fliege Nodes 
# http://ncmerge.sourceforge.net/