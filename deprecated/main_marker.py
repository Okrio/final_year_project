import toolbox as tb
import numpy as np
import cv2 
import glob

### Single image detection
source_img = 'images/process/raw_image.jpg'

troubleshoot_flag = True

# Pre-processing: 
img = cv2.imread(source_img, 1)
filtered = tb.filterMarkerColour(img)
cv2.imwrite('images/process/filtered_image.jpg', filtered)

# Scan Images: 
filtered_img = 'images/process/filtered_image.jpg'

azimuth, elevation = tb.scanPerspectives(filtered_img, troubleshoot_flag) 
print('Azimuth: ' + str(azimuth) + ' Elevation: ' + str(elevation))

if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows() 