from keras.models import load_model

import numpy
import cv2

import os


class Application(object):
    
    def __init__(self):
        print("init application")
        # default setting for using 1gpu and gpu_ids for 0
        self.gpu_num = 1
        self.gpu_ids = [0]

    def use_specific_gpus(self, gpuids):
        self.gpu_ids = gpuids
        self.gpu_num = len(gpuids)
        
