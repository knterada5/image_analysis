import datetime
import glob
import os
import sys
from enum import Enum

import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors


class PathType(Enum):
    FILE = 1
    FOLDER = 2

EXTENSIONS = (".jpeg", ".jpg", ".png")

def file_or_folder(path):
    # Check file or folder.
    if os.path.isfile(path):
        # Check image file or not.
        if path.lower().endswith(EXTENSIONS):
            return PathType.FILE
        else:
            raise Exception('This is not image file.')
    else:
        files = []
        for ext in EXTENSIONS:
            files += glob.glob("./*" + ext)
        if files == []:
            raise Exception('No image file in this folder.')
        else:
            return PathType.FOLDER

def get_image(path, path_type):
    if path_type == PathType.FILE:
        if path.lower().endswith(".png"):
            image_bgra = cv2.imread(path, -1)
        else:
            image = cv2.imread(path)
            image_bgra = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

def disp():
    root = 

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2 or 3:
        try:
            path_type = file_or_folder(args[1])
        except Exception as e:
            print(e)
        path = os.path.abspath(args[1])
        if path == PathType.FILE:
            image = get_image(path)
        elif path == PathType.FOLDER:
            files = []
            for ext in EXTENSIONS:
                files += glob.glob("")