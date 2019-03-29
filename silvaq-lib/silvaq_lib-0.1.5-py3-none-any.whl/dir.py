"""
将目录相关的常用方法聚集在这里
"""
import os, os.path as path, codecs, chardet, shutil


def maketree(dirs):
    """
    一级，多级都用这个
    os.makedirs(dirs)
    :param str dirs:
    :return:
    """
    os.makedirs(dirs)


# 删除目录
def removetree(dirs):
    """
    一级，多级都用这个
     shutil.rmtree(dirs)
    :param dirs:
    :return:
    """
    shutil.rmtree(dirs)


# 复制目录
def copytree(src, dest):
    """
    一级，多级都用这个
    shutil.copytree(src, dest)
    :param src:
    :param dest:
    :return:
    """
    return shutil.copytree(src, dest)


# 移动目录
def move(src, dest):
    """
    shutil.move(src, dest)
    :param src:
    :param dest:
    :return:
    """
    return shutil.move(src, dest)


def rename(old, new):
    """
     os.rename(old, new)
    :param old:
    :param new:
    :return:
    """
    os.rename(old, new)


# 获取目录下文件列表 listdir
def listdir(dir):
    """
    os.listdir(dir)
    :param dir:
    :return:
    """
    return os.listdir(dir)


# 递归获取 walk
def walk(top, topdown=True, onerror=None, followlinks=False):
    """
     os.walk(top, topdown, onerror, followlinks)
    :param top:
    :param topdown:
    :param onerror:
    :param followlinks:
    :return:
    """
    return os.walk(top, topdown, onerror, followlinks)


def exists(dir):
    """
    os.path.exists(dir)
    :param dir:
    :return:
    """
    return path.exists(dir)


def is_dir(dir):
    """
    os.path.isdir(dir)
    :param dir:
    :return:
    """
    return path.isdir(dir)


def is_abs(dir):
    """
    os.path.isabs(dir)
    :param dir:
    :return:
    """
    return path.isabs(dir)
