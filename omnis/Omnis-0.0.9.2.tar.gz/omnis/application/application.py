from keras.models import load_model
from tensorflow.python.client import device_lib

import numpy
import cv2

import os


class Application(object):
    
    def __init__(self):
        self.gpu_num = self._count_available_gpu()


    def _count_available_gpu(self):
        local_device_protos = device_lib.list_local_devices()
        return len([x.name for x in local_device_protos if x.device_type == 'GPU'])

    def _use_specific_gpus(self, gpuids):
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = gpuids
        self.gpu_num = len(gpuids)
        
