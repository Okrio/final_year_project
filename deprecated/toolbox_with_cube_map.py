######################################### Toolbox ######################################## 
import numpy as np
import cv2 

# For remap function
from numpy import pi
from PIL import Image
import sys

# For perspective shift function: 
import os

################ Global Variables ################
font = cv2.FONT_HERSHEY_SIMPLEX

################ Functions ################

######## Horizontal Plane Speaker Detection ########
def setEdgeParameters(img):
	# Description: Adaptive thresholds for Canny Edge Detection
	# Input: Image 
	# Output: Upper and Lower thresholds for Canny Edge Detection 

	sigma = 0.33 
	v = np.median(img) 
	lower_threshold = int(max(0, (1.0 - sigma) * v))
	upper_threshold = int(min(255, (1.0 + sigma) * v))

	return lower_threshold, upper_threshold 

def getPosition(contour):
	# Description: Obtains the x and y pixel of center of contour 
	# Input: Contour
	# Output: Pixel position of contour's center 

	M = cv2.moments(contour) 
	if M['m00']!=0: 
		cX = int(M['m10']/M['m00'])
		cY = int(M['m01']/M['m00'])
	else: 
		cX, cY = 0, 0
	return cX, cY 

def displayText(img, contour, pixel_threshold):
	# Description: Displays speaker's pixel position on screen 
	# Input: Image, contour, current_pixel_threshold 
	
	cX, cY = getPosition(contour) 
	position_text = "Speaker Position: " + str(getPosition(contour))
	cv2.putText(img, position_text, (cX, cY - 15), font, 0.5, (0,0,255), 2)
	cv2.putText(img, "x", (cX, cY), font, 0.5, (0, 255, 0), 1) 
	cv2.putText(img, str(pixel_threshold), (cX, cY - 30), font, 0.5, (0,0,255), 2)

def getTrueAzimuth(theta, phi, pixel_position): 
	# Description: Translates xy pixel positions along with camera directions into true azimuths 
	# Input: Camera direction and pixel positions in those directions 
	# Output: True Azimuth and Inclination

	# RICOH Theta Resolution: 5376x2688 pixels 
	x, y = pixel_position 
	pixel_center_x = 638 #653 #672 
	

	### Calculating Azimuth: 
	#14.93 pixels = 1 azimuth degree 
	pixel_azimuth = x - pixel_center_x 

	if theta == 0: # If looking directly forward 
		if pixel_azimuth > 0: # Right half of perspective 
			azimuth = round((pixel_azimuth/14.93), 2) 

		elif pixel_azimuth < 0: # Left half of perspective
			azimuth = round((pixel_azimuth/14.93), 2) + 360 

		else: 
			azimuth = theta 

	elif theta != 0: # If looking any other direction 
		if pixel_azimuth > 0: # Right half of perspective
			azimuth = round((pixel_azimuth/14.93), 2) + theta 

		elif pixel_azimuth < 0: # Left half of perspective
			azimuth = round((pixel_azimuth/14.93), 2) + theta 

		else: 
			azimuth = theta 

	return azimuth 

def getTrueElevation(theta, phi, pixel_position):
	x, y = pixel_position 
	pixel_center_y = 664 #675 #672 

	### Calculating Elevation: 
	# 14.93 pixels = 1 elevation degree 
	pixel_elevation = pixel_center_y - y # Since the pixel index starts from top to bottom

	if pixel_elevation > 0: # Top half of perspective 
		elevation = round((pixel_elevation/14.93), 2) + phi

	elif pixel_elevation < 0: # Bottom half of perspective 
		elevation = round((pixel_elevation/14.93), 2) + phi 

	else: 
		elevation = phi 

	return elevation

def extendImage(img):
	# Description: Used to account for speaker image split across the two ends of screen 
	# 			   getTruePosition still works since speaker will not be detected in x pixels > 5376
	# Input: Image
	# Output: Horizontally extended image 
	
	left_extension = img[0:2688, 0:1000]
	extended_img = np.concatenate((img, left_extension), axis=1)
	return extended_img

	# References: 
	# http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
	# https://stackoverflow.com/questions/7589012/combining-two-images-with-opencv

