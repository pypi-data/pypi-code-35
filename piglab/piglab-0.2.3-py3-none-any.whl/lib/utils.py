#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 通用函数
from __future__ import print_function
import os
import sys
import platform
import subprocess
import time
import json
import math
import datetime
import logging
import traceback
import copy
import hashlib
import socket
import pickle
import zlib
from PIL import Image
from PIL import ImageOps
import cv2
import numpy as np

try:
    import paddle.fluid as fluid
    from paddle.fluid.contrib.trainer import *
    from paddle.fluid.contrib.inferencer import *
except:
    print("not found paddlepaddle!")

# PATH
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.realpath(CUR_PATH + '/../../')
sys.path.append(BASE_PATH)
# print(CUR_PATH, BASE_PATH)

# 公用static目录，通过http://www.yanjingang.com/static/tmp/1.txt 可访问过程文件
STATIC_PATH = BASE_PATH + '/webservice/piglab/upload/'
STATIC_URL = 'http://www.yanjingang.com/piglab/upload/'

NUMERALS = {u'零': 0, u'一': 1, u'二': 2, u'两': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7,
            u'八': 8, u'九': 9, u'十': 10, u'百': 100, u'千': 1000, u'万': 10000, u'亿': 100000000}
SKIP = ['.DS_Store', 'unknow', 'tmp']


def init_logging(log_file="sys", log_path=BASE_PATH, log_level=logging.INFO):
    """初始化默认日志参数"""
    mkdir(log_path + '/log')
    logging.basicConfig(level=log_level,
                        format='[%(levelname)s]\t%(asctime)s:%(relativeCreated)d\t%(filename)s:%(lineno)d\t%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_path + "/log/" + log_file + "." + time.strftime('%Y%m%d%H', time.localtime()) + ".log",
                        filemode='a')
    logging.info("__init_logging__")


def get_trace():
    """获得异常栈内容"""
    try:
        errmsg = "Traceback (most recent call last):\n "
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            errmsg += "  File \"%-23s\", line %s, in %s() \n\t  %s \n" % (filename, linenum, funcname, source)
        errmsg += str(exc_type.__name__) + ": " + str(exc_value)
        # traceback.print_exc()
    except:
        traceback.print_exc()
        errmsg = ''
    return errmsg


def mkdir(path):
    """检查并创建目录"""
    if not os.path.exists(path):
        os.makedirs(path)


def rmdir(path, skips=None):
    """删除目录"""
    # print(path)
    if not os.path.exists(path):
        return
    if os.path.isfile(path):  # 文件
        if skips is None or path not in skips:
            os.unlink(path)
    elif os.path.isdir(path):  # 目录
        for file in os.listdir(path):
            # print(path +'/'+ file)
            rmdir(path + '/' + file, skips=skips)
        if skips is None or path not in skips:
            os.rmdir(path)

def rm(filename):
    """删除文件"""
    # print(filename)
    if os.path.exists(filename):
        os.unlink(filename)

def copy_file(source_file, target_file, remove=False):
    """复制文件"""
    ret = False
    if not os.path.exists(target_file) or (os.path.exists(target_file) and os.path.getsize(target_file) != os.path.getsize(source_file)):
        ret = open(target_file, "wb").write(open(source_file, "rb").read())
    if remove is True:
        if os.path.exists(target_file) and os.path.getsize(target_file) == os.path.getsize(source_file):  # 确保目标文件与源文件完全一致才能删源文件
            ret = os.unlink(source_file)
    return ret


def move_file(source_file, target_file):
    """移动文件"""
    return copy_file(source_file, target_file, remove=True)


def play_sound(filename="warning0.wav"):
    """播放声音（默认声音为报警音）"""
    import pygame
    if filename == '':
        return
    filename = CUR_PATH + '/media/' + filename
    pygame.init()
    # pygame.display.set_mode((100, 50)) #alert window
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(0)

    # clock = pygame.time.Clock()    #wait
    # clock.tick(10)
    while pygame.mixer.music.get_busy():
        pygame.event.poll()
        # clock.tick(10) #每秒循环10次
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


def get_today():
    """获得今天日期"""
    return time.strftime("%Y-%m-%d", time.localtime())


def get_date(timestamp, format='%Y-%m-%d %H:%M:%S'):
    """返回时间戳对应的格式化日期格式"""
    x = time.localtime(float(timestamp))
    return time.strftime(format, x)


def md5(string):
    """生成md5"""
    if isinstance(string, list):
        string = copy.deepcopy(string)
        for i in range(len(string)):
            string[i] = md5(string[i])
            if string[i] == '':
                return ''
                # print string
    elif isinstance(string, str):
        try:
            string = hashlib.md5(string.encode(encoding='UTF-8')).hexdigest()
        except:
            logging.error('md5 fail! [' + string + ']\n' + get_trace())
            return ''
    return string


