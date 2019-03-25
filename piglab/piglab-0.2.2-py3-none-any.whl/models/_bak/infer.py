#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: infer.py
Desc: 人脸识别预测
Author:yanjingang(yanjingang@mail.com)
Date: 2019/2/21 23:34
Cmd: python infer.py ./data/test/myft_e.80.jpg
"""

from __future__ import print_function
import sys
import os
import getopt
import logging
import paddle.fluid as fluid
from paddle.fluid.contrib.trainer import *
from paddle.fluid.contrib.inferencer import *
import numpy as np
import tensorflow as tf

# PATH
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.realpath(CUR_PATH + '/../../../')
sys.path.append(BASE_PATH)

from machinelearning.lib import utils
from train import Train


class Infer():
    """预测"""

    def __init__(self, params_dirname=CUR_PATH, use_cuda=False):
        if use_cuda and not fluid.core.is_compiled_with_cuda():
            exit('compiled is not with cuda')

        # load label list
        Train.load_label_list()

        place = fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace()
        logging.info('param_path:' + params_dirname + '/model/adclassification')
        self.inferencer = Inferencer(infer_func=Train.image_classification_network, param_path=params_dirname + '/model/adclassification', place=place)

    def image_infer(self, img_file='', printf=True):
        """使用模型测试"""
        if img_file == '':
            return 1, 'file_name is empty', {}

        # 预测
        img = utils.load_rgb_image(img_file)
        # logging.info(img.shape)
        result = self.inferencer.infer({'img': img})
        result = np.where(result[0][0] > 0.05, result[0][0], 0)  # 概率<5%的直接设置为0
        logging.debug(result)
        label = np.argmax(result)
        # logging.info(Train.LABEL_LIST)
        # print(label)
        label_name = Train.LABEL_LIST[label]
        label_info = Train.LABEL_INFO[label]
        weight = result[label]

        if printf is True:
            print("***********************************")
            print("*img: {}".format(img_file))
            print("*label: {}".format(label))
            print("*label_name: {}".format(label_name))
            print("*label weight: {}".format(weight))
            print("*label info: {}".format(label_info))
            print("***********************************")

        return 0, '', {'src': img_file, 'label': label, 'label_name': label_name, 'label_info': label_info, 'weight': float(weight)}


if __name__ == '__main__':
    """infer test"""
    img_file = CUR_PATH + '/data/test/sjkzr_s.10.png'
    opts, args = getopt.getopt(sys.argv[1:], "p:", ["file_name="])
    if len(args) > 0 and len(args[0]) > 4:
        img_file = args[0]

    # log init
    log_file = 'infer-' + str(os.getpid())
    utils.init_logging(log_file=log_file, log_path=CUR_PATH)
    print("log_file: {}".format(log_file))

    infer = Infer()

    # infer
    ret = infer.image_infer(img_file)
    logging.info(ret)
