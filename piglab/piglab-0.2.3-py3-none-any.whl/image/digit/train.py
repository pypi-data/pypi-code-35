#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 使用fluid学习cnn图像识别手写数字
from __future__ import print_function
import os
import sys
import numpy
import paddle
import paddle.fluid as fluid
from paddle.fluid.contrib.trainer import *
from paddle.fluid.contrib.inferencer import *

# PATH
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.realpath(CUR_PATH + '/../../../')
sys.path.append(BASE_PATH)
# print(CUR_PATH, BASE_PATH)
from machinelearning.lib import utils


# 定义输入层及网络结构: 单层全连接层+softmax
def softmax_regression():
    img = fluid.layers.data(name='img', shape=[1, 28, 28], dtype='float32')
    predict = fluid.layers.fc(input=img, size=10, act='softmax')
    return predict


# 定义输入层及网络结构: 多层感知器+relu*2+softmax(Multilayer Perceptron, MLP)
def multilayer_perceptron():
    img = fluid.layers.data(name='img', shape=[1, 28, 28], dtype='float32')
    # first fully-connected layer, using ReLu as its activation function
    hidden = fluid.layers.fc(input=img, size=128, act='relu')
    # second fully-connected layer, using ReLu as its activation function
    hidden = fluid.layers.fc(input=hidden, size=64, act='relu')
    # The thrid fully-connected layer, note that the hidden size should be 10,
    # which is the number of unique digits
    prediction = fluid.layers.fc(input=hidden, size=10, act='softmax')
    return prediction


# 定义输入层及网络结构: 卷积神经网络(Convolutional Neural Network, CNN)
def convolutional_neural_network():
    img = fluid.layers.data(name='img', shape=[1, 28, 28], dtype='float32')
    # first conv pool
    conv_pool_1 = fluid.nets.simple_img_conv_pool(
        input=img,
        filter_size=5,
        num_filters=20,
        pool_size=2,
        pool_stride=2,
        act="relu")
    conv_pool_1 = fluid.layers.batch_norm(conv_pool_1)
    # second conv pool
    conv_pool_2 = fluid.nets.simple_img_conv_pool(
        input=conv_pool_1,
        filter_size=5,
        num_filters=50,
        pool_size=2,
        pool_stride=2,
        act="relu")
    # output layer with softmax activation function. size = 10 since there are only 10 possible digits.
    prediction = fluid.layers.fc(input=conv_pool_2, size=10, act='softmax')
    return prediction


def optimizer_program():
    """定义优化器"""
    return fluid.optimizer.Adam(learning_rate=0.001)


# 定义训练损失函数
def train_program():
    # 定义训练用label数据层
    label = fluid.layers.data(name='label', shape=[1], dtype='int64')

    # 定义网络结构
    # predict = softmax_regression() # uncomment for Softmax
    # predict = multilayer_perceptron() # uncomment for MLP
    predict = convolutional_neural_network()  # uncomment for LeNet5

    # 定义cost损失函数
    cost = fluid.layers.cross_entropy(input=predict, label=label)
    avg_cost = fluid.layers.mean(cost)
    # acc用于在迭代过程中print
    acc = fluid.layers.accuracy(input=predict, label=label)
    return [avg_cost, acc]


def main():
    # 定义训练和测试数据batch reader
    # mnist_path = CUR_PATH + '/data/mnist/'
    mnist_path = '~/.cache/paddle/dataset/mnist/'
    train_image = mnist_path + 'train-images-idx3-ubyte.gz'
    train_label = mnist_path + 'train-labels-idx1-ubyte.gz'
    test_image = mnist_path + 't10k-images-idx3-ubyte.gz'
    test_label = mnist_path + 't10k-labels-idx1-ubyte.gz'
    img_path = CUR_PATH + '/data/'
    train_reader = paddle.batch(paddle.reader.shuffle(
        # paddle.dataset.mnist.train(),
        # utils.mnist_reader_creator(train_image, train_label, buffer_size=100),  # 自己读取mnist训练集
        utils.image_reader_creator(img_path + 'train/', 28, 28),  # 自己读取images
        buf_size=500),
        batch_size=64)
    test_reader = paddle.batch(
        # paddle.dataset.mnist.test(),
        # utils.mnist_reader_creator(test_image, test_label, buffer_size=100),  # 自己读取mnist测试集
        utils.image_reader_creator(img_path + 'test/', 28, 28),  # 自己读取images
        batch_size=64)

    # 是否使用GPU
    use_cuda = False  # set to True if training with GPU
    place = fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace()

    # 创建训练器(train_func损失函数; place是否使用gpu; optimizer_func优化器)
    trainer = Trainer(train_func=train_program, place=place, optimizer_func=optimizer_program)

    # 模型参数保存目录
    params_dirname = CUR_PATH + "/model"
    # 定义event_handler，输出训练过程中的结果
    lists = []

    def event_handler(event):
        if isinstance(event, EndStepEvent):  # 每步触发事件
            if event.step % 100 == 0:
                # event.metrics maps with train program return arguments.
                # event.metrics[0] will yeild avg_cost and event.metrics[1] will yeild acc in this example.
                print("Pass %d, Batch %d, Cost %f" % (event.step, event.epoch,
                                                      event.metrics[0]))
        if isinstance(event, EndEpochEvent):  # 每次迭代触发事件
            # test的返回值就是train_func的返回值
            avg_cost, acc = trainer.test(
                reader=test_reader, feed_order=['img', 'label'])
            print("Test with Epoch %d, avg_cost: %s, acc: %s" %
                  (event.epoch, avg_cost, acc))
            # 保存模型参数
            trainer.save_params(params_dirname)
            # 保存训练结果损失情况
            lists.append((event.epoch, avg_cost, acc))

    # 开始训练模型
    trainer.train(
        num_epochs=5,   #Best pass is 3, classification accuracy is 98.74%
        event_handler=event_handler,
        reader=train_reader,
        feed_order=['img', 'label'])

    # 找到训练误差最小的一次结果(trainer.save_params()自动做了最优选择，这里只用于确定num_epochs)
    best = sorted(lists, key=lambda list: float(list[1]))[0]
    print('Best pass is %s, testing Avgcost is %s' % (best[0], best[1]))
    print('The classification accuracy is %.2f%%' % (float(best[2]) * 100))

    # 加载测试数据
    img = utils.load_image(CUR_PATH + '/data/image/infer_52.jpeg', 28, 28)

    # 使用保存的模型参数+测试图片进行预测
    inferencer = Inferencer(
        # infer_func=softmax_regression, # uncomment for softmax regression
        # infer_func=multilayer_perceptron, # uncomment for MLP
        infer_func=convolutional_neural_network,  # uncomment for LeNet5
        param_path=params_dirname,
        place=place)
    results = inferencer.infer({'img': img})
    lab = numpy.argsort(results)  # probs and lab are the results of one batch data
    print("Inference result : %d" % lab[0][0][-1])


if __name__ == '__main__':
    main()
