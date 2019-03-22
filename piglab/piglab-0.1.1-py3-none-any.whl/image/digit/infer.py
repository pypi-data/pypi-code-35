#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 手写数字识别模型测试
# cmd: python infer.py infer_62.jpeg
from __future__ import print_function
import sys
import os
import getopt
import numpy
import paddle.fluid as fluid
from paddle.fluid.contrib.trainer import *
from paddle.fluid.contrib.inferencer import *

# PATH
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.realpath(CUR_PATH + '/../../../')
sys.path.append(BASE_PATH)
#print(CUR_PATH, BASE_PATH)
from machinelearning.lib import utils
from machinelearning.lib import logger
from machinelearning.image.digit import train as digit_train


def infer(img_file='', model_path=CUR_PATH):
    if img_file == '':
        return 1, 'file_name is empty', {}
    file_name = img_file.split('/')[-1]

    # 是否使用GPU
    use_cuda = False  # set to True if training with GPU
    place = fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace()

    params_dirname = model_path + "/model/"  # 模型参数保存目录
    logger.debug('param_path:' + params_dirname )
    height = width = 28

    # 加载测试数据
    imgs = []  # 使用多种不同的预处理方法
    results_mid = []  # 过程图片
    imgs_weight = [1, 0.99, 0.99]  # 不同预处理方法的结果权重
    try:  # 测试集图片
        mid_imgs = []  # 过程图片
        imgs.append(utils.load_image(img_file, height, width, mid_imgs=mid_imgs, save_resize=True))
        results_mid.append(mid_imgs)
    except:
        logger.warning(logger.get_trace())
        imgs.append([])
        results_mid.append([])
    try:  # 白纸手写照片
        if len(file_name.split('_')) > 1 and len(file_name.split('_')[1].split('.')[0]) >= 2 and int(file_name.split('_')[1][1:2]) > 0:  # infer_>=2
            imgs_weight[1] = 5
        elif len(file_name.split('.')) > 1 and file_name.split('.')[0].isdigit() and img_file.count('upload/') > 0:  # 拍照上传的照片
            imgs_weight[1] = 5
        mid_imgs = []  # 过程图片
        imgs.append(utils.load_image(img_file, height, width, rotate=0, sobel=True, save_resize=True, ksize=5, dilate=1, mid_imgs=mid_imgs))
        results_mid.append(mid_imgs)
    except:
        logger.warning(logger.get_trace(), 'infer')
        imgs.append([])
        results_mid.append([])
    try:  # 黑纸粗笔写照片
        mid_imgs = []  # 过程图片
        imgs.append(utils.load_image(img_file, height, width, rotate=0, sobel=True, save_resize=True, ksize=3, dilate=6, erode=1, mid_imgs=mid_imgs))
        results_mid.append(mid_imgs)
    except:
        logger.warning(logger.get_trace(), 'infer')
        imgs.append([])
        results_mid.append([])

    # 使用保存的模型参数+测试图片进行预测
    inferencer = Inferencer(
        # infer_func=digit_train.softmax_regression, # uncomment for softmax regression
        # infer_func=digit_train.multilayer_perceptron, # uncomment for MLP
        infer_func=digit_train.convolutional_neural_network,  # uncomment for LeNet5
        param_path=params_dirname,
        place=place)

    results = []
    results_sum = numpy.ndarray([])
    numpy.set_printoptions(precision=2)
    for i in xrange(len(imgs)):
        if len(imgs[i]) == 0: continue
        result = inferencer.infer({'img': imgs[i]})  # 此输入img的各label概率
        result = numpy.where(result[0][0] > 0.01, result[0][0], 0)  # 概率<1%的直接设置为0
        print(result)
        results.append(result)
        print(numpy.argsort(result))
        results_sum = results_sum + result * imgs_weight[i]  # 累加label下标概率
    # print(imgs_weight)
    # 按概率加和排序
    lab = numpy.argsort(results_sum)  # probs and lab are the results of one batch data
    label = lab[-1]  # 概率倒排最后一个

    # 组织返回结果
    idx = 0
    weight = []
    mid_imgs = []
    for i in xrange(len(results)):
        result = results[i]
        if numpy.argsort(result)[-1] == label:
            weight = list(result.astype(str))
            for img in results_mid[i]:
                mid_imgs.append(img.replace(utils.STATIC_PATH, utils.STATIC_URL))
            idx = i
            break

    print("*idx: %d" % idx)
    print("*label weight sort:")
    print(results_sum)
    print(lab)
    print("*img: %s" % img_file)
    print("*label: %d weight: %s" % (label, weight[label]))

    return 0, '', {'img': img_file, 'label': label, 'weight': weight, 'mid_imgs': mid_imgs, 'idx': idx}


if __name__ == '__main__':
    # default or cmd input img_file
    img_file = CUR_PATH+'/data/image/infer_62.jpeg'
    # img_file = '/home/work/odp/webroot/yanjingang/www/piglab/upload/181220/1545291680131.jpeg'
    # img_file = '/home/work/odp/webroot/yanjingang/www/piglab/upload/181220/1545300858701.jpeg'
    # img_file = '/home/work/piglab/machinelearning/image/digit/train/data/image/infer_62.jpeg'
    opts, args = getopt.getopt(sys.argv[1:], "p:", ["file_name="])
    if len(args) > 0 and len(args[0]) > 4:
        img_file = CUR_PATH+'/data/image/' + args[0]

    ret = infer(img_file)
    print(ret)
