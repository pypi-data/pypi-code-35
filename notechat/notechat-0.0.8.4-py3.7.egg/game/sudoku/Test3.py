#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/04/01 16:31
# @Author  : niuliangtao
# @Site    :
# @File    : Test2.py
# @Software: PyCharm
import cv2 as cv
import numpy as np
import pytesseract
from PIL import Image

import notechat.game.sudoku.auto_adb as adb
import notechat.game.sudoku.sudoku as sudoku
from notechat.game.sudoku.auto_adb import click, screenshot_to_local


def cut_image(image, para=(55, 220, 972 / 9, 972 / 9)):
    start_x, start_y, length_x, length_y = para

    result = []
    for j in range(0, 9):
        line = []
        for i in range(0, 9):
            x_s = start_x + i * length_x + 10  # 10
            y_s = start_y + j * length_y + 10  # 10

            x_e = start_x + (i + 1) * length_x - 10
            y_e = start_y + (j + 1) * length_y - 10

            # print((x_s, y_s, x_e, y_e))

            box = image.crop((x_s, y_s, x_e, y_e))

            num = pytesseract.image_to_string(box, config="-c tessedit_char_whitelist=0123456789"
                                                          " --psm 10 digits"
                                                          " -l osd "
                                                          " --oem 0")
            num = num.replace(")", "")
            num = num.replace("e", "9")
            num = num.replace("U", "9")
            print("num  " + num)
            if len(num) > 0:
                line.append(int(num))
            else:
                line.append(0)
        result.append(line)

    print(image.size)

    return np.array(result)


def click_up(i, j):
    x = 55 + i * 972 / 9 + 972 / 9 / 2
    y = 220 + j * 972 / 9 + 972 / 9 / 2

    click(x, y)


def click_down(num):
    # 55, 1710, 972, 250 #216,125
    pos = [(1, 163, 1773),
           (2, 379, 1773),
           (3, 595, 1773),
           (4, 811, 1773),
           (5, 1027, 1773),

           (6, 163, 1898),
           (7, 379, 1898),
           (8, 595, 1898),
           (9, 811, 1898)]
    x = pos[num - 1][1]
    y = pos[num - 1][2]

    click(x, y)


def click_screen(title, arr):
    sum = 0
    for j in range(0, 9):
        for i in range(0, 9):

            if title[j][i] > 0:
                continue

            click_up(i, j)
            click_down(arr[j][i])

            sum += 1
            if sum > 3:
                pass
                # return False
    print("Done")
    return True


def run(ip="172.19.33.19", port="5555", button=False):
    if button:
        adb.connect_ip(ip, port)

    screenshot_to_local()

    file_path = "screenshots.png"  # 图片保存的地址
    image = Image.open(file_path)
    title = cut_image(image)
    print(title)
    arr = sudoku.solve2(title)
    print(arr)
    click_screen(title, arr)

    if button:
        adb.disconnect_ip(ip, port)


def test():
    img = cv.imread("screenshots.png")

    start_x, start_y, length_x, length_y = (55, 220, 972, 972)  # 108,108

    cv.rectangle(img, (start_x, start_y), (start_x + length_x, start_y + length_y), (255, 0, 0), 3, 4, 0)

    start_x, start_y, length_x, length_y = (55, 1710, 972, 250)  # 216,125

    cv.rectangle(img, (start_x, start_y), (start_x + length_x, start_y + length_y), (255, 0, 0), 3, 4, 0)

    cv.imwrite('test.jpg', img)

    cv.imwrite('test.jpg', img)


if __name__ == '__main__':
    run()

    #
    # adb tcpip 5555
    # adb connect 172.19.33.19:5555
    # adb disconnect 172.19.33.19:5555
