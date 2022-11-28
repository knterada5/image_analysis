import imghdr
import cv2
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
import sys
import os
args = sys.argv

path = os.path.abspath(args[1])
img = cv2.imread(path)
scale = 500 / img.shape[1]
img_scale = cv2.resize(img, dsize=None, fx=scale, fy=scale)
cv2.imshow('b', img_scale)
cv2.waitKey(1)

b, g, r = cv2.split(img_scale)
fig = plt.figure(figsize=(10, 9))
axis = fig.add_subplot(1,1,1, projection='3d')

pixel_colors = img_scale.reshape((np.shape(img_scale)[0]*np.shape(img_scale)[1], 3))
norm = colors.Normalize(vmin=-1., vmax=1.)
norm.autoscale(pixel_colors)
pixel_colors = norm(pixel_colors).tolist()

# axis.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=pixel_colors, marker=".")
# axis.set_xlabel("Red")
# axis.set_ylabel("Green")
# axis.set_zlabel("Blue")
# plt.show()

img_hsv = cv2.cvtColor(img_scale, cv2.COLOR_BGR2HSV)
cv2.imshow('hsv', img_hsv)
cv2.waitKey(1)

h, s, v = cv2.split(img_hsv)
fig = plt.figure(figsize=(10, 9))
axis = fig.add_subplot(1,1,1, projection='3d')

axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker=".")
axis.set_xlabel("Hue")
axis.set_ylabel("Saturation")
axis.set_zlabel("Value")
plt.show()