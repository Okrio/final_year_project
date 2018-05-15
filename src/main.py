import toolbox as tb
import numpy as np
import cv2 

# Initialisation
source_img = 'images/process/raw_image.jpg'
cube_map = 'images/process/cube_map.jpg'
troubleshoot_flag = True

# Pre-processing:
tb.remapImage(source_img)
img = cv2.imread(cube_map, 1)
filtered_img = tb.filterColour(img)

# Detection: 
pixel_position, contourArea = tb.detectSpeaker(filtered_img, troubleshoot_flag)

# 


# Logging: 
cX, cY = pixel_position
print(tb.getTruePosition(pixel_position))

if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows() 
