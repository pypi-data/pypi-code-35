#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: clear_video_ad.py
Desc: 清理视频的首尾广告帧
Author:yanjingang(yanjingang@mail.com)
Date: 2019/3/11 11:34
Cmd:
    #视频帧提取（用于视频首尾广告帧边界人工标注）
        python clear_video_ad.py video2photo sjkzr.mp4
        python clear_video_ad.py video2photo fhws.mp4
        python clear_video_ad.py video2photo myft.mp4
        python clear_video_ad.py video2photo myzx.mp4
        python clear_video_ad.py video2photo syjk.mp4
        python clear_video_ad.py video2photo msys.mp4
        python clear_video_ad.py video2photo bohe.mp4
        python clear_video_ad.py video2photo mfk.mp4
        python clear_video_ad.py video2photo plyk.mp4
        python clear_video_ad.py video2photo ylys.mp4
        python clear_video_ad.py video2photo ywyd.mp4
    #使用模型清理视频的首尾广告帧
        python clear_video_ad.py clear sjkzr.mp4 false
        python clear_video_ad.py clear fhws.mp4
        python clear_video_ad.py clear myft.mp4
        python clear_video_ad.py clear myzx.mp4
        python clear_video_ad.py clear syjk.mp4
        python clear_video_ad.py clear msys.mp4
        python clear_video_ad.py clear bohe.mp4 false
        python clear_video_ad.py clear mfk.mp4 false
        python clear_video_ad.py clear plyk.mp4 false
        python clear_video_ad.py clear ylys.mp4 false
        python clear_video_ad.py clear ywyd.mp4 false
        #批量下载并清理
        down_clear.sh

    grep clear_video_ad.py log/clearvideoad_sjkzr*
