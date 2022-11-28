import sys
import os
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import datetime

extensions = (".jpeg",".jpg",".png")

def getImages(arg_path):
    if os.path.isfile(arg_path):
        if  arg_path.lower().endswith(extensions):
            full_path = os.path.abspath(arg_path)
            return [full_path]
        else:
            raise Exception('Not image file')
    else:
        os.chdir(arg_path)
        files = []
        for ext in extensions:
            files += glob.glob("./*" + ext)
        if files == []:
            raise Exception('No image file')
        else:
            full_paths = []
            for file in files:
                full_paths.append(os.path.abspath(file))
            return full_paths


def getArea(image_path):
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    image = cv2.imread(image_path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(image_name + '_gray.jpeg', image_gray)
    edge = cv2.Canny(image_gray, 20, 20)
    cv2.imwrite(image_name + '_canny.jpeg', edge)
    _, image_threshold = cv2.threshold(image_gray, 180, 255, cv2.THRESH_BINARY)
    cv2.imwrite(image_name + '_thresh.jpeg', image_threshold)
    reverse_threshold = cv2.biwtise_not(image_threshold)
    contours, _ = cv2.findContours(reverse_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, color=(0,0,255), thickness=3)
    cv2.imwrite(image_name + "_cont.jpeg", image)

def getGraph(image):
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(image_hsv)
    fig = plt.figure(figsize=(10,9))
    pixel_colors = image.reshape((np.shape(image)[0]*np.shape(image)[1], 3))
    norm = colors.Normalize(vmin=1., vmax=1.)
    norm.autoscale(pixel_colors)
    pixel_colors = norm(pixel_colors).tolist()

    axis = fig.add_subplot(1,1,1, projection='3d')

    axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker=".")
    axis.set_xlabel("Hue")
    axis.set_ylabel("Saturation")
    axis.set_zlabel("Value")
    plt.show

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2 or 3:
        try:
            images = getImages(args[1])
        except Exception as e:
            raise Exception(e) from e
        if len(args) == 2:
            path = os.path.abspath(args[1])
            result_path = os.path.dirname(path)
        elif len(args) == 3:
            result_path = os.path.abspath(args[2])
        result_folder = result_path + "/Result-" + str(datetime.date.today())
        os.makedirs(result_folder, exist_ok=True)
        os.chdir(result_folder)
        for image in images:
            getArea(image)
        
    else:
        raise Exception('Invalid argument')