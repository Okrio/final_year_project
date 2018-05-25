import toolbox as tb
import numpy as np
import cv2 
import glob

# ### Looping through whole folder: 
# troubleshoot_flag = False 
# filenames = glob.glob('images/909b_out_of_plane_optical_calibration/out_of_plane_calibration_results/elevation_20/*.jpg')
# filenames.sort() 
# for source_img in filenames: 
# 	print('file is:' + str(source_img))
# 	img = cv2.imread(source_img, 1)
# 	filtered = tb.filterColour(img)
# 	cv2.imwrite('images/process/filtered_image.jpg', filtered)

# 	# Scan Images:
# 	filtered_img = 'images/process/filtered_image.jpg'

# 	azimuth, elevation = tb.scanPerspectives(filtered_img) 
# 	print('Azimuth: ' + str(azimuth) + ' Elevation: ' + str(elevation))

# if cv2.waitKey(0) & 0xFF == ord('q'):
# 	cv2.destroyAllWindows() 


### Single image detection
source_img = 'images/process/157_az_35.9_el.jpg'

troubleshoot_flag = True

# Pre-processing: 
img = cv2.imread(source_img, 1)
filtered = tb.filterSpeakerColour(img)
cv2.imwrite('images/process/filtered_image.jpg', filtered)

# Scan Images: 
filtered_img = 'images/process/filtered_image.jpg'

azimuth, elevation = tb.scanPerspectives(filtered_img, troubleshoot_flag) 
print('Azimuth: ' + str(azimuth) + ' Elevation: ' + str(elevation))

if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows() 



# # Detection: 
# filenames = glob.glob('images/perspective/*.jpg')
# filenames.sort() 
# print(filenames)
# perspectives = [cv2.imread(img) for img in filenames]
# # https://stackoverflow.com/questions/38675389/python-opencv-how-to-load-all-images-from-folder-in-alphabetical-order?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