"""

import os
import sys
import logging
import numpy as np

# PATH
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.realpath(CUR_PATH + '/../../../')
sys.path.append(BASE_PATH)

from machinelearning.lib import utils
from train import Train
from infer import Infer


class ClearVideoAD():
    """视频片头片尾识别"""
    VIDEO_PATH = CUR_PATH + "/data/video/"  # 视频数据保存位置

    def __init__(self):
        """init"""
        utils.mkdir(Train.VIDEO_PATH)

    @staticmethod
    def video2photo(video_file):
        """视频帧提取"""
        video_name = ClearVideoAD._get_video_name(video_file)
        logging.info("__video2photo__ {} {}".format(video_file, video_name))
        # photo path
        photo_path = Train.PHOTO_PATH + video_name + '/'
        if os.path.exists(photo_path) and len(os.listdir(photo_path)) > 1:
            logging.warning("photo_path exists! {}".format(photo_path))
            return photo_path
        utils.mkdir(photo_path)
        # video -> photo
        cmd = 'ffmpeg -i {} {}video-%d.png'.format(video_file, photo_path)
        logging.info("cmd: {}  ".format(cmd))
        output = os.popen(cmd)
        res = output.read()
        logging.info(res)
        logging.info("video2photo res: {}".format(photo_path))
        return photo_path

    @staticmethod
    def get_content_pos(photo_path=None, video_info=None, check_ratio=0.15, ad_limit=10, ad_weight=0.9999):
        """获得视频的正文坐标：清理视频的首尾广告帧"""
        if photo_path is None:
            photo_path = Train.PHOTO_PATH + 'sjkzr/'
        logging.info("__get_content_pos__ {}".format(photo_path))

        infer = Infer()
        # 检测首尾广告
        logging.info("get_content_pos start: {}  sum:{}  video_info:{}".format(photo_path, sum, video_info))
        pos = {'sum': video_info['sum'], 'start': 0, 'end': video_info['sum'], 'time': {'ss': '0:0:0', 't': video_info['len']}}  # ss:开始时间， t:持续时间
        last_weight = []  # 最近n次的分数
        for i in range(video_info['sum']):
            filename = "video-{}.png".format(i)
            img_file = photo_path + filename
            # print(img_file)
            ratio = round(i / video_info['sum'], 2)
            if filename in utils.SKIP or not os.path.exists(img_file) or (ratio > check_ratio and ratio < (1 - check_ratio)):  # 只判断首尾12%部分
                continue
            # logging.info(img_file)

            # 预测
            ret, msg, res = infer.image_infer(img_file, printf=False)

            if (ratio < check_ratio and res['label_name'].split('_')[1] == 'e') or (ratio > (1 - check_ratio) and res['label_name'].split('_')[1] == 's'):
                res['weight'] = 0.0  # 首尾识别反的，概率置0
            # else:
            #    res['weight'] = round(res['weight'], 4)
            last_weight.append(res['weight'])
            if len(last_weight) > ad_limit * 2:  # 定长长度: ad_limit * 2
                last_weight.pop(0)
            x = np.array(last_weight)
            ad_cnt = len(x[np.where(x > ad_weight)])  # 最近ad_limit*次帧里有几个广告
            if ratio < check_ratio and res['weight'] < ad_weight and ad_cnt >= ad_limit:  # 正文开始
                pos['start'] = i - (ad_limit * 2 - ad_cnt) + 2 + res['label_info']['sp']
                pos['time']['ss'] = utils.format_video_length(pos['start'] / video_info['fps'])
                pos['time']['t'] = utils.format_video_length(pos['end'] / video_info['fps'] - pos['start'] / video_info['fps'])
            if ratio > (1 - check_ratio) and res['weight'] > ad_weight and ad_cnt == ad_limit:  # 片尾广告定位
                pos['end'] = i - ad_cnt + res['label_info']['ep']
                pos['time']['t'] = utils.format_video_length(pos['end'] / video_info['fps'] - pos['start'] / video_info['fps'])
            logging.info("{} {}% {}: {} {} {}\t{}".format(i, ratio, filename, ad_cnt, res['weight'], res['label_name'], pos))

        logging.info("get_content_pos res: {}  ".format(pos))
        return pos

    @staticmethod
    def create_content_video(video_file, pos, clear_tmpfile=True):
        """使用清理后的图片帧逆向为视频"""
        logging.info("__create_content_video__ {} {}".format(video_file, pos))
        video_name = ClearVideoAD._get_video_name(video_file)
        output_path = os.path.dirname(video_file) + '/'  # 输出到原视频位置.out
        # 0.从图片帧目录中获取正文帧并重置文件序号
        photo_path = Train.PHOTO_PATH + video_name + '/'
        tmp_path = Train.TMP_PATH + video_name + '/'
        utils.rmdir(tmp_path)  # clear tmp path
        logging.info("0. clear video-%d.png to: {}  ".format(tmp_path))
        n = 0
        for i in range(pos['sum']):
            filename = "video-{}.png".format(i)
            img_file = photo_path + filename
            if not os.path.exists(img_file):
                continue
            if i < pos['start'] or i > pos['end']:
                continue
            # cp
            utils.mkdir(tmp_path)
            n += 1
            utils.copy_file(img_file, tmp_path + "video-{}.png".format(n))
        # 1.图片帧逆向出正文视频png to mp4
        video_cut_file = '{}{}.cut.mp4'.format(output_path, video_name)
        if os.path.exists(video_cut_file):
            os.remove(video_cut_file)
        cmd = 'ffmpeg -i {}video-%d.png  -c:v libx264 -vf "fps=25,format=yuv420p" {}'.format(tmp_path, video_cut_file)
        logging.info("1. png->cut.mp4  cmd: {}  ".format(cmd))
        output = os.popen(cmd)
        res = output.read()
        logging.info(res)
        if clear_tmpfile:
            utils.rmdir(tmp_path)
        # 2.提取音频
        audio_file = '{}{}.mp3'.format(output_path, video_name)
        if os.path.exists(audio_file):
            os.remove(audio_file)
        cmd = 'ffmpeg -y -i {} -vn -ar 44100 -ac  192 -f mp3 {}'.format(video_file, audio_file)
        logging.info("2. get audio mp3  cmd: {}  ".format(cmd))
        output = os.popen(cmd)
        res = output.read()
        logging.info(res)
        # 3.裁剪音频
        audio_cut_file = '{}{}.cut.mp3'.format(output_path, video_name)
        if os.path.exists(audio_cut_file):
            os.remove(audio_cut_file)
        cmd = 'ffmpeg -y -vn -ss {} -t {} -i {} -acodec copy  {}'.format(pos['time']['ss'], pos['time']['t'], audio_file, audio_cut_file)
        logging.info("3. cut mp3  cmd: {}  ".format(cmd))
        output = os.popen(cmd)
        res = output.read()
        logging.info(res)
        # 4.视频&音频合并
        output_file = '{}{}.out.mp4'.format(output_path, video_name)
        if os.path.exists(output_file):
            os.remove(output_file)
        cmd = 'ffmpeg -y -i {} -i {} -vcodec copy -acodec copy {}'.format(video_cut_file, audio_cut_file, output_file)
        logging.info("4. merge cut_video&cut_audio  cmd: {}  ".format(cmd))
        output = os.popen(cmd)
        res = output.read()
        logging.info(res)
        # clear tmp file
        if clear_tmpfile:
            utils.rm(audio_file)
            utils.rm(audio_cut_file)
            utils.rm(video_cut_file)
        logging.info("create_content_video res: {}".format(output_file))
        return output_file

    @staticmethod
    def cut_content_video(video_file, pos):
        """直接用原视频+时间段裁剪出正文视频"""
        logging.info("__cut_content_video__ {} {}".format(video_file, pos))
        video_name = ClearVideoAD._get_video_name(video_file)
        output_path = os.path.dirname(video_file) + '/'  # 输出到原视频位置.out
        output_file = '{}{}.clear.mp4'.format(output_path, video_name)
        if os.path.exists(output_file):
            os.remove(output_file)
        # cut video
        cmd = 'ffmpeg -ss {} -t {} -i {} -codec copy {}'.format(pos['time']['ss'], pos['time']['t'], video_file, output_file)  # -accurate_seek
        logging.info("cut cmd: {}  ".format(cmd))
        output = os.popen(cmd)
        res = output.read()
        logging.info(res)
        logging.info("cut_content_video res: {}".format(output_file))
        return output_file

    @staticmethod
    def _get_video_name(video_file):
        """从视频路径中获取名称"""
        return os.path.basename(video_file).split('.')[0]

    @staticmethod
    def clear_video_ad(video_file, clear_tmpfile=True):
        """使用模型清理视频中的广告"""
        logging.info("__clear_video_ad__ {}".format(video_file))
        # 获取视频信息（帧率/帧数/时长等信息）
        video_info = utils.get_video_info(video_file)
        print(video_info)

        # 视频帧提取（默认输出到./data/photo/video-%d.png）
        photo_path = ClearVideoAD.video2photo(video_file)
        print(photo_path)

        # 识别帧首尾广告边界，返回正文区间位置信息
        pos = ClearVideoAD.get_content_pos(photo_path, video_info)
        print(pos)

        # 裁剪出正文视频（默认输出到原视频位置/$video_name.out.mp4）
        output_file = ClearVideoAD.cut_content_video(video_file, pos)
        # 逆向生成正文视频（默认输出到原视频位置/$video_name.out.mp4）
        # output_file = ClearVideoAD.create_content_video(video_file, pos, clear_tmpfile=clear_tmpfile)
        print(output_file)

        # clear photo (磁盘容量不足)
        if clear_tmpfile:
            utils.rmdir(photo_path)

        res = {'video': video_info, 'photo': photo_path, 'pos': pos, 'output': output_file}
        logging.info("clear_video_ad res: {}".format(res))
        return res


if __name__ == '__main__':
    """test"""
    optype = 'clear'
    if len(sys.argv) >= 2:
        optype = sys.argv[1]
    video_file = ClearVideoAD.VIDEO_PATH + 'sjkzr.mp4'
    if len(sys.argv) >= 3:
        video_file = sys.argv[2]
        if video_file.count('/') == 0:  # video path
            video_file = ClearVideoAD.VIDEO_PATH + video_file

    # log init
    log_file = ClearVideoAD.__name__.lower() + '_' + os.path.basename(video_file) + '-' + str(os.getpid())
    utils.init_logging(log_file=log_file, log_path=CUR_PATH)
    print("log_file: {}".format(log_file))

    # 视频帧提取（用于视频首尾广告帧边界人工标注）
    if optype == 'video2photo':
        photo_path = ClearVideoAD.video2photo(video_file)
        print(photo_path)

    # 清理视频的首尾广告帧
    if optype == 'clear':
        clear_tmpfile = True
        if len(sys.argv) >= 4:
            clear_tmpfile = False if sys.argv[3].lower() == 'false' else True
        # clear
        res = ClearVideoAD.clear_video_ad(video_file, clear_tmpfile)
        print(res)
