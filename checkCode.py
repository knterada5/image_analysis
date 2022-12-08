import os
import sys
import tkinter
import tkinter.messagebox as messagebox

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
from numpy import pi, cos, sin, sqrt
from PIL import Image
import glob
import os
import tempfile

def main():
    gif()

def gif():
    with tempfile.TemporaryDirectory(prefix='tmp_', dir='.') as temp:
        print('hajimari', os.curdir)
        print('temp', temp)
        for i in range(10):
            if i%2 == 0:
                image = cv2.imread('1.png')
                cv2.imwrite(temp + '/' + str(i) + '.png', image)
            else:
                image = cv2.imread('arrow.png')
                cv2.imwrite(temp + '/' + str(i) + '.png', image)
        files = sorted(glob.glob(temp + '/*.png'))
        images = list(map(lambda file: Image.open(file), files))
        images[0].save('gattai.gif', save_all=True, append_images=images[1:], duration=500, loop=0)
    print('owari', os.curdir)
    
def check_convert():
    # delete_alpha()
    print('cv2')
    start = time.time()
    hsv_cv2 = bgr2hsv_cv2()
    print(time.time() - start)
    print(hsv_cv2)
    print('kenchi')
    sstart = time.time()
    image = cv2.imread('./2.webp')
    hsv = np.apply_along_axis(lambda x: bgr2hsv(x), 2, image)
    print(time.time() - sstart)
    print(hsv)


def bgr2hsv_cv2():
    image = cv2.imread('./2.webp')
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    

def delete_alpha():
    array = np.array([[1,1,1,0], [2,2,2,0],[3,3,3,3],[4,4,4,4],[5,5,5,0]])
    


def loop_double():
    aa = [1,2,3,4,5]
    bb = ['a','b','c','d','e']

    for (a, (i, b)) in zip(aa, enumerate(bb)):
        print("a is", a, "b no is ", i, "b is ", b)


def change():
    hsv = []
    arr_bgr = np.array([[100,80,200,255], [200,200,200,255], [150,150,150,255], [250,250,250,255], [0,0,0,255], [255,255,255,255]])
    for bgr in arr_bgr:
        h,s,v = bgr2hsv(bgr)
        pixel = [h,s,v]
        hsv.append(pixel)
    result = np.array(hsv)
    print(result)

    # hsv = map(lambda x: bgr2hsv(x), arr_bgr)
    # print(hsv)

def bgr2hsv(bgr):
        b,g,r = int(bgr[0]), int(bgr[1]), int(bgr[2])
        bgr_max = max(b,g,r)
        bgr_min = min(b,g,r)
        
        # Hue
        h = 0
        if bgr_max == bgr_min:
            h = 0
        elif b == bgr_max:
            h = 60 * (r - g) / (bgr_max - bgr_min) + 240
        elif g == bgr_max:
            h = 60 * (b - r) / (bgr_max - bgr_min) + 120
        elif r == bgr_max:
            h = 60 * (g - b) / (bgr_max - bgr_min)
        if h < 0:
            h += 360
        

        # S
        if bgr_max == 0:
            s = 0
        else: 
            s = (bgr_max - bgr_min) / bgr_max * 255

        # v
        v = bgr_max    
        return [h,s,v]


