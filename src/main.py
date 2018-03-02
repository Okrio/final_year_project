import toolbox as tb
import numpy as np
import cv2 

# Input Image: 
img = cv2.imread('mapping_images/0.JPG', 1)
img2 = cv2.imread('mapping_images/30.JPG', 1)
img3 = cv2.imread('mapping_images/60.JPG', 1)
img4 = cv2.imread('mapping_images/90.JPG', 1)
img5 = cv2.imread('mapping_images/120.JPG', 1)
img6 = cv2.imread('mapping_images/150.JPG', 1)
img7 = cv2.imread('mapping_images/180.JPG', 1)
img8 = cv2.imread('mapping_images/210.JPG', 1)
img9 = cv2.imread('mapping_images/240.JPG', 1)
img10 = cv2.imread('mapping_images/270.JPG', 1)
img11 = cv2.imread('mapping_images/300.JPG', 1)
img12 = cv2.imread('mapping_images/330.JPG', 1)

print("0: " + str(tb.detectSpeaker(img)) + " Expected: " + str(tb.getTruePosition(tb.detectSpeaker(img)))) 
print("30: " + str(tb.detectSpeaker(img2)) + " Expected: " + str(tb.getTruePosition(tb.detectSpeaker(img2)))) 
print("60: " + str(tb.detectSpeaker(img3)) + " Expected: " + str(tb.getTruePosition(tb.detectSpeaker(img3)))) 
print("90: " + str(tb.detectSpeaker(img4)) + " Expected: " + str(tb.getTruePosition(tb.detectSpeaker(img4)))) 
print("120: " + str(tb.detectSpeaker(img5)) + " Expected: " + str(tb.getTruePosition(tb.detectSpeaker(img5)))) 
print("150: " + str(tb.detectSpeaker(img6)) + " Expected: " + str(tb.getTruePosition(tb.detectSpeaker(img6)))) 
print("180: " + str(tb.detectSpeaker(img7)) + " Expected: " + str(tb.getTruePosition(tb.detectSpeaker(img7)))) 
#print("210: " + str(tb.detectSpeaker(img8)) + " Expected: " + str(tb.getTruePosition(tb.detectSpeaker(img8)))) 
print("240: " + str(tb.detectSpeaker(img9)) + " Expected: " + str(tb.getTruePosition(tb.detectSpeaker(img9)))) 
print("270: " + str(tb.detectSpeaker(img10)) + " Expected: " + str(tb.getTruePosition(tb.detectSpeaker(img10)))) 
print("300: " + str(tb.detectSpeaker(img11)) + " Expected: " + str(tb.getTruePosition(tb.detectSpeaker(img11)))) 
print("330: " + str(tb.detectSpeaker(img12)) + " Expected: " + str(tb.getTruePosition(tb.detectSpeaker(img12)))) 

# print("30: " + str(tb.detectSpeaker(img2))) 
# print("60: " + str(tb.detectSpeaker(img3))) 
# print("90: " + str(tb.detectSpeaker(img4))) 
# print("120: " + str(tb.detectSpeaker(img5))) 
# print("150: " + str(tb.detectSpeaker(img6))) 
# print("180: " + str(tb.detectSpeaker(img7))) 
# print("210: " + str(tb.detectSpeaker(img8))) 
# print("240: " + str(tb.detectSpeaker(img9)))
# print("270: " + str(tb.detectSpeaker(img10))) 
# print("300: " + str(tb.detectSpeaker(img11)))
# print("330: " + str(tb.detectSpeaker(img12))) 
   
if cv2.waitKey(0) & 0xFF == ord('q'):
	cv2.destroyAllWindows() 