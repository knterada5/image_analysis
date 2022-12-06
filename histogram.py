import datetime
import glob
import os
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from matplotlib import colors
import itertools

EXTENSIONS = (".jpeg", ".jpg", ".png")

def main():
    path = get_image_abspath('./green.jpg')
    cut_image = detect_white_background(path)
    bgr, hsv = remove_invisible(image_bgra=cut_image)
    print(bgr.shape)
    print(hsv.shape)
    draw_histogram(bgr, 'green', type='BGR', result_path='C:/Users/Kento Terada/VSwork/image_analysis/code/test')
    draw_histogram(hsv, 'green', type='HSV')

def get_image_abspath(path):
    if os.path.isfile(path):
        # Image file or not.
        if path.lower().endswith(EXTENSIONS):
            abspath = os.path.abspath(path)
            return abspath
        else:
            raise Exception(path, ' is not image file.')
    # Get path list of image file in selected folder.
    else:
        path_list = []
        for ext in EXTENSIONS:
            path_list.append(glob.glob(path + '/*' + ext))
        if path_list == []:
            raise Exception(path,'has no image file.')
        else:
            abspath_list = []
            for path in path_list:
                abspath_list.append(os.path.abspath(path))
            return abspath_list

def detect_white_background(image_path):
    image = cv2.imread(image_path)
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
    return cv2.bitwise_and(image_bgra, image_bgra, mask=mask)

def remove_invisible(image_path=None, image_bgra=None):
    # If image file type is PNG, read file as BGRA. Other type, read as BGR and convert to BGRA.
    if image_path != None:
        if image_path.lower().endswith('.png'):
            image_bgra = cv2.imread(image_path, -1)
        else:
            image = cv2.imread(image_path)
            image_bgra = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    image_hsv = cv2.cvtColor(image_bgra, cv2.COLOR_BGR2HSV_FULL)
    # Convert image to 2D array [B, G, R, A], [H, S, V].
    array_bgra = image_bgra.reshape((image_bgra.shape[0]*image_bgra.shape[1]), image_bgra.shape[2])
    array_hsv = image_hsv.reshape((image_hsv.shape[0]*image_hsv.shape[1]), image_hsv.shape[2])
    
    # Create array of visivle pixel.
    # When all pixel alpha = 0 (when BGRA but BGR PNG), set all alpha = 255.
    if sum(x > 0 for x in array_bgra[:,3]) == 0:
        array_bgra[:,3] = 255
        return array_bgra, array_hsv
    else:
        return array_bgra[array_bgra[:,3] > 0], array_hsv[array_bgra[:,3] > 0]    # Remove pixel, of which alpha = 0.

def draw_histogram(array_color, filename, type, result_path=None):
    # Graph settings.
    bgr_colors = ('blue', 'green', 'red')    # BGR marker color.
    bgr_labels = ('Blue', 'Green', 'Red')    # BGR label name.
    hsv_colors = ('cyan', 'magenta', 'yellow')    # HSV marker color.
    hsv_labels = ('Hue', 'Saturation', 'Value')    # HSV label name.

    figure = go.Figure()

    # Data set.
    if type == 'BGR':
        colors = bgr_colors
        labels = bgr_labels
    elif type == 'HSV':
        colors = hsv_colors
        labels = hsv_labels
    for ((i, color), label) in zip(enumerate(colors), labels):
        hists, bins = np.histogram(array_color[:,i], np.arange(256 + 1))    # bins: every 1 in the range from 0 to 256 to prevent come togehter hist of 254 and 255.
        hists = np.append(hists, 0)    # At bin = 256, bgr = 0
        figure.add_trace(go.Scatter(x=bins, y=hists, name=label, marker_color=color))
    figure.show()
    
    # Save
    name = filename + '_' + type + 'Hist.html'
    def save(dir):
        # When already file exists, save as new name.
        if os.path.exists(dir + '/' + name):
            print('exist')
            for i in itertools.count(1):
                print('for', i)
                new_name = dir + '/' + filename + '_' + type + 'Hist(' + str(i) + ').html'
                if not os.path.exists(new_name):
                    break
            figure.write_html(new_name)
        else:    # Not exist.
            print('not exist')
            figure.write_html(dir + '/' + name)
    if result_path == None:
        save('.')
    else:
        print('result path is ', result_path)
        save(result_path)
        
def draw_3dplot(array_color, filename, type, result_path=None):
    pixel_colors = array_color[:,:3]
    normal = colors.Normalize(vmin=0., vmax=255.)

    b, g, r = pixel_colors[:,0], pixel_colors[:,1], pixel_colors[:,2]
    array_pixels = pixel_colors[:, [2,1,0]]

    array_pixels = normal(array_pixels).tolist()
    
if __name__ == '__main__':
    main()