def pickle_dump(data, data_file):
    """将python对象转为bytes->压缩->保存到文件"""
    # obj -> bytes
    data_bytes = pickle.dumps(data, 4)
    # print(len(data_bytes))
    # compress bytes
    compress_bytes = zlib.compress(data_bytes)
    # print(len(compress_bytes))
    # dump bytes to file
    pickle.dump(compress_bytes, open(data_file, 'wb'), protocol=4)


def pickle_load(data_file):
    """加载保存的压缩文件bytes->解压-转回python对象->"""
    # load file bytes
    compress_bytes = pickle.load(open(data_file, 'rb'), encoding='iso-8859-1')
    # print(len(compress_bytes))
    # decompress bytes
    data_bytes = zlib.decompress(compress_bytes)
    # print(len(data_bytes))
    # bytes -> obj
    data = pickle.loads(data_bytes, encoding='iso-8859-1')
    # print(data)
    return data


def load_data(filename, split=None, loadjson=False):
    '加载词典'
    data = []
    # print filename
    fo = None
    try:
        fo = open(filename, 'r')
        if fo is None:
            return data
        for line in fo:
            line = line.strip()
            if len(line) == 0:
                continue
            if loadjson is True:
                line = json.loads(line)
            elif type(split) is str and len(split) > 0:
                line = line.split(split)
            else:
                line = line.split()
            data.append(line)
    finally:
        if fo:
            fo.close()
    logging.info("load_dict: [" + filename + "][" + str(len(data)) + "]")
    return data


def gen_token(appid, uid, secret_key, token_type='11'):
    """生成token"""
    timestamp = str(int(time.time()))
    # timestamp = '1469618708'
    sign = md5(timestamp + str(uid) + str(appid) + str(secret_key))
    return token_type + '.' + sign + '.' + timestamp + '.' + str(uid) + "-" + str(appid)


def get_video_info(filename):
    """获得视频的fps帧率（即每秒传输帧数）、总帧数、时长等信息"""
    logging.info('__get_video_info__ {}'.format(filename))
    video_info = {
        'fps': 0.0,  # 帧率
        'sum': 0,  # 总帧数
        'seconds': 0,  # 总秒数
        'len': '00:00:00'  # 格式化时长
    }
    if not os.path.exists(filename):
        return video_info
    video = cv2.VideoCapture(filename)

    # get fps帧率
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    if int(major_ver) < 3:
        video_info['fps'] = video.get(cv2.cv.CV_CAP_PROP_FPS)
    else:
        video_info['fps'] = video.get(cv2.CAP_PROP_FPS)
    logging.info('{} {}'.format(filename, video_info['fps']))

    # get sum cap总帧数
    while (True):
        ret, frame = video.read()
        if ret is False:
            break
        video_info['sum'] = video_info['sum'] + 1
    video.release()

    # 计算视频总时长
    video_info['seconds'] = video_info['sum'] / video_info['fps']
    video_info['len'] = format_video_length(video_info['seconds'])

    logging.info('get_video_info res: {}'.format(video_info))
    return video_info


