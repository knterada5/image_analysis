import glob
import os
import sys

import cv2
import numpy as np
import plotly.graph_objects as go
from matplotlib import colors
import itertools
import tempfile
from PIL import Image
from tqdm import tqdm


EXTENSIONS = (".jpeg", ".jpg", ".png", ".webp")

class DrawGraphSubject():
    def __init__(self):
        self.__observers = []
        self.__process = []

    def add_observer(self, observer):
        '''Add self to observer list.'''
        self.__observers.append(observer)

    def remove_observer(self, observer):
        '''Remove self from observer list.'''
        self.__observers.remove(observer)

    def notify_message(self):
        '''Notify message to observers.'''
        for observer in self.__observers:
            observer.update_message(self)

    def set_message(self, message):
        '''Set latest message.'''
        print(message)
        self.message = message
        self.set_message()
        self.notify_message()

    def notify_process(self):
        '''Notify latest process to observers.'''
        for observer in self.__observers:
            observer.update_process(self)

    def start_process(self, process):
        '''Start process and add to process list.'''
        self.__process.append(process)

    def end_process(self, process):
        '''End process and remove from process list.'''
        index = list(map(lambda x: x.name, self.__process)).index(process.name)
        del self.__process[index]
        self.notify_process()

    def set_process(self, process, now):
        '''Set latest process.'''
        now_process = process.set_now(now)
        index = list(map(lambda x: x.name, self.__process)).index(process.name)
        self.__process[index] = now_process

def main():
    args = sys.argv
    path = get_image_abspath()
    cut_image = detect_white_background(path)
    bgr, hsv = remove_invisible(image_bgra=cut_image)
    bgr_histogram = draw_histogram(bgr, type='BGR')
    hsv_histogram = draw_histogram(hsv, type='HSV')
    sctter3d = draw_scatter3d(bgr, 'green', 'BGR')

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

def draw_histogram(array_color, type):
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

    return figure
    
def save_histogram(figure, filename, type, result_path=None):
    def save():
        name = filename + '_' + type + 'Hist.html'
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

    if result_path == None:    # Save at current directry.
        save('.')
    else:
        print('result path is ', result_path)
        save(result_path)
        
def draw_scatter3d(array_color, type):
    # Transform bgr, if format is bgra.
    pixel_colors = array_color[:,:3]
    # Split B, G, R or H, S, V.
    x, y, z = pixel_colors[:,0], pixel_colors[:,1], pixel_colors[:,2]

    # Set format BGR or HSV.
    if type == 'BGR':
        labels = ['Blue', 'Green', 'Red']
        # Transform BGR to RGB.
        array_pixels = pixel_colors[:, [2,1,0]]
    elif type == 'HSV':
        labels = ['Hue', 'Saturation', 'Value']

    normal = colors.Normalize(vmin=0., vmax=255.)
    array_pixels = normal(array_pixels).tolist()

    figure = go.Figure(
        data=[go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='markers',
            marker=dict(
                size=0.5,
                color=array_pixels
                )
            )]
        )

    figure.update_layout(
        title='RGB 3D plot',
        scene=dict(
            xaxis=dict(title=labels[0], range=(0,255)),
            yaxis=dict(title=labels[1], range=(0,255)),
            zaxis=dict(title=labels[1], range=(0,255))
        ))
        
    return figure

def save_scatter3d(figure: go.Figure, filename: str, type: str ,result_path=None):
    def rotate_z(x, y, z, theta):
        # 1j = i (complex number).
        # Transform x-y to complex plane (e.g. A(1, root3) -> A = 2{sin(pi/3) + isin(pi/3)} = 1 + root3i ))
        w = x + 1j * y
        
        # np.exp(1j * theta) = e^(i*theta) = cos(theta) + isin(theta).
        # z = r{cos(phi) + isin(phi)}, w = cos(theta) + isin(theta) => zw = r{cos(phi + theta) + isin(phi + theta)}
        return np.real(np.exp(1j * theta) * w), np.imag(np.exp(1j * theta) * w), z

    # Camera position.
    x_eye = -1.25
    y_eye = 2
    z_eye = 0.5

    if result_path == None:
        result_path = '.'

    # Save each angle image in temprary directory, and combine to gif.
    with tempfile.TemporaryDirectory(prefix='temp_', dir='.') as temp:
        for i, theta in enumerate(np.arange(0, 2*np.pi, 0.1)):
            x_rotate, y_rotate, z_rotate = rotate_z(x_eye, y_eye, z_eye, -theta)
            figure.update_layout(scene_camera_eye=dict(x=x_rotate, y=y_rotate, z=z_rotate))
            figure.write_image(temp + '/' + str(i) + '.png')

        files = sorted(glob.glob(temp + '/*.png'))
        images = list(map(lambda file: Image.open(file) , files))
        images[0].save(result_path + '/' + filename + '_scatter3D.gif', save_all = True, append_images=images[1:], duration=500, loop=0)

if __name__ == '__main__':
    main()