import cv2
import numpy as np

image = cv2.imread('./ha2.JPG')
# scale = 500 / image_raw.shape[1]
# image = cv2.resize(image_raw, dsize=None, fx=scale, fy=scale)
image_bgra = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Extrat background(white)
hsv_min = np.array([0,0,0])
hsv_max = np.array([180,40,255])
background = cv2.inRange(image_hsv, hsv_min, hsv_max)   # background area.

# Reverse select area.
background_not = cv2.bitwise_not(background)
# Detect contours.
contours, _ = cv2.findContours(background_not, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create blank image, of which size is same as original image.
mask = np.zeros(image_bgra.shape[:2], dtype=np.uint8)
# Fill contours area for 255(white).
cv2.drawContours(mask, contours, contourIdx=-1, color=255, thickness=-1)    # contourIdx=-1: Select all contours. thickness=-1: Fill contours.

# Erase background using mask which is not background area.
print('finish')
bgra = cv2.bitwise_and(image_bgra, image_bgra, mask=mask)
cv2.imwrite('ha2.png', bgra)