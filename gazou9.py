import glob
import math
import os
import sys
from ast import arg
from fileinput import isfirstline

import cv2
import numpy as np
from genericpath import exists

isSingle = True
args = sys.argv     # 引数取得

isFirst = True
light_standard = 0
dark_standard = 0

if args[1].endswith('.JPG'):
    files = [args[1]]
    path = os.path.abspath(args[1])
    dir = os.path.dirname(path)
    os.chdir(dir)
else:
    folder = args[1]    # フォルダパス
    os.chdir(folder)    
    files = glob.glob("./*JPG")     # フォルダ内の画像ファイルパス取得

if len(args) == 3:
    isSingle = False
    files.insert(0, args[2])
    print(args[2])

# 結果フォルダ作成
os.makedirs('Result', exist_ok=True)

for file in files:
    img_file = os.path.basename(file)
    img_name = os.path.splitext(img_file)[0]
    os.makedirs(img_name, exist_ok=True)
    print('{0}の処理を開始します'.format(img_name))
    print('light_standard', light_standard)
    print('dark_standard', dark_standard)
    
    # 画像の読み込み
    img = cv2.imread(img_file)
    os.chdir(img_name)

    # 結果ログファイル
    log = open('{0}.log'.format(img_name), 'w')


    # リスケーリング
    scale = 3000 / img.shape[1]
    img_scale = cv2.resize(img, dsize=None, fx=scale, fy=scale)

    # グレースケール化
    img_scale_gray = cv2.cvtColor(img_scale, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('gray.jpeg', img_scale_gray)

    # 二値化
    _, img_threshold = cv2.threshold(img_scale_gray, 150, 255, cv2.THRESH_BINARY)
    cv2.imwrite('threshhold.jpeg', img_threshold)


    # 輪郭検出
    contours, _ = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_list = []
    for i in range(len(contours)):
        M = cv2.moments(contours[i])
        if M['m00'] > 5000.0:
            contours_list.append(contours[i])
    log.write('検出された領域は{0}個です\n'.format(len(contours_list)))


    approx_list = []    # 座標
    rect_list = []      # 4点リスト
    other_list = []     # 4点以外リスト


    # 輪郭点の近似
    for i in range(len(contours_list)):
        # 輪郭点の近似
        approx = cv2.approxPolyDP(contours_list[i], 0.001 * cv2.arcLength(contours_list[i], True), True)
        approx = cv2.convexHull(approx)
        approx = cv2.approxPolyDP(approx, 0.08 * cv2.arcLength(approx, True), True)
        
        # 輪郭が4点かの判定
        if len(approx) == 4:
            rect_list.append(approx)
            log.write('領域{0}は4点で近似できます\n'.format(i))
        elif 3<= len(approx) <= 10:
            other_list.append(approx)
            log.write('領域{0}は10点以下で近似できます\n'.format(i))


    # 射影変換（4点輪郭
    img_rect_list = []  # 射影変換画像リスト

    for i in range(len(rect_list)):
        # numpy配列をlistに変換
        rect_area = rect_list[i].tolist()

        # 4点を左右に分ける
        left = sorted(rect_area, key=lambda x:x[0]) [:2]    # 左の2点
        right = sorted(rect_area, key=lambda x:x[0]) [2:]   # 右の2点

        # 上下に分ける
        left_up = sorted(left, key=lambda x:x[0][1]) [0]
        left_down = sorted(left, key=lambda x:x[0][1]) [1]
        right_up = sorted(right, key=lambda x:x[0][1]) [0]
        rigth_down = sorted(right, key=lambda x:x[0][1]) [1]

        # 4点の座標
        perspective1 = np.float32([left_up, right_up, rigth_down, left_down])

        # 4点の幅、高さ
        width = int(math.sqrt((left_up[0][0] - right_up[0][0]) ** 2 + (left_up[0][1] - right_up[0][1]) ** 2))
        height = int(math.sqrt((left_up[0][0] - left_down[0][0]) ** 2 + (left_up[0][1] - left_down[0][1]) ** 2))
        
        # 補正後の座標
        perspective2 = np.float32([[0,0], [width, 0], [width, height], [0, height]])

        # 射影変換行列生成
        psp_matrix = cv2.getPerspectiveTransform(perspective1, perspective2)
        # 射影変換
        img_rect = cv2.warpPerspective(img_scale, psp_matrix, (width, height))

        # 横長に回転
        h, w = img_rect.shape[:2]
        print('width', w)
        print('height', h)
        if h > w:
            img_rect = cv2.rotate(img_rect, cv2.ROTATE_90_CLOCKWISE)
            print('回転しました')

        img_rect = cv2.resize(img_rect, dsize=(840, 594))

        # リストに追加
        img_rect_list.append(img_rect)

        # 出力
        rect_name = "rect_{0}.jpeg".format(i)
        cv2.imwrite(rect_name, img_rect)


    # 射影変換（その他）
    for i in range(len(other_list)):
        
        # 輪郭に外接する長方形を取得
        rect = cv2.minAreaRect(other_list[i])
        (_, _), (width, height), _ = rect

        #サイズ
        width = np.int32(width)
        height = np.int32(height)

        # 4点座標に修正
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        box = box.tolist()

        # 4点を左右に分ける
        left = sorted(box, key=lambda x:x[0]) [:2]
        right = sorted(box, key=lambda x:x[0]) [2:]

        # 上下に分ける
        left_up = sorted(left, key=lambda x:x[1]) [0]
        left_down = sorted(left, key=lambda x:x[1]) [1]
        right_up = sorted(right, key=lambda x:x[1]) [0]
        right_down = sorted(right, key=lambda x:x[1]) [1]

        # 4点の座標
        perspective1 = np.float32([left_up, right_up, right_down, left_down])

        # 補正後の座標
        perspective2 = np.float32([[0,0], [width, 0], [width, height], [0, height]])

        # 射影変換行列生成
        psp_matrix = cv2.getPerspectiveTransform(perspective1, perspective2)
        
        # 射影変換
        img_rect = cv2.warpPerspective(img_scale, psp_matrix, (width, height))

        # 横長に回転
        h, w = img_rect.shape[:2]
        if h > w:
            img_rect = cv2.rotate(img_rect, cv2.ROTATE_90_CLOCKWISE)

        # リストに追加
        img_rect_list.append(img_rect)

        # 出力
        name = "other_rect_{0}.jpeg".format(i)
        cv2.imwrite(name, img_rect)


    # 色見本の判定1 (縦横比率)
    ng1_list = []
    for i in range(len(img_rect_list)):
        # 射影変換画像のサイズ取得
        h, w = img_rect_list[i].shape[:2]

        # 色見本縦横比1.4を判定
        if 1.2 < (w / h) < 1.6:
            log.write('img_rect_{0}は縦横比1.4です。OK\n'.format(i))
        else:
            log.write('img_rect_{0}は縦横比1.4ではありません。NG\n'.format(i))
            ng1_list.append(i)
            continue


    # 基準外のものをリストから削除
    ng1_list.reverse()
    for i in range(len(ng1_list)):
        del1_no = ng1_list[i]
        del img_rect_list[del1_no]
        log.write('img_rect_{0}を除外\n'.format(del1_no))
    log.write('色見本候補は{0}個です\n'.format(len(img_rect_list)))


    # 色見本の判定2 (白枠の有無)
    ng2_list = []
    for i in range(len(img_rect_list)):
        # 射影変換画像のサイズ
        h, w = img_rect_list[i].shape[:2]

        # 二値化
        img_binary = cv2.cvtColor(img_rect_list[i], cv2.COLOR_BGR2GRAY)
        _, threshold2 = cv2.threshold(img_binary, 100, 255, cv2.THRESH_BINARY)
        white_name = "white_{0}.jpeg".format(i)
        cv2.imwrite(white_name, threshold2)

        # 白の連続最大長を計算
        white_max = 0
        for line in threshold2:
            white = 0
            for l in line:
                if l > 0:
                    white += 1
            if white > white_max:
                white_max = white

        # 白の連続最大長が色見本の幅に合うか判定
        if white_max > w * 0.95:
            log.write('white_{0}は連続白を含みます\n'.format(i))
        else:
            log.write('img_rect{0}は白の連続長が不十分です\n'.format(i))
            ng2_list.append(i)
            continue
        
    # 基準外のものをリストから削除
    ng2_list.reverse()
    for i in range(len(ng2_list)):
        del2_no = ng2_list[i]
        del img_rect_list[del2_no]
        log.write('white_{0}を除外\n'.format(del2_no))
    log.write('色見本候補は{0}個です\n'.format(len(img_rect_list)))


    # 色見本の判定3 (色の構成)
    ng3_list = []
    for i in range(len(img_rect_list)):
        # 白枠の幅取得
        stdH, stdW = img_rect_list[i].shape[:2]
        ratio = 0.11    # 白枠の幅の比率
        frame = int(stdW * ratio)  # 白枠の幅
        
        # 白枠を除いた画像
        stdW2 = stdW - frame    # 白枠以外の幅
        stdH2 = stdH - frame    # 白枠以外の高さ
        img_std = img_rect_list[i][frame: stdH2, frame: stdW2]
        
        # 出力
        name_cut = "std_cut_{0}.jpeg".format(i)
        cv2.imwrite(name_cut, img_std)

        # 切り出しサイズ
        color = 3   # 色見本の色数（黒・白・黒）
        splitW = 8  # 分割幅
        splitH = 8  # 分割高さ
        cutW = int(stdW2 / (color * splitW))    # 切り出し幅
        cutH = int(stdH2 / splitH)              # 切り出し高さ
        colorW = int(stdW2 / color)             # 色幅
        
        # 切り出し開始位置
        cutStartX = cutW
        cutStartY = cutH

        # 色見本色情報の初期化
        color_bgr = np.zeros((color, 3), dtype=np.uint8)
        color_hsv = np.zeros((color, 3), dtype=np.uint8)

        # 1色ずつ切り出し、平均値を取得
        for c in range(color):
            # 切り出し
            img_color_bgr = img_std[cutStartY: cutStartY + cutH, cutStartX: cutStartX + cutW * 2]
            name_color_bgr = 'stdCut_{0}_color_{1}.jpeg'.format(i, c)
            cv2.imwrite(name_color_bgr, img_color_bgr)

            # BGR平均値取得
            color_bgr[c][0] = int(img_color_bgr.T[0].flatten().mean())
            color_bgr[c][1] = int(img_color_bgr.T[1].flatten().mean())
            color_bgr[c][2] = int(img_color_bgr.T[2].flatten().mean())
            
            # BGRからHSVに変換
            img_color_hsv = cv2.cvtColor(img_color_bgr, cv2.COLOR_BGR2HSV)

            # HSV平均値取得
            color_hsv[c][0] = img_color_hsv.T[0].flatten().mean()
            color_hsv[c][1] = img_color_hsv.T[1].flatten().mean()
            color_hsv[c][2] = img_color_hsv.T[2].flatten().mean()

            # 次の色へ
            cutStartX += colorW

        # 左右の黒の差
        diff_black = 0
        for n in range(3):
            diff_black += (abs(int(color_bgr[0][n]) - int(color_bgr[2][n])))
        if diff_black > 100:
            log.write('std_cut_{0}は左右で色が異なります。差：{1}\n'.format(i, diff_black))
            ng3_list.append(i)
            continue
        else:
            log.write('std_cut_{0}は左右の色が同じです。差：{1}\n'.format(i, diff_black))
            # 白と黒の差
            diff_white = 0
            for n in range(3):
                diff_white += (abs(int(color_bgr[0][n]) - int(color_bgr[1][n])))
            if diff_white < 250:
                log.write('std_cut_{0}は白と黒ではありません。差：{1}\n'.format(i, diff_white))
                ng3_list.append(i)
                continue
            else:
                log.write('std_cut_{0}は白と黒を含みます。差：{1}\n'.format(i, diff_white))
                bgr_ok = color_bgr


    # 基準外のものをリストから削除
    ng3_list.reverse()
    for i in range(len(ng3_list)):
        del3_no = ng3_list[i]
        del img_rect_list[del3_no]
        log.write('white_{0}を除外\n'.format(del3_no))
    log.write('色見本候補は{0}個です\n'.format(len(img_rect_list)))


    # 色見本の数
    if len(img_rect_list) > 1:
        log.write("色見本を1つに絞れませんでした\n")
    elif len(img_rect_list) == 1:
        log.write('色見本を検出しました\n')
    else:
        log.write('色見本を検出できませんでした\n')


    # 二値化閾値の初期値
    thresh = 128
    thresh_max = 255
    thresh_min = 0

    # 画像サイズ
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height_img, width_img = img_gray.shape[:2]
    size = height_img * width_img

    # 二値化
    img_bool = img_gray > thresh
    hilight_sum = img_bool.sum()
    if hilight_sum <= size / 2:
        while thresh < thresh_max:
            img_bool = img_gray > thresh
            hilight_sum = img_bool.sum()
            if hilight_sum > size / 2:
                thresh += 1
            else:
                break
    else:
        while thresh > thresh_min:
            img_bool = img_gray > thresh
            hilight_sum = img_bool.sum()
            if hilight_sum < size / 2:
                thresh -= 1
            else:
                break

    # 明るい画素の補正値
    if isSingle or (~isSingle and isFirst):
        print('1回目だよ')
        img_hi = np.full_like(img, 255)
        w_max = max(bgr_ok[1])
        print('w_max', w_max)
        light_standard = w_max
        w_bgr = (bgr_ok[1] < w_max)
        w_bgr = w_bgr * (w_max - bgr_ok[1])
        print('bgr_ok', bgr_ok)
        log.write('明るい画素の補正値：{0}\n'.format(w_bgr))

        # 色差が大きい補正値になる場合は、画像全体を明るい画素のみにする
        if max(w_bgr) - min(w_bgr) > 50:
            img_bool_light = np.full_like(img_bool, True)
        else:
            img_bool_light = img_bool

        # 補正値加算可能な最大BGR値
        maxval = [255, 255, 255]
        max_Wbgr = abs(w_bgr - maxval)
        img_hi_bool = np.empty_like(img_hi)

        # 補正値を加算しても255を超えない画素値のみを補正対象とする
        for i in range(3):
            img_hi_bool[:, :, i] = img[:, :, i] <= max_Wbgr[i]

        # 補正値を加算
        for i in range(3):
            img_hi[:,:,i] += img_bool * img_hi_bool[:,:,i] * (img[:,:,i] + w_bgr[i])
        cv2.imwrite('light.jpeg', img_hi)

        # 暗い画素の補正値
        img_dark = np.zeros_like(img)
        b_min = min(bgr_ok[0])
        print('b_min', b_min)
        dark_standard = b_min
        b_bgr = (bgr_ok[0] > b_min)
        b_bgr = b_bgr * (bgr_ok[0] - b_min)
        log.write('暗い画素の補正値：{0}\n'.format(b_bgr))

        # 色差が大きい補正値になる場合は、画像全体を暗い画素のみにする
        if max(b_bgr) - min(b_bgr) > 50:
            img_bool = np.full_like(img_bool, False)

        # 補正減算可能な最小BGR値
        minval = b_bgr
        img_dark_bool = np.empty_like(img_dark)

        # 補正値で減算しても0未満にならない画素値のみを補正対象とする
        for i in range(3):
            img_dark_bool[:,:,i] = img[:,:,i] >= minval[i]

        # 補正値を減算
        for i in range(3):
            img_dark[:,:,i] = ~img_bool * img_dark_bool[:,:,i] * (img[:,:,i] - b_bgr[i])
        cv2.imwrite('dark.jpeg', img_dark)

        # 合成
        img_combine = img_dark.copy()
        for i in range(3):
            img_combine[:,:,i] += img_bool * img_hi[:,:,i]

        # 明るさの補正
        # 補正値
        bright_up = int(255 - w_max)
        bright_down = b_min
        bright = int(bright_up - bright_down)

        # 補正
        def adjust(image, alpha=1.0, beta=0.0):
            dst = alpha * image + beta
            return np.clip(dst, 0, 255).astype(np.uint8)
        img_combine = adjust(img_combine, alpha=1.0, beta=0.392 * bright)

        # 出力
        os.chdir('../')
        cv2.imwrite("Result/{0}_combine.jpeg".format(img_name), img_combine)
        print('{0}の処理が完了しました'.format(img_name))
        log.close
        isFirst = False

    elif ~isSingle and ~isFirst:
        print('2回目です')
        # 画像をB,G,Rに分割
        img_b, img_g, img_r = cv2.split(img)

        # 明るい画素の補正値
        ok_w = bgr_ok[1].astype(np.int64)
        w_bgr = light_standard - ok_w
        log.write('light_standard {0}\n'.format(light_standard))
        log.write('bgr_ok {0}\n'.format(bgr_ok[1]))
        log.write('minus {0}\n'.format(light_standard - bgr_ok[1]))
        log.write('明るい画素の補正値：{0}\n'.format(w_bgr))

        # 補正値を加算
        img_bl = cv2.add(img_b, int(w_bgr[0]))
        img_bl = img_bool * img_bl
        img_gl = cv2.add(img_g, int(w_bgr[1]))
        img_gl = img_bool * img_gl
        img_rl = cv2.add(img_r, int(w_bgr[2]))
        img_rl = img_bool * img_rl

        # B, G, Rを合成
        img_light = cv2.merge([img_bl, img_gl, img_rl])
        cv2.imwrite('light.jpeg', img_light)

        # 暗い画素の補正値
        ok_b = bgr_ok[0].astype(np.int64)
        b_bgr = dark_standard - ok_b
        log.write('暗い画素の補正値：{0}\n'.format(b_bgr))

        # 補正値を減算
        img_bd = cv2.add(img_b, int(b_bgr[0]))
        img_bd = ~img_bool * img_bd
        img_gd = cv2.add(img_g, int(b_bgr[1]))
        img_gd = ~img_bool * img_gd
        img_rd = cv2.add(img_r, int(b_bgr[2]))
        img_rd = ~img_bool * img_rd

        # B,G,Rを合成
        img_dark = cv2.merge([img_bd, img_gd, img_rd])
        cv2.imwrite('dark.jpeg', img_dark)

        # 合成
        img_combine = img_dark.copy()
        for i in range(3):
            img_combine[:,:,i] += img_bool * img_light[:,:,i]

        # 明るさの補正
        # 補正値
        bright_up = int(255 - light_standard)
        bright_down = dark_standard
        bright = int(bright_up - bright_down)

        # 補正
        def adjust(image, alpha=1.0, beta=0.0):
            dst = alpha * image + beta
            return np.clip(dst, 0, 255).astype(np.uint8)

        img_combine = adjust(img_combine, alpha=1.0, beta=0.392 * bright)

        # 出力
        os.chdir('../')
        cv2.imwrite("Result/{0}_combine.jpeg".format(img_name), img_combine)
        print('{0}の処理が完了しました'.format(img_name))
        log.close