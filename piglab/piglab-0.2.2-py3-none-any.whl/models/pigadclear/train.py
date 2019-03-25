#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: train.py
Desc: 视频片头片尾识别模型训练类
Author:yanjingang(yanjingang@mail.com)
Date: 2019/3/11 11:34
Cmd: python train.py
"""

from __future__ import print_function
import sys
import os
import logging
import paddle
import paddle.fluid as fluid
from paddle.fluid.contrib.trainer import *
from paddle.fluid.contrib.inferencer import *
import numpy

# PATH
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.realpath(CUR_PATH + '/../../../')
sys.path.append(BASE_PATH)

# logging.info(CUR_PATH, BASE_PATH)
from machinelearning.lib.resnet import resnet_cifar100
from machinelearning.lib import utils


class Train():
    """视频片头片尾识别模型训练"""
    PHOTO_PATH = CUR_PATH + "/data/photo/"  # 视频帧图片保存位置
    AD_PATH = CUR_PATH + "/data/ad/"  # ad素材保存位置
    TRAIN_PATH = CUR_PATH + "/data/train/"  # 训练数据集
    TEST_PATH = CUR_PATH + "/data/test/"  # 测试数据集
    TMP_PATH = CUR_PATH + "/data/tmp/"  # 临时保存位置
    TRAIN_CONF = CUR_PATH + "/conf/train.conf"
    # label名称
    LABEL_LIST = []
    LABEL_INFO = []

    def __init__(self):
        """init"""
        # path init
        utils.mkdir(Train.PHOTO_PATH)
        utils.mkdir(Train.AD_PATH)
        utils.mkdir(Train.TRAIN_PATH)
        utils.mkdir(Train.TEST_PATH)
        # reload
        Train.load_label_list()

    @staticmethod
    def load_label_list():
        """更新label_list"""
        data = utils.load_data(Train.TRAIN_CONF)
        # print(data)
        Train.LABEL_LIST = ['unknow']
        Train.LABEL_INFO = [
            {
                'type': 'unknow',  # 类型
                'name': 'unknow',  # 名称
                'spos_a': 0,  # 片头广告起始位置
                'spos_b': 0,  # 片头广告结束位置
                'epos_a': 0,  # 片尾广告起始位置
                'epos_b': 0,  # 片尾广告结束位置
                'sp': 0,  # 片头广告裁剪pos偏移量
                'ep': 0,  # 片尾广告裁剪pos偏移量
            }
        ]
        for v_type, name, spos_a, spos_b, epos_a, epos_b, sp, ep in data:
            Train.LABEL_LIST.append(v_type + '_s')
            Train.LABEL_LIST.append(v_type + '_e')
            try:
                spos_a = int(spos_a)
                spos_b = int(spos_b)
                epos_a = int(epos_a)
                epos_b = int(epos_b)
                sp = int(sp)
                ep = int(ep)
            except:
                pass
            Train.LABEL_INFO.append({'type': v_type + '_s', 'name': name + '_s', 'spos_a': spos_a, 'spos_b': spos_b, 'epos_a': epos_a, 'epos_b': epos_b, 'sp': sp, 'ep': 0})
            Train.LABEL_INFO.append({'type': v_type + '_e', 'name': name + '_e', 'spos_a': spos_a, 'spos_b': spos_b, 'epos_a': epos_a, 'epos_b': epos_b, 'sp': 0, 'ep': ep})
        return Train.LABEL_INFO

    @staticmethod
    def create_train_data():
        """使用face数据生成训练数据（10%用于测试）"""
        logging.info('__create_train_data__')
        # clearlabel_list
        utils.mkdir(Train.AD_PATH)
        utils.rmdir(Train.TEST_PATH)
        utils.mkdir(Train.TEST_PATH)
        utils.rmdir(Train.TRAIN_PATH)
        utils.mkdir(Train.TRAIN_PATH)
        # 加载配置
        data = utils.load_data(Train.TRAIN_CONF)
        print(data)
        # create
        num = {'train': 0, 'test': 0, 'vtypes': {}}
        for v_type, name, spos_a, spos_b, epos_a, epos_b in data:
            source_path = Train.PHOTO_PATH + v_type
            if not os.path.exists(source_path) or len(os.listdir(source_path)) < 2:  # 如果photo目录因磁盘空间原因已删除，就到ad目录下找备份
                source_path = Train.AD_PATH + v_type
                if not os.path.exists(source_path) or len(os.listdir(source_path)) < 2:
                    logging.warning("train data not exists! {}".format(source_path))
                    continue
            spos_a = int(spos_a)
            spos_b = int(spos_b)
            epos_a = int(epos_a)
            epos_b = int(epos_b)
            i = 0
            source_files = os.listdir(source_path)
            logging.info('list path: {}'.format(source_path))
            utils.mkdir(Train.AD_PATH + v_type)
            for filename in source_files:
                source_file = source_path + '/' + filename
                if filename in utils.SKIP or len(filename.split('-')) < 2:
                    continue

                n = int(filename.split('-')[1].split('.')[0])
                if n >= spos_a and (n <= spos_b and spos_b > 0):  # 片头
                    vtype = v_type + '_s'
                elif epos_a > 0 and n >= epos_a and (epos_b == 0 or (n <= epos_b and epos_b > 0)):  # 片尾
                    vtype = v_type + '_e'
                else:
                    continue
                logging.debug("{} {} {} {} {} {} {}".format(source_file, n, spos_a, spos_b, epos_a, epos_b, vtype))
                if vtype not in num['vtypes']:
                    num['vtypes'][vtype] = 0
                num['vtypes'][vtype] += 1
                target_file = "{}.{}.png".format(vtype, n)
                if i % 10 == 0:
                    target_file = Train.TEST_PATH + target_file
                    num['test'] += 1
                else:
                    target_file = Train.TRAIN_PATH + target_file
                    num['train'] += 1

                # train path
                utils.copy_file(source_file, target_file)
                # logging.debug("copy: {} -> {}".format(source_file, target_file))
                # backup to ad path
                utils.copy_file(source_file, "{}{}/{}".format(Train.AD_PATH, v_type, filename))

                i += 1
        logging.info('create_train_data done! {}'.format(num))
        return num

    @staticmethod
    def image_classification_network():
        """定义图像分类输入层及网络结构: resnet or vgg"""
        # 输入层：The image is 32 * 32 with RGB representation.
        data_shape = [3, 32, 32]
        images = fluid.layers.data(name='img', shape=data_shape, dtype='float32')

        # 网络模型
        # resnet
        predict = resnet_cifar100(images, 32)
        # vgg
        # predict = vgg_bn_drop(images) # un-comment to use vgg net
        return predict

    @staticmethod
    def optimizer_program():
        """定义优化器"""
        return fluid.optimizer.Adam(learning_rate=0.001)

    @staticmethod
    def train_network():
        """定义训练输入层、网络结果、label数据层、损失函数等训练参数"""
        # 定义输入img层及网络结构resnet
        predict = Train.image_classification_network()
        # 定义训练用label数据层
        label = fluid.layers.data(name='label', shape=[1], dtype='int64')
        # 定义训练损失函数cost
        cost = fluid.layers.cross_entropy(input=predict, label=label)
        avg_cost = fluid.layers.mean(cost)
        # accuracy用于在迭代过程中print
        accuracy = fluid.layers.accuracy(input=predict, label=label)
        return [avg_cost, accuracy]

    @staticmethod
    def train(use_cuda, params_dirname="model/adclassification"):
        """开始训练"""
        if use_cuda and not fluid.core.is_compiled_with_cuda():
            return
        BATCH_SIZE = 256
        EPOCH_NUM = 500  # Best pass is 415, testing Avgcost is 0.00023589146439917386, classification accuracy is 100.00%

        # 定义训练和测试数据batch reader
        train_reader = paddle.batch(
            paddle.reader.shuffle(
                utils.image_reader_creator(CUR_PATH + '/data/train/', 32, 32, rgb=True, reshape1=True, label_split_midline=-1, label_list=Train.LABEL_LIST)  # 自己读取images
                , buf_size=50000),
            batch_size=BATCH_SIZE)
        test_reader = paddle.batch(
            utils.image_reader_creator(CUR_PATH + '/data/test/', 32, 32, rgb=True, reshape1=True, label_split_midline=-1, label_list=Train.LABEL_LIST)  # 自己读取images
            , batch_size=BATCH_SIZE)

        # 定义event_handler，输出训练过程中的结果
        lists = []

        def event_handler(event):
            if isinstance(event, EndStepEvent):
                if event.step % 100 == 0:
                    logging.info("Pass %d, Batch %d, Cost %f, Acc %f" % (event.step, event.epoch, event.metrics[0], event.metrics[1]))
                else:
                    sys.stdout.write('.')
                    sys.stdout.flush()

            if isinstance(event, EndEpochEvent):
                avg_cost, accuracy = trainer.test(reader=test_reader, feed_order=['img', 'label'])

                logging.info('  Test with Pass {0}, Loss {1:2.2}, Acc {2:2.2}'.format(event.epoch, avg_cost, accuracy))
                if params_dirname is not None:
                    trainer.save_params(params_dirname)
                # 保存训练结果损失情况
                lists.append((event.epoch, avg_cost, accuracy))

        # 创建训练器(train_func损失函数; place是否使用gpu; optimizer_func优化器)
        place = fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace()
        trainer = Trainer(train_func=Train.train_network, optimizer_func=Train.optimizer_program, place=place)

        # 开始训练模型
        trainer.train(
            reader=train_reader,
            num_epochs=EPOCH_NUM,
            event_handler=event_handler,
            feed_order=['img', 'label'])

        # 找到训练误差最小的一次结果(trainer.save_params()自动做了最优选择，这里只是为了验证EPOCH_NUM设置几次比较合理)
        best = sorted(lists, key=lambda list: float(list[1]))[0]
        logging.info('Best pass is %s, testing Avgcost is %s' % (best[0], best[1]))
        logging.info('The classification accuracy is %.2f%%' % (float(best[2]) * 100))

    @staticmethod
    def infer(use_cuda, params_dirname="model/adclassification"):
        """使用模型测试"""
        if use_cuda and not fluid.core.is_compiled_with_cuda():
            return
        place = fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace()
        inferencer = Inferencer(infer_func=Train.image_classification_network, param_path=params_dirname, place=place)

        img = utils.load_rgb_image(CUR_PATH + '/data/test/myzx_s.100.png')

        # 预测
        results = inferencer.infer({'img': img})

        logging.info("infer results: %s" % Train.LABEL_LIST[numpy.argmax(results[0])])


if __name__ == '__main__':
    use_cuda = False

    # log init
    log_file = 'train-' + str(os.getpid())
    utils.init_logging(log_file=log_file, log_path=CUR_PATH)
    print("log_file: {}".format(log_file))

    # create train&test data
    res = Train.create_train_data()
    # load label list
    Train.load_label_list()
    print("label_list: {}".format(Train.LABEL_LIST))

    # train
    Train.train(use_cuda=use_cuda)
    # infer
    Train.infer(use_cuda=use_cuda)
