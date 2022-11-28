import cv2
import sys
import numpy as np
import os

extensions = (".jpeg",".jpg",".png")

def get_image_path(arg_path):
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


def detect_background(image_path):
    image = cv2.imread(image_path)
    image_bgra = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 背景（白）の範囲抽出
    hsv_min = np.array([0,0,0])
    hsv_max = np.array([180, 40, 255])
    background = cv2.inRange(image_hsv, hsv_min, hsv_max)
    
    # 背景反転し、輪郭抽出
    background_not = cv2.bitwise_not(background)
    contours, _ = cv2.findContours(background_not, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # マスク作成
    # 元画像と同じサイズの画像を作成（全て0）
    mask = np.zeros(image_bgra.shape[:2], dtype=np.uint8)
    # 抽出した輪郭内を255で塗りつぶす
    cv2.drawContours(mask, contours, -1, color=255, thickness=-1)
    
    image_cut = cv2.bitwise_and(image_bgra, image_bgra, mask=mask)
    return image_cut  

def bgr2hsv():
    

if __name__ == '__main__':
    args = sys.argv
    detect_background(args[1])