def format_video_length(seconds):
    """格式化视频长度格式（秒数 -> h:m:s格式）"""
    seconds = math.ceil(seconds)  # 向上取整
    s = int(seconds % 60)
    m = int(seconds // 60 % 60)
    h = int(seconds // 60 // 60)
    return '%02d:%02d:%02d' % (h, m, s)


# 自定义mnist数据集reader
def mnist_reader_creator(image_filename, label_filename, buffer_size):
    def reader():
        # 调用命令读取文件，Linux下使用zcat
        if platform.system() == 'Linux':
            zcat_cmd = 'zcat'
        else:
            raise NotImplementedError("This program is suported on Linux,\
                                      but your platform is" + platform.system())

        # 读取mnist图片集
        sub_img = subprocess.Popen([zcat_cmd, image_filename], stdout=subprocess.PIPE)
        sub_img.stdout.read(16)  # 跳过前16个magic字节

        # 读取mnist标签集
        sub_lab = subprocess.Popen([zcat_cmd, label_filename], stdout=subprocess.PIPE)
        sub_lab.stdout.read(8)  # 跳过前8个magic字节

        try:
            while True:  # 前面使用try,故若再读取过程中遇到结束则会退出
                # 批量读取label，每个label占1个字节
                labels = np.fromfile(sub_lab.stdout, 'ubyte', count=buffer_size).astype("int")
                if labels.size != buffer_size:
                    break
                # 批量读取image，每个image占28*28个字节，并转换为28*28的二维float数组
                images = np.fromfile(sub_img.stdout, 'ubyte', count=buffer_size * 28 * 28).reshape(buffer_size, 28, 28).astype("float32")
                # 像素值映射到(-1,1)范围内用于训练
                images = images / 255.0 * 2.0 - 1.0;
                for i in range(buffer_size):
                    yield images[i, :], int(labels[i])  # 将图像与标签抛出，循序与feed_order对应！
        finally:
            try:
                # 结束img读取进程
                sub_img.terminate()
            except:
                pass
            try:
                # 结束label读取进程
                sub_lab.terminate()
            except:
                pass

    return reader


def image_reader_creator(img_path, height, width, rgb=False, reshape1=False, label_split_dot=0, label_split_midline=1, label_list=[]):
    """自定义image目录文件列表reader"""

    def reader():
        imgs = os.listdir(img_path)
        for i in range(len(imgs)):
            if imgs[i] in SKIP:
                continue
            # imgs[i] = '0-5.png'
            # print(imgs[i])
            label = imgs[i].split('.')[label_split_dot]
            if label_split_midline >= 0:
                label = label.split('-')[label_split_midline]
            if type(label_list) is list and len(label_list) > 0:
                label = label_list.index(label)
            if rgb:
                image = load_rgb_image(img_path + imgs[i], height, width)
                # print(image.shape)  #(1, 3, 32, 32)
                image = image[0]
                # print(img_path + imgs[i])
                if reshape1:  # 多维转1维
                    image = image.reshape(-1)
                    # print(image.shape) (3072,)
                #print('{} {} {}'.format(img_path + imgs[i], label, image))
                yield image, int(label)
            else:
                image = load_image(img_path + imgs[i], height, width)
                # print(img_path + imgs[i])
                # print('{} {} {}'.format(img_path + imgs[i], label, image[0][0]))
                yield image[0][0], int(label)

    return reader


def load_rgb_image(img_path, height=32, width=32):
    """加载rgb图片数据"""
    im = Image.open(img_path)
    im = im.resize((height, width), Image.ANTIALIAS)
    im = np.array(im).astype(np.float32)
    # print(im)
    # print(im.shape)    #(32, 32, 3)
    # The storage order of the loaded image is W(width),H(height), C(channel). PaddlePaddle requires the CHW order, so transpose them.
    im = im.transpose((2, 0, 1))  # CHW
    im = im / 255.0
    # print(im.shape)    #(3, 32, 32)

    # Add one dimension to mimic the list format.
    im = np.expand_dims(im, axis=0)
    # print(im.shape)   load_rgb_image #(1, 3, 32, 32)
    return im


def load_image(img_path, height, width, rotate=0, invert=False, sobel=False, ksize=5, dilate=0, erode=0, save_resize=False, mid_imgs=[]):
    """加载黑白图片数据"""
    if sobel:  # 边缘检测
        img_path = image_sobel(img_path, ksize=ksize, dilate=dilate, erode=erode, mid_imgs=mid_imgs)
    # 加载图片
    im = Image.open(img_path).convert('L')
    # 缩略图
    im = im.resize((height, width), Image.ANTIALIAS)
    # 旋转
    if rotate != 0:  # 旋转度数
        im = im.rotate(rotate)
    # 反转颜色(不要跟sobel一起用，因为sobel已经自动转为黑底+白边缘了)
    if invert:
        im = ImageOps.invert(im)
    # 临时保存
    if save_resize:
        name = img_path.split('/')[-1]
        # resize_path = img_path.replace(name,'') + '../tmp/' + name.split('.')[0]+"_"+str(height)+"x"+str(width)+"."+name.split('.')[1]
        mkdir(STATIC_PATH + 'tmp/')
        resize_path = STATIC_PATH + 'tmp/' + name.split('.')[0] + "_" + str(height) + "x" + str(width) + "." + name.split('.')[1]
        print(resize_path)
        im.save(resize_path)
        mid_imgs.append(resize_path)
    # 返回数据
    im = np.array(im).reshape(1, 1, height, width).astype(np.float32)  # [N C H W] N几张图;C=1灰图;H高;W宽
    im = im / 255.0 * 2.0 - 1.0
    return im


def image_sobel(img_path, ksize=5, dilate=0, erode=0, dilate2=0, mid_imgs=[]):
    """图片边缘检测"""
    img = cv2.imread(img_path)
    # 灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # write_image(gray, img_path, 'gray')
    # 高斯平滑
    gaussian = cv2.GaussianBlur(gray, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
    # write_image(gaussian, img_path, 'gaussion')
    # 中值滤波
    median = cv2.medianBlur(gaussian, 5)
    # write_image(median, img_path, 'median')
    # Sobel算子，X方向求梯度,对图像进行边缘检测
    sobel = cv2.Sobel(median, cv2.CV_8U, 1, 0, ksize=ksize)  # ksize:1/3/5/7   cv2.CV_8U/cv2.CV_16S
    # sobel = cv2.Sobel(median, cv2.CV_16S, 1, 0, ksize=ksize) #ksize:1/3/5/7   cv2.CV_8U/cv2.CV_16S
    sobel = cv2.convertScaleAbs(sobel)
    # 二值化
    ret, binary = cv2.threshold(sobel, 170, 255, cv2.THRESH_BINARY)
    threshold_path = write_image(binary, img_path, 'threshold')
    mid_imgs.append(threshold_path)
    if dilate == 0 and erode == 0:
        return threshold_path
    else:
        # 膨胀和腐蚀操作的核函数
        element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
        element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 7))
        # 膨胀一次，让轮廓突出
        dilation = cv2.dilate(binary, element2, iterations=dilate)  # iterations=1
        dilation_path = write_image(dilation, img_path, 'dilation')
        mid_imgs.append(dilation_path)
        if erode > 0:  # 腐蚀，去掉细节
            dilation = cv2.erode(dilation, element1, iterations=erode)  # iterations=1
            dilation_path = write_image(dilation, img_path, 'erosion')
            mid_imgs.append(dilation_path)
        if dilate2 > 0:  # 再次膨胀，让轮廓明显一些
            dilation2 = cv2.dilate(dilation, element2, iterations=dilate2)  # iterations=3设置太大但车牌区域很小时非车牌区域容易边缘连片过度，设置太小但车牌占比过大时容易省简称和后边连不上
            dilation_path = write_image(dilation2, img_path, 'dilation2')
            mid_imgs.append(dilation_path)
        return dilation_path


def write_image(img, img_path, step='', path='tmp'):
    """保存图片并打印"""
    name = img_path.split('/')[-1]
    # img_path = img_path.replace(name, '')
    # print(name)
    # print(img_path)
    mkdir(STATIC_PATH + path)
    if step != '':
        # img_file = img_path+'../'+path+'/'+name.split('.')[0]+'_'+step+'.'+name.split('.')[1]
        img_file = STATIC_PATH + path + '/' + name.split('.')[0] + '_' + step + '.' + name.split('.')[1]
    else:
        # img_file = img_path+'../'+path+'/'+name
        img_file = STATIC_PATH + path + '/' + name
    cv2.imwrite(img_file, img)
    print(img_file)
    return img_file


if __name__ == '__main__':
    """函数测试"""

    """
    mnist_path = BASE_PATH + '/machinelearning/image/digit/data/mnist/'
    train_image   = mnist_path + 'train-images-idx3-ubyte.gz'
    train_label   = mnist_path + 'train-labels-idx1-ubyte.gz'
    for img,label in mnist_reader_creator(train_image,train_label,1)():  #reader
        print(img)
        print(len(img))
        print(len(img[0]))
        print(label)
	break
    for img, label in paddle.dataset.cifar.train10()():  # reader
        print(img)
        print(len(img))
        print(label)
        break

    img_path = BASE_PATH + '/machinelearning/image/dog_cat/data/train/'
    label_list = ["cat", "dog"]
    for img, label in image_reader_creator(img_path, 32, 32, rgb=True, reshape1=True, label_split_midline=-1, label_list=label_list)():  # reader
        print(img)
        print(len(img))
        print(label)
        break
   
    print(md5('B000000115915'))
    print(get_tphid(400, -1))
    print(get_date(1548124450.6668496))
    """

    # model databuffer zip
    """
    data_path = BASE_PATH + '/machinelearning/game/chess/data/databuffer/'
    for data_file in os.listdir(data_path):
        data_file = data_path+data_file
        data = pickle.load(open(data_file, 'rb'), encoding='iso-8859-1')
        pickle_dump(data, data_file + '.data')
        #check
        data2 = pickle_load(data_file + '.data')
        print("{} len:{}".format(data_file, len(data[0])))
        print("{} len:{}".format(data_file + '.data', len(data2[0])))

    data_path = BASE_PATH + '/machinelearning/game/chess/model/'
    for data_file in os.listdir(data_path):
        data_file = data_path+data_file
        data = pickle.load(open(data_file, 'rb'), encoding='iso-8859-1')
        pickle_dump(data, data_file + '.data')
        #check
        data2 = pickle_load(data_file + '.data')
        print("{} len:{}".format(data_file, len(data[0])))
        print("{} len:{}".format(data_file + '.data', len(data2[0])))
    """
