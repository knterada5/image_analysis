import cv2
import sys
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import datetime
from matplotlib import colors
import plotly.graph_objects as go
import plotly.express as px
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

extensions = (".jpeg",".jpg",".png")
flag_bgr = True
flag_hsv = True
flag_multi = False
array_bgra = None
array_hsv = None

def get_image_path(arg_path):
    if os.path.isfile(arg_path):
        if  arg_path.lower().endswith(extensions):
            full_path = os.path.abspath(arg_path)
            return [str(full_path)]
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
    
def remove_invisible(image_path):
    global array_bgra
    # pngはBGRAで読み込む。PNG以外は読み込み後、BGRAに変換
    if image_path.lower().endswith(".png"):
        image_bgra = cv2.imread(image_path, -1)
    else:
        image = cv2.imread(image_path)
        image_bgra = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    # scale = 100 / image_raw.shape[1]
    # image_bgra = cv2.resize(image_raw, dsize=None,  fx=scale, fy=scale)
    
    # 二次元配列に変換し、αが0の画素を削除
    array_image = image_bgra.reshape((image_bgra.shape[0]*image_bgra.shape[1]), image_bgra.shape[2])
    if sum(x > 0 for x in array_image[:,3]) == 0:
        array_image[:,3] = 255
        array_visible = array_image
    else:
        array_visible = array_image[array_image[:,3] > 0]
    array_bgra = array_visible

def make_histgram():
    global array_hsv
    
    hsv = []
    for bgr in array_bgra:
        h, s, v = bgr2hsv(bgr)
        hsv.append([h, s, v])
    array_hsv = np.array(hsv)

    def plot_bgr(ax):
        bgr_colors = ('b', 'g', 'r')
        bgr_labels = ('Blue', 'Green', 'Red')
        fig = go.Figure()
        for ((i, color), label) in zip(enumerate(bgr_colors), bgr_labels):
            hists, bins = np.histogram(array_bgra[:,i], bins = np.arange(256 + 1))
            hists = np.append(hists, 0)
            # ax.plot(bins, hists, color=color, label=label)
            # ax.legend()
        #     fig.add_trace(go.Scatter(x=bins, y=hists))
        # fig.show()
    
    def plot_hsv(ax):
        hsv_colors = ('c', 'm', 'y')
        hsv_labels = ('Hue', 'Saturation', 'Value')
        for ((i, color), label) in zip(enumerate(hsv_colors), hsv_labels):
            hists, bins = np.histogram(array_hsv[:,i], bins=np.arange(256 + 1))
            hists = np.append(hists, 0)
            ax.plot(bins, hists, color=color, label=label)
            ax.legend()
    
    figure = plt.figure()
    ax1 = figure.add_subplot(2,1,1)
    ax2 = figure.add_subplot(2,1,2)
    plot_bgr(ax1)
    # plot_hsv(ax2)
    # figure.savefig("plot.png")
    # plt.show()


def bgr2hsv(array_bgra):
    b, g, r = int(array_bgra[0]), int(array_bgra[1]), int(array_bgra[2])
    max_bgr = max(b, g, r)
    min_bgr = min(b, g, r)

    # Hue
    h = 0
    if max_bgr == min_bgr:
        h = 0
    elif b == max_bgr:
        h = 60 * (r - g) / (max_bgr - min_bgr) + 240
    elif g == max_bgr:
        h = 60 * (b - r) / (max_bgr - min_bgr) + 120
    elif r == max_bgr:
        h = 60 * (g - b) / (max_bgr - min_bgr)
    if h < 0:
        h += 360

    # S
    if max_bgr == 0:
        s = 0
    else:
        s = (max_bgr - min_bgr) / max_bgr * 255

    # V
    v = max_bgr

    return int(h), int(s), int(v)

figg = plt.figure()
ax = figg.add_subplot(1,1,1, projection="3d")

def make_plot():
    global array_bgra, array_hsv
    array_bgr = array_bgra[:,:3]
    pixel_colors = array_bgr.reshape(array_bgr.shape[0], 3)
    norm = colors.Normalize(vmin=0., vmax=255.)
    # norm.autoscale(pixel_colors)

    b,g,r = pixel_colors[:,0], pixel_colors[:,1], pixel_colors[:,2]
    array_colors = pixel_colors[:,[2,1,0]]
    
    array_colors = norm(array_colors).tolist()
    # fig = px.scatter_3d(x=b,y=g,z=r)
    # fig.show()
    # fig.write_html("result.html")
    ax.scatter(b, g, r, facecolors=array_colors, marker=".")
    plt.show()


    

if __name__ == '__main__':
    args = sys.argv
    image_path = get_image_path(args[1])
    image = detect_background(image_path[0])
    result_dir = os.path.dirname(image_path[0]) + "/Result-" + str(datetime.date.today())
    os.makedirs(result_dir, exist_ok=True)
    os.chdir(result_dir)
    cv2.imwrite('cut.png', image)
    remove_invisible('./cut.png')
    # make_histgram()
    make_plot()

# print('start ani')
# def plt_graph3d(angle):
#     ax.view_init(azim=angle*5)
#     print('rotoate')
    
# ani = FuncAnimation(
#     figg,
#     func=plt_graph3d,
#     frames=72,
#     init_func=make_plot,
#     interval=300
# )

# ani.save("rolling.gif", writer="pillow")