def make_plot(image_path):
    # image = cv2.imread(image_path)
    # b,g,r = cv2.split(image)
    # hist_b = cv2.calcHist([b],[0],None,[256],[0,256])
    # hist_g = cv2.calcHist([g],[0],None,[256],[0,256])
    # hist_r = cv2.calcHist([r],[0],None,[256],[0,256])
    # plt.plot(hist_b, color='b', label="b")
    # plt.plot(hist_g, color='g', label="g")
    # plt.plot(hist_r, color='r', label="r")
    
    if image_path.lower().endswith(".png"):
        img = cv2.imread(image_path, -1)
    else:
        imgg = cv2.imread(image_path)
        img = cv2.cvtColor(imgg, cv2.COLOR_BGR2BGRA)
    print("shape0", img.shape[0])
    print("shape1", img.shape[1])
    print("shape2", img.shape[2])
    new_img = img.reshape((img.shape[0]*img.shape[1]), img.shape[2])
    cut_img = new_img[new_img[:,3] > 0]

    
    colors = ('b','g','r')
    for i,color in enumerate(colors):
        hist, bins = np.histogram(cut_img[:,i], bins=np.arange(256+1))
        hist = np.append(hist,0)
        plt.plot(bins, hist, color=color)
    # hist, bins = np.histogram(cut_img[:,0], bins=np.arange(256 + 1))
    # hist2 = np.append(hist,0)

    # plt.plot(bins, hist2,color='r')

    # plt.hist(cut_img[:,0], bins=128, histtype='step')
    # plt.hist(cut_img[:,1], bins=128, histtype='step')
    # plt.hist(cut_img[:,2], bins=128, histtype='step')
    hsv = []
    for bgr in cut_img:
        h,s,v = bgr2hsv(bgr)
        pixel = [h,s,v]
        hsv.append(pixel)
    hsv_col = np.array(hsv)

    hsv_colors = ('c','m','y')
    for i,col in enumerate(hsv_colors):
        hist, bins = np.histogram(hsv_col[:,i], bins=np.arange(256+1))
        hist = np.append(hist,0)
        plt.plot(bins, hist, color=col)
    plt.show()


    # b,g,r,a = img[:,:,0], img[:,:,1], img[:,:,2],img[:,:,3]
    # a1 = np.ravel(a)
    # print(a1)
    # a_true = np.where(a1 > 0)
    # print(a_true)
    # color = ('b', 'g', 'r')
    # for i, col in enumerate(color):
    #     hist = cv2.calcHist([img],[i],None,[256],[0,256])
    #     plt.plot(hist,color=col)
    #     plt.xlim([0,256])
    # plt.show()

    


    # img_hsv = cv2.cvtColor(bgr_imag,cv2.COLOR_BGR2HSV)
    # hsv = ('c','m','y')
    # for i,col in enumerate(hsv):
    #     histh = cv2.calcHist([img_hsv],[i],None,[256],[0,256])
    #     plt.plot(histh,color=col,label=col)
    # plt.legend()
    # plt.show()

def disp():
    root = tkinter.Tk()
    root.geometry('300x200')
    root.title('test')

    main_frame = tkinter.Frame(root)
    main_frame.grid(column=0,row=0,sticky=tkinter.NSEW)
    button = tkinter.Button(main_frame, text='button', command=show_dialog)
    button.grid(column=0,row=0)
    root.mainloop()

def show_dialog():
    messagebox.showerror('エラー', 'フォルダを選択してください')
    

def detect_background(img_path):
    image = cv2.imread(img_path)
    rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    hsv_min = np.array([0,0,0])
    hsv_max = np.array([180, 40, 255])
    background = cv2.inRange(hsv, hsv_min, hsv_max)
    back_not = cv2.bitwise_not(background)
    mask1 = np.zeros(rgba.shape[:2], dtype=np.uint8)
    mask1 = cv2.bitwise_not(mask1, mask1, mask=back_not)
    img =cv2.bitwise_and(rgba, rgba, mask=mask1)
    cv2.imwrite('mask.png', img)
    img_A = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    img_not = cv2.bitwise_and(image, image, mask=back_not)
    img_not_rgba = cv2.cvtColor(img_not, cv2.COLOR_BGR2BGRA)

    # img_not_rgba[:,:,3] = np.where(np.all(img_not_rgba == 0, axis=-1), 0, 0)
    
    # back = cv2.cvtColor(background, cv2.COLOR_HSV2BGR)
    img_back = cv2.bitwise_or(image, image, mask=background)
    mask = cv2.bitwise_not(background)
    rgba_not = cv2.bitwise_not(rgba, rgba, mask=background)
    rgba_not[:,:,3] = np.where(rgba_not[:,:,3] == 0, 50, 255)
    cv2.imwrite('3.png', img_not)

    masked_image = cv2.bitwise_and(image, image, mask=background)
    img_gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(img_gray, 10, 255, cv2.THRESH_BINARY)
    cv2.imwrite('2.jpeg', thresh)
    cv2.imwrite('1.jpeg', masked_image)

    img_bool = cv2.bitwise_not(image,image, mask=background)
    cv2.imwrite('1.png', img_bool)

if __name__ == '__main__':
    main()
    # args = sys.argv
    # change()

    # loop_double()

    # make_plot(args[1])
    
    # detect_background(os.path.abspath(args[1]))
    # disp()