from keras.callbacks import Callback
import json
from collections import OrderedDict
import sys


class Callback_Image_Classification(Callback):
    def __init__(self, total_step, total_epoch):
        self.step = 0
        self.epoch = 0
        self.total_step = total_step
        self.total_epoch = total_epoch

    def on_batch_end(self, batch, logs={}):
        self.step += 1
        logJson = OrderedDict()
        logJson['logType'] = "batchend"
        logJson['totalStep'] = self.total_step
        logJson['nowStep'] = self.step
        logJson['totalEpoch'] = self.total_epoch
        logJson['nowEpoch'] = self.epoch
        logJson['loss'] = str(logs.get('loss'))
        logJson['acc'] = str(logs.get('acc'))
        sys.stderr.write(json.dumps(logJson, ensure_ascii=False, indent="\t"))
        return
    
    def on_epoch_end(self, epoch, logs={}):
        self.epoch += 1
        self.step = 0
        logJson = OrderedDict()
        logJson['logType'] = "epochend"
        logJson['totalEpoch'] = self.total_epoch
        logJson['nowEpoch'] = self.epoch
        logJson['loss'] = str(logs.get('loss'))
        logJson['acc'] = str(logs.get('acc'))
        sys.stderr.write(json.dumps(logJson, ensure_ascii=False, indent="\t"))
        return