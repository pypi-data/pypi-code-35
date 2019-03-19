#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
from ctypes import *

import numpy as np

# dllFilePath = os.path.join(os.path.dirname(__file__), "NNLS.dll")
# dll = cdll.LoadLibrary(dllFilePath)
# dll = cdll.LoadLibrary(r"F:\Beta\FACEGOOD_Retargeter.dll")

# path = "../facegood/FACEGOOD_Retargeter.dll"
path = "FACEGOOD_Retargeter.dll"

dll = cdll.LoadLibrary(path)

# mayaExePath = str(sys.argv[0])
# mayaPath = os.path.split(mayaExePath)[0]
# dllFilePath = os.path.join(mayaPath,"../Python/Lib/site-packages/facegood/FACEGOOD_Retargeter.dll")
# dll = cdll.LoadLibrary(dllFilePath)

def FgFilter(data, frameRate=25, cutoffFrequency=5, filterOrder=3):
    dataLen = len(data)
    oldData = (c_double * dataLen)()
    for i in xrange(0, dataLen):
        oldData[i] = float(data[i])
    outT = (c_double * dataLen)()
    dll.FgFilterRetargeter(
        c_double(frameRate),
        c_double(cutoffFrequency), c_ulonglong(filterOrder),
        c_double(float(data[0])), pointer(oldData), dataLen, pointer(outT))
    return outT


def FgKalmanFilter(data, filterCoefficient=0.85):
    dataLen = len(data)
    oldData = (c_double * dataLen)()
    for i in xrange(0, dataLen):
        oldData[i] = float(data[i])
    outT = (c_double * dataLen)()
    dll.FgKalmanFilter(
        c_double(filterCoefficient), dataLen, pointer(oldData), pointer(outT))
    return outT


def fg_filter(read_file_path,
              save_file_path,
              frameRate=25,
              cutoffFrequency=5,
              filterOrder=3):
    vertexs = np.load(read_file_path)
    total_frame = len(vertexs)
    total_vertexs = len(vertexs[0])
    vertexs_out = np.ndarray(
        shape=(total_frame, total_vertexs, 3), dtype=float)
    for vertex_num in xrange(0, total_vertexs):
        for axis in xrange(0, 3):
            vertex_axis = [
                vertexs[frame][vertex_num][axis]
                for frame in xrange(0, total_frame)
            ]
            history = FgFileter(
                vertex_axis,
                frameRate=frameRate,
                cutoffFrequency=cutoffFrequency,
                filterOrder=filterOrder)
            for frame in xrange(0, total_frame):
                vertexs_out[frame][vertex_num][axis] = history[frame]

    np.save(save_file_path, vertexs_out)


def kalman_filter(read_file_path, save_file_path, filterCoefficient=0.85):
    vertexs = np.load(read_file_path)
    total_frame = len(vertexs)
    total_vertexs = len(vertexs[0])
    vertexs_out = np.ndarray(
        shape=(total_frame, total_vertexs, 3), dtype=float)
    for vertex_num in xrange(0, total_vertexs):
        for axis in xrange(0, 3):
            vertex_axis = [
                vertexs[frame][vertex_num][axis]
                for frame in xrange(0, total_frame)
            ]
            history = FgKalmanFilter(
                vertex_axis, filterCoefficient=filterCoefficient)
            for frame in xrange(0, total_frame):
                vertexs_out[frame][vertex_num][axis] = history[frame]

    np.save(save_file_path, vertexs_out)
