#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import logging
import numpy as np
from PIL import Image, ImageDraw

# PATH
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.realpath(CUR_PATH + '/../../../')
sys.path.append(BASE_PATH)

from machinelearning.lib import utils
from train import Train

# log init
utils.init_logging(log_file='test', log_path=CUR_PATH)

# 生成训练数据
data = utils.load_data(Train.TRAIN_CONF)
print(data)


# Train.create_train_data()


# 获得token
class InnerToken:
    def generateToken(self, appid, uid, sk):
        timestamp = str(int(time.time()))
        # timestamp = '1469618708'
        sign = utils.md5(timestamp + str(uid) + str(appid) + str(sk))
        token = '11.' + sign + '.' + timestamp + '.' + str(uid) + "-" + str(appid)
        return token


if __name__ == '__main__':
    p = InnerToken()
    # print(p.generateToken(8376254, '1884599608', 't6gtosOTYv6aXHy7Gfa5ebVxG2s44Cqp'))
    print(p.generateToken(15716384, '1884599608', 'nP1cmYUEkASzKXRDSYYnTE47oPQZXTnv'))
    print(utils.gen_token(15716384, '1884599608', 'nP1cmYUEkASzKXRDSYYnTE47oPQZXTnv'))


# 获得视频帧率
video_file = "/Users/yanjingang/project/piglab/machinelearning/video/clear_video_ad/data/video/sjkzr.mp4"
#info = utils.get_video_info(video_file)
#print(info)

print(Train.LABEL_LIST)
res = Train.load_label_list()
print(Train.LABEL_LIST)
print(res)