def filterSpeakerColour(img): 
	# Description: Applies a colour mask to filter out similar objects in image 
	# Input: Image 
	# Output: Mask 

	# Filter Values: 
	low_blue = 0
	low_green = 0
	low_red = 0
	high_blue = 255 # 135
	high_green = 137 # 146
	high_red = 73 # 26

	BGRLOW=np.array([low_blue, low_green, low_red])
	BGRHIGH=np.array([high_blue, high_green, high_red])

	#img = cv2.GaussianBlur (img, (5,5),0) # Blur image before masking 
	mask = cv2.inRange(img, BGRLOW, BGRHIGH) # Threshold the RGB image to get desired colours

	output_img = cv2.bitwise_and(img, img, mask = mask) # Bitwise-AND mask the original image 

	return output_img

def findSpeaker(contour): 
	# Description: Algorithm to find distinguish speaker contour 
	# Input: Contour
	# Output: foundSpeaker flag and contour 

	perimeter = cv2.arcLength(contour, True)
	epsilon = 0.01*perimeter 
	approx = cv2.approxPolyDP(contour, epsilon, True)

	if len(approx) == 4: 
		(x,y,w,h) = cv2.boundingRect(approx) 
		aspect_ratio = w/float(h) 
		area = cv2.contourArea(contour)
		hullArea = cv2.contourArea(cv2.convexHull(contour))
		solidity = area/float(hullArea)

		# Check for Flags: 
		keepSolidity = solidity > 0.9
		keepAspectRatio = aspect_ratio >= 0.95 and aspect_ratio <= 1.1
		keepDims = w > 50 and h > 50
 
		# Found Speaker: 
		if keepAspectRatio and keepSolidity and keepDims:
			return True, [approx]
		else: 
			return False, [] 
	else: 
		return False, []

def detectSpeaker(img, troubleshoot_flag): 
	# Description: Does a binary intensity sweep to detect and outline speaker in the image; 
	#			   Troubleshoot flag used to trigger canny edge and removes loop break after finding speaker
	# Input: Image, Troubleshoot Flag (True or False)
	# Output: Pixel position (1x2 array), Contour Area

	# Initialisation: 
	cv2.namedWindow('output_img', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('output_img', 1000, 800)

	if (troubleshoot_flag == True):
		cv2.namedWindow('output_edged', cv2.WINDOW_NORMAL) # Canny Edge Window Initialisation
		cv2.resizeWindow('output_edged', 1000, 800)
		cv2.namedWindow('filtered', cv2.WINDOW_NORMAL) # Colour Filter Window Initialisation
		cv2.resizeWindow('filtered', 1000, 800)

	pixel_threshold = 10 
	foundSpeaker = False 
	canny_low, canny_high = setEdgeParameters(img)

	# Image Pre-processing: 
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray_img, (5,5), 0)

	# Speaker Detection Loop: 
	# Troubleshooting Routine
	if (troubleshoot_flag == True): 
		while(pixel_threshold != 256):
			# Binary intensity sweep
			ret, th1 = cv2.threshold(blurred, pixel_threshold, 255, cv2.THRESH_BINARY_INV)

			# Canny Edge Detection post-binary sweep
			edged = cv2.Canny(th1, canny_low, canny_high)
			edged = cv2.dilate(edged, None, iterations = 1)
			edged = cv2.erode(edged, None, iterations = 1)

			# Display Canny Edge Changes 
			cv2.imshow('output_edged', edged)

			# Display filtered image
			cv2.imshow('filtered', img)

			# Find Contours: 
			output, contours, hierarchy = cv2.findContours(
												edged, 
												cv2.RETR_EXTERNAL, 
												cv2.CHAIN_APPROX_SIMPLE
												)
			# https://docs.opencv.org/3.4.0/d9/d8b/tutorial_py_contours_hierarchy.html

			# Loop through all contours to find possible contours of speaker
			for c in contours: 
				foundSpeaker, approx = findSpeaker(c) 

				if foundSpeaker: 
					cv2.drawContours(img, approx, -1, (0,0,255), 2)
					displayText(img, c, pixel_threshold)
					cv2.imshow('output_img', img)
					if 0xFF == ord('q'):
						break

			if pixel_threshold < 256: 
				pixel_threshold += 3

			if cv2.waitKey(1) & 0xFF == ord('q'): 
				break

	# Normal Routine
	elif (troubleshoot_flag == False): # Loop Breaks once Speaker is found
		while(foundSpeaker == False): 
			# Binary intensity sweep
			ret, th1 = cv2.threshold(blurred, pixel_threshold, 255, cv2.THRESH_BINARY_INV)
			
			# Canny Edge Detection post-binary sweep
			edged = cv2.Canny(th1, canny_low, canny_high)
			edged = cv2.dilate(edged, None, iterations = 1)
			edged = cv2.erode(edged, None, iterations = 1)

			# Finding and Drawing Contour: 
			output, contours, hierarchy = cv2.findContours(
												edged, 
												cv2.RETR_EXTERNAL, 
												cv2.CHAIN_APPROX_SIMPLE
												)
			# https://docs.opencv.org/3.4.0/d9/d8b/tutorial_py_contours_hierarchy.html

			for c in contours: 
				foundSpeaker, approx = findSpeaker(c) 

				if foundSpeaker: 
					cv2.drawContours(img, approx, -1, (0,0,255), 2)
					displayText(img, c, pixel_threshold)
					cv2.imshow('output_img', img)
					return getPosition(c)
					#return getPosition(c), cv2.contourArea(c)
					
			if pixel_threshold < 256: 
				pixel_threshold += 2 # Note that changing this will affect the break point

			if pixel_threshold == 256: 
				print('Speaker not found')
				return (None,None)

			# Used after analysing resulting image
			if cv2.waitKey(1) & 0xFF == ord('q'): 
				return (None, None)

