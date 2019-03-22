#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: download_image.py
Desc: 从百度图片下载指定图片
Author:yanjingang(yanjingang@mail.com)
Date: 2019/2/27 23:34
Cmd: python ~/project/piglab/machinelearning/lib/download_image.py
"""

import os
import sys
import re
import uuid
import requests

# PATH
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.realpath(CUR_PATH + '/../../')
sys.path.append(BASE_PATH)
#print(CUR_PATH, BASE_PATH)

from machinelearning.lib import utils


class DownloadImages:
    """从百度图片下载指定图片"""
    def __init__(self, download_max, key_word, save_path=None):
        self.download_sum = 0
        self.download_max = download_max
        self.key_word = key_word
        self.save_path = save_path
        if self.save_path is None:
            self.save_path = "{}/output/download/{}/".format(BASE_PATH, utils.get_date())
        utils.mkdir(self.save_path)
        print(self.save_path)

    def start(self):
        self.download_sum = 0
        gsm = 80
        str_gsm = str(gsm)
        pn = 0
        while self.download_sum < self.download_max:
            str_pn = str(self.download_sum)
            url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&' \
                  'word=' + self.key_word + '&pn=' + str_pn + '&gsm=' + str_gsm + '&ct=&ic=0&lm=-1&width=0&height=0'
            print(url)
            result = requests.get(url)
            self.downloadImages(result.text)
        print('下载完成')

    def downloadImages(self, html):
        img_urls = re.findall('"objURL":"(.*?)",', html, re.S)
        print('找到关键词:' + self.key_word + '的图片，现在开始下载图片...')
        for img_url in img_urls:
            print('正在下载第' + str(self.download_sum + 1) + '张图片，图片地址:' + str(img_url))
            try:
                pic = requests.get(img_url, timeout=50)
                # pic_name = self.save_path + '/' + str(uuid.uuid1()) + '.jpg'
                pic_name = self.save_path + '/' + str(self.download_sum + 1) + '.jpg'
                with open(pic_name, 'wb') as f:
                    f.write(pic.content)
                self.download_sum += 1
                if self.download_sum >= self.download_max:
                    break
            except:
                print('【错误】当前图片无法下载，%s' % utils.get_trace())
                continue


if __name__ == '__main__':
    """test"""
    # log init
    log_file = 'download_image-' + str(os.getpid())
    utils.init_logging(log_file=log_file, log_path=BASE_PATH)
    print("log_file: {}".format(log_file))


    #down = DownloadImages(80, '雪诺', '/Users/yanjingang/project/faceswap/data/photo/snow/')
    #down.start()
    down = DownloadImages(80, '黄蓉 翁美玲', '/Users/yanjingang/project/faceswap/data/photo/huangrong/')
    down.start()
    down = DownloadImages(80, '郭靖 黄日华', '/Users/yanjingang/project/faceswap/data/photo/guojing/')
    down.start()
