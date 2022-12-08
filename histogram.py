import datetime
import glob
import os
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly
from matplotlib import colors
import itertools

EXTENSIONS = (".jpeg", ".jpg", ".png", ".webp")

def main():
    path = get_image_abspath('./1.png')
    cut_image = detect_white_background(path)
    bgr, hsv = remove_invisible(image_bgra=cut_image)
    # bgr_histogram = draw_histogram(bgr, 'green', type='BGR', result_path='C:/Users/Kento Terada/VSwork/image_analysis/code/test')
    # hsv_histogram = draw_histogram(hsv, 'green', type='HSV')
    sctter3d = draw_3dplot(bgr, 'green', 'BGR')

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
    image_raw = cv2.imread(image_path)
    scale = 500 / image_raw.shape[1]
    image = cv2.resize(image_raw, dsize=None, fx=scale, fy=scale)
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
        figure.update_layout(
            title=type + ' histogram'
        )
    
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
    return figure
        
def draw_3dplot(array_color, filename, type, result_path=None):
    pixel_colors = array_color[:,:3]
    normal = colors.Normalize(vmin=0., vmax=255.)

    b, g, r = pixel_colors[:,0], pixel_colors[:,1], pixel_colors[:,2]
    array_pixels = pixel_colors[:, [2,1,0]]

    array_pixels = normal(array_pixels).tolist()

    figure = go.Figure(
        data=[go.Scatter3d(
            x=b,
            y=g,
            z=r,
            mode='markers',
            marker=dict(
                size=0.5,
                color=array_pixels
                )
            )]
        )
    
    # -------------------------------------
    t = np.linspace(0, 10, 50)
    x, y, z = np.cos(t), np.sin(t), t
    x_eye = -1.25
    y_eye = 2
    z_eye = 0.5
    # ----------------------------------

    figure.update_layout(
        title='RGB 3D plot',
        scene=dict(
            xaxis=dict(title='Blue', range=(0,255)),
            yaxis=dict(title='Green', range=(0,255)),
            zaxis=dict(title='Red', range=(0,255))
        ),
        scene_camera_eye=dict(x=x_eye,y=y_eye,z=z_eye),
        # ----------------------------------
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            y=1,
            x=0.8,
            xanchor='left',
            yanchor='bottom',
            pad=dict(t=45, r=10),
            buttons=[dict(
                label='play',
                method='animate',
                args=[None,dict(
                    frame=dict(duration=5,redraw=True),
                    transition=dict(duration=0),
                    fromcurrent=True,
                    mode='immediate'
                )]
            )])]
    )

    def rotate_z(x,y,z,theta):
        w = x + 1j*y
        return np.real(np.exp(1j*theta)*w), np.imag(np.exp(1j*theta)*w), z

    frames = []
    for t in np.arange(0, 6.26, 0.1):
        xe, ye, ze = rotate_z(x_eye, y_eye, z_eye, -t)
        frames.append(go.Frame(layout=dict(scene_camera_eye=dict(x=xe, y=ye, z=ze))))
    figure.frames=frames
    figure.show()
    return figure
    

if __name__ == '__main__':
    main()