######## Image Warping (For 360 Detection) ########

### For Perspective Shifts: 
# https://github.com/fuenwang/Equirec2Perspec
# http://paulbourke.net/miscellaneous/sphere2persp/

class Equirectangular:
    def __init__(self, img_name):
        self._img = cv2.imread(img_name, cv2.IMREAD_COLOR)
        [self._height, self._width, _] = self._img.shape
        #cp = self._img.copy()  
        #w = self._width
        #self._img[:, :w/8, :] = cp[:, 7*w/8:, :]
        #self._img[:, w/8:, :] = cp[:, :7*w/8, :]
    

    def GetPerspective(self, FOV, THETA, PHI, height, width, RADIUS = 128):
        #
        # THETA is left/right angle, PHI is up/down angle, both in degree
        #

        equ_h = self._height
        equ_w = self._width
        equ_cx = (equ_w - 1) / 2.0
        equ_cy = (equ_h - 1) / 2.0

        wFOV = FOV
        hFOV = float(height) / width * wFOV

        c_x = (width - 1) / 2.0
        c_y = (height - 1) / 2.0

        wangle = (180 - wFOV) / 2.0
        w_len = 2 * RADIUS * np.sin(np.radians(wFOV / 2.0)) / np.sin(np.radians(wangle))
        w_interval = w_len / (width - 1)

        hangle = (180 - hFOV) / 2.0
        h_len = 2 * RADIUS * np.sin(np.radians(hFOV / 2.0)) / np.sin(np.radians(hangle))
        h_interval = h_len / (height - 1)
        x_map = np.zeros([height, width], np.float32) + RADIUS
        y_map = np.tile((np.arange(0, width) - c_x) * w_interval, [height, 1])
        z_map = -np.tile((np.arange(0, height) - c_y) * h_interval, [width, 1]).T
        D = np.sqrt(x_map**2 + y_map**2 + z_map**2)
        xyz = np.zeros([height, width, 3], np.float)
        xyz[:, :, 0] = (RADIUS / D * x_map)[:, :]
        xyz[:, :, 1] = (RADIUS / D * y_map)[:, :]
        xyz[:, :, 2] = (RADIUS / D * z_map)[:, :]
        
        y_axis = np.array([0.0, 1.0, 0.0], np.float32)
        z_axis = np.array([0.0, 0.0, 1.0], np.float32)
        [R1, _] = cv2.Rodrigues(z_axis * np.radians(THETA))
        [R2, _] = cv2.Rodrigues(np.dot(R1, y_axis) * np.radians(-PHI))

        xyz = xyz.reshape([height * width, 3]).T
        xyz = np.dot(R1, xyz)
        xyz = np.dot(R2, xyz).T
        lat = np.arcsin(xyz[:, 2] / RADIUS)
        lon = np.zeros([height * width], np.float)
        theta = np.arctan(xyz[:, 1] / xyz[:, 0])
        idx1 = xyz[:, 0] > 0
        idx2 = xyz[:, 1] > 0

        idx3 = ((1 - idx1) * idx2).astype(np.bool)
        idx4 = ((1 - idx1) * (1 - idx2)).astype(np.bool)
        
        lon[idx1] = theta[idx1]
        lon[idx3] = theta[idx3] + np.pi
        lon[idx4] = theta[idx4] - np.pi

        lon = lon.reshape([height, width]) / np.pi * 180
        lat = -lat.reshape([height, width]) / np.pi * 180
        lon = lon / 180 * equ_cx + equ_cx
        lat = lat / 90 * equ_cy + equ_cy
        #for x in range(width):
        #    for y in range(height):
        #        cv2.circle(self._img, (int(lon[y, x]), int(lat[y, x])), 1, (0, 255, 0))
        #return self._img 
    
        persp = cv2.remap(self._img, lon.astype(np.float32), lat.astype(np.float32), cv2.INTER_CUBIC, borderMode=cv2.BORDER_WRAP)
        return persp

