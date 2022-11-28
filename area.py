from multiprocessing.sharedctypes import Value
import string
from webbrowser import Grail
import cv2
import sys
from cv2 import cvtColor
from cv2 import COLOR_BGR2HSV
from matplotlib import pyplot as plt
import numpy as np
import tkinter
from tkinter import colorchooser
from tkinter import filedialog

# 輪郭の検出
def detectConts(img):
    # グレースケール、二値化
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
    cv2.imwrite('nichika.jpeg', thresh)

    # 輪郭検出
    conts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    conts_list = list(filter(lambda x: cv2.contourArea(x) > 100, conts))
    return conts_list


# 輪郭の描画
def drawCont(img, conts_list):
    cv2.drawContours(img, conts_list, -1, color=(0,0,255), thickness=3)
    for i, cnt in enumerate(conts_list):
        cnt = cnt.squeeze(axis=1)
        cv2.putText(img, str(i), (cnt[0][0], cnt[0][1]), cv2.FONT_HERSHEY_COMPLEX, 2.0, (255,0,0), thickness=3)
    return img


# 色の抜き出し
def pick_color(img, H, S, V, range):
    global B,G,R
    lower = np.array([60, 40, 0])
    upper = np.array([90, 200, 80])
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_mask = cv2.inRange(img_hsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=img_mask)
    return result


# 面積測定
def measureArea(conts_list):
    total_area = 0
    for i in range(len(conts_list)):
        area = cv2.contourArea(conts_list[i])
        print('領域{0}の面積は {1}'.format(i, area))
        total_area += area
    return total_area





file_path = None
color = None
color_range = None
B = G = R = 0
H = S = V = 0

def disp():
    def onMouse(event, x, y, flags, params):
        global B, G, R, H, S, V
        if event == cv2.EVENT_LBUTTONDOWN:
            crop_img = img_scale[[y], [x]]
            B = crop_img.T[0].flatten().mean()
            G = crop_img.T[1].flatten().mean()
            R = crop_img.T[2].flatten().mean()
            print(B,G,R)
            cv2.destroyWindow('Image')
            txt = str(B) +', ' + str(G) + ', ' + str(R)
            txt_color.insert(tkinter.END, txt)
            H, S, V = calc_hsv(B, G, R)
            print('H, S, V', H, S, V)
            
    def calc_hsv(B, G, R):
        Max = max(B,G,R)
        Min = min(B,G,R)

        if B == G == R:
            if Max == 255:
                return 0, 0, 100
            if Max == 0:
                return 0,0,0

        try:
            if R == Max:
                H = int(60 * (G - B) / (Max - Min))
            if G == Max:
                H = int(60 * (G - B) / (Max - Min) + 120)
            if B == Max:
                H = int(60 * (G - B) / (Max - Min) + 240)
            if H < 0:
                H += 360
        except ZeroDivisionError:
            pass

        S = int(100 * (Max - Min) / Max)
        V = int(100 * Max / 255)

        return H, S, V

    def btn_img_click():
        global file_path, img, img_scale
        file_path = tkinter.filedialog.askopenfilename()
        img = cv2.imread(file_path)
        scale = 800 / img.shape[1]
        img_scale = cv2.resize(img, dsize=None, fx=scale, fy=scale)
        txt_img.insert(tkinter.END, file_path)
        window_name = 'Image'
        cv2.imshow(window_name, img_scale)
        cv2.setMouseCallback(window_name, onMouse)
        cv2.waitKey(1)

    def btn_color_click():
        global color
        color = colorchooser.askcolor()
        txt_color.insert(tkinter.END, color)

    def btn_enter_click():
        window_name = 'Image'
        cv2.imshow(window_name, img_scale)
        cv2.setMouseCallback(window_name, onMouse)
        cv2.waitKey(1)

    def btn_kettei_click():
        global color_range, H, S, V
        color_range = int(txt_range.get())
        result = pick_color(img, (H / 2), S, V, color_range)
        cv2.imwrite('result.jpeg', result)
        print('push kettei')
        scale = 800 / result.shape[1]
        result_scale = cv2.resize(result, dsize=None, fx=scale, fy=scale)
        window_name = 'Image'
        cv2.imshow(window_name, result_scale)
        cv2.waitKey(1)
                
        
    root = tkinter.Tk()
    root.geometry('300x200')
    root.title('色抽出')

    main_frm = tkinter.Frame(root)
    main_frm.grid(column=0, row=0, sticky=tkinter.NSEW, padx=5, pady=10)

    lbl_img = tkinter.Label(main_frm, text='画像')
    lbl_color = tkinter.Label(main_frm, text='抽出色')
    lbl_range = tkinter.Label(main_frm, text='色範囲')

    txt_img = tkinter.Entry(main_frm)
    txt_color = tkinter.Entry(main_frm)
    txt_range = tkinter.Entry(main_frm)

    btn_img = tkinter.Button(main_frm, text='▼', command=btn_img_click)
    btn_color = tkinter.Button(main_frm, text='▼', command=btn_color_click)
    btn_enter = tkinter.Button(main_frm, text='実行', command=btn_enter_click)
    btn_kettei = tkinter.Button(main_frm, text='決定', command=btn_kettei_click)

    lbl_img.grid(column=0, row=0)
    lbl_color.grid(column=0, row=1)
    lbl_range.grid(column=0, row=2)
    txt_img.grid(column=1, row=0, sticky=tkinter.EW, padx=5)
    txt_color.grid(column=1, row=1, sticky=tkinter.EW, padx=5)
    txt_range.grid(column=1, row=2, sticky=tkinter.EW, padx=5)
    btn_img.grid(column=2, row=0)
    btn_color.grid(column=2, row=1)
    btn_enter.grid(column=1, row=3)
    btn_kettei.grid(column=2, row=3)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frm.columnconfigure(1, weight=1)

    root.mainloop()


if __name__ == '__main__':
    img = None
    img_scale = None
    disp()