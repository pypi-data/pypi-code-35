# coding=utf-8
from __future__ import print_function

import base64
import hashlib
import os
import shutil


def safeMkdirs(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
    return path


def safeMkdirsForFile(filepath):
    return safeMkdirs(os.path.dirname(os.path.abspath(filepath)))


def mkdirs(path, parent=False):
    mkdirFunction = safeMkdirsForFile if parent else safeMkdirs
    return mkdirFunction(path)


def merge(paths, dist, mode="move"):
    safeMkdirs(dist)
    mergeFunc = getattr(shutil, mode)
    for path in paths:
        if os.path.isfile(path):
            mergeFunc(path, dist)
        else:
            for p in os.listdir(path):
                subpath = os.path.join(path, p)
                mergeFunc(subpath, dist)
            if mode == "move":
                os.rmdir(path)
    return dist


def md5(filepath, block_size=64 * 1024):
    with open(filepath, "rb") as f:
        _md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            _md5.update(data)
    return base64.b64encode(_md5.digest()).decode()


def empty(folder):
    return [remove(os.path.join(folder, path)) for path in os.listdir(folder)]


def remove(path):
    removeFunction = removeFile if os.path.isfile(path) else removeFolder
    return removeFunction(path)


def removeFile(filePath):
    if os.path.exists(filePath):
        os.remove(filePath)
    return filePath


def removeFolder(folderPath):
    if os.path.exists(folderPath):
        shutil.rmtree(folderPath)
    return folderPath


def removeEmptyFolders(folderPath):
    try:
        os.removedirs(folderPath)
        return folderPath
    except Exception:
        return folderPath


def copy(src, dst):
    copyFunction = copyFile if os.path.isfile(src) else copyFolder
    return copyFunction(src, dst)


def copyFile(src, dst):
    mkdirs(dst, parent=True)
    shutil.copyfile(src, dst)
    return dst


def copyFolder(src, dst):
    remove(dst)
    mkdirs(dst, parent=True)
    shutil.copytree(src, dst)
    return dst