def scanPerspectives(img, troubleshoot_flag): 
	# Description: Generates images of the perspective of a virtual camera at the middle of a sphere
	# Input: Image 
	# Output: Perspective images 

	fov = 90 
	height = 1344
	width = 1344 
	phi = 0 

	# Initialising list of azimuths and elevations obtained from different perspectives
	azimuth = [] 
	elevation = []  

	# Generate map:
	equ = Equirectangular(img)

	# Scan image: 
	# Faces, Edges and Corners:
	for theta in range (0, 360, 45): 
		for phi in range (-45, 90, 45):
			imgOut = equ.GetPerspective(fov, theta, phi, height, width)
			if (troubleshoot_flag == True): 
				cv2.namedWindow('imgOut', cv2.WINDOW_NORMAL) # Canny Edge Window Initialisation
				cv2.resizeWindow('imgOut', 1000, 800)
				cv2.imshow('imgOut', imgOut)
			pixel_position = detectSpeaker(imgOut, False)
			# pixel_position = detectMarker(imgOut)

			if pixel_position != (None, None): 
				print('Speaker found when facing azimuth: ' + str(theta) + ' and inclination: ' + str(phi))
				azimuth.append(getTrueAzimuth(theta, phi, pixel_position)) 
				elevation.append(getTrueElevation(theta, phi, pixel_position))
	
	# Top and Bottom: 
	for phi in range (-90, 180, 90):
		theta = 0
		imgOut = equ.GetPerspective(fov, theta, phi, height, width)
		pixel_position = detectSpeaker(imgOut, False)
		# pixel_position = detectMarker(imgOut)

		if pixel_position != (None, None): 
			print('Speaker found when facing azimuth: ' + str(theta) + ' and inclination: ' + str(phi))
			azimuth.append(getTrueAzimuth(theta, phi, pixel_position)) 
			elevation.append(getTrueElevation(theta, phi, pixel_position))


	# Return true averaged position: 
	if len(azimuth) > 1: 
		true_azimuth = round(sum(azimuth)/len(azimuth), 2) 
	else: 
		true_azimuth = azimuth[0]  

	if len(elevation) > 1: 
		true_elevation = round(sum(elevation)/len(elevation), 2)
	else: 
		true_elevation = elevation[0] 

	return true_azimuth, true_elevation


### For Cube Map: 
def genMapData(image_width): 
	# Description: Generates the coordinates to remap equirectangular image into a cube map (Feeder for remapImage function)
	# Input: Image width
	# Output: Cube map coordinates

	in_size = [image_width, image_width * 3 / 4]
	edge = in_size[0]/4 # The length of each edge in pixels

	# Create our np arrays
	out_pix = np.zeros((in_size[1], in_size[0], 2), dtype="f4")
	xyz = np.zeros((in_size[1] * in_size[0] / 2, 3), dtype="f4")
	vals = np.zeros((in_size[1] * in_size[0] / 2, 3), dtype="i4")

	# Much faster to use an arange when we assign to to vals
	start, end = 0, 0
	rng_1 = np.arange(0, edge * 3)
	rng_2 = np.arange(edge, edge * 2)

	for i in xrange(in_size[0]):
		# 0: back
		# 1: left
		# 2: front
		# 3: right
		face = int(i / edge)
		rng = rng_1 if face == 2 else rng_2

		end += len(rng)
		vals[start:end, 0] = rng
		vals[start:end, 1] = i
		vals[start:end, 2] = face
		start = end

	# Top/bottom are special conditions
	j, i, face = vals.T
	face[j < edge] = 4  # top
	face[j >= 2 * edge] = 5  # bottom

	# Convert to image xyz
	a = 2.0 * i / edge
	b = 2.0 * j / edge
	one_arr = np.ones(len(a))
	for k in range(6):
		face_idx = face == k

		# Using the face_idx version of each is 50% quicker
		one_arr_idx = one_arr[face_idx]
		a_idx = a[face_idx]
		b_idx = b[face_idx]

		if k == 0:
			vals_to_use =  [-one_arr_idx, 1.0 - a_idx, 3.0 - b_idx]
		elif k == 1:
			vals_to_use =  [a_idx - 3.0, -one_arr_idx, 3.0 - b_idx]
		elif k == 2:
			vals_to_use =  [one_arr_idx, a_idx - 5.0, 3.0 - b_idx]
		elif k == 3:
			vals_to_use =  [7.0 - a_idx, one_arr_idx, 3.0 - b_idx]
		elif k == 4:
			vals_to_use =  [b_idx - 1.0, a_idx - 5.0, one_arr_idx]
		elif k == 5:
			vals_to_use =  [5.0 - b_idx, a_idx - 5.0, -one_arr_idx]

		xyz[face_idx] = np.array(vals_to_use).T

	# Convert to theta and pi
	x, y, z = xyz.T
	theta = np.arctan2(y, x)
	r = np.sqrt(x**2 + y**2)
	phi = np.arctan2(z, r)

	# Source img coords
	uf = (2.0 * edge * (theta + pi) / pi) % in_size[0]
	uf[uf==in_size[0]] = 0.0 # Wrap to pixel 0 (much faster than modulus)
	vf = (2.0 * edge * (pi / 2 - phi) / pi)

	# Mapping matrix
	out_pix[j, i, 0] = vf
	out_pix[j, i, 1] = uf

	map_x_32 = out_pix[:, :, 1]
	map_y_32 = out_pix[:, :, 0]
	return map_x_32, map_y_32

def remapImage(img): 
	# Generates a cube map image from an equirectangular image 
	# Input: Image 
	# Output: Cubemap Image.jpg

	imgIn = Image.open(img)
	inSize = imgIn.size 

	map_x_32, map_y_32 = genMapData(inSize[0])
	cubemap = cv2.remap(np.array(imgIn), map_x_32, map_y_32, cv2.INTER_LINEAR)

	imgOut = Image.fromarray(cubemap)
	imgOut.save("images/process/cube_map.jpg")

	# References: 
	# https://pastebin.com/Eeki92Zv (key source)
	# https://stackoverflow.com/questions/29678510/convert-21-equirectangular-panorama-to-cube-map (explanation)
	# https://github.com/bingsyslab/360projection


# Unwarping: 
# https://hackaday.io/project/12384-autofan-automated-control-of-air-flow/log/41862-correcting-for-lens-distortions
# https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/

