# -*- coding: utf-8 -*-
import time
import tensorflow as tf
import numpy as np
import sys
from deepfree.base._data import Batch
from deepfree.core._loss import Loss
from deepfree.base._attribute import PASS_DICT
from deepfree.base._saver import Saver, Tensorboard

class Message(object):
    def train_message_str(self, i, time_delta, var_dict):
        if hasattr(self, 'is_sub') and self.is_sub:
            self.msg_str = '>>> epoch = {}/{}  | 「Train」: loss = {:.4} , expend time = {:.4}'.format(
                    i+1, self.pre_epoch, var_dict['loss'], time_delta)
        elif self.task == 'classification':
            self.msg_str = '>>> epoch = {}/{}  | 「Train」: loss = {:.4} , accuracy = {:.4}% , expend time = {:.4}'.format(
                    i+1, self.epoch, var_dict['loss'], var_dict['accuracy']*100, time_delta)
        else:
            self.msg_str = '>>> epoch = {}/{}  | 「Train」: loss = {:.4} , rmse = {:.4} , R2 = {:.4} , expend time = {:.4}'.format(
                    i+1, self.epoch, var_dict['loss'], var_dict['rmse'], var_dict['R2'], time_delta)
        
    def test_message_str(self, var_dict):
        if self.task == 'classification':
            self.msg_str += '  | 「Test」: accuracy = {:.4}%           '.format(
                    var_dict['accuracy']*100)
        else:  
            self.msg_str += '  | 「Test」: rmse = {:.4} , R2 = {:.4}           '.format(
                    var_dict['rmse'], var_dict['R2'])
    
    def update_message(self):
        sys.stdout.write('\r'+ self.msg_str)
        sys.stdout.flush()

class Sess(object):
    def start_sess(self):
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer()) # 初始化变量
        
        self.saver = Saver(self.save_name,self.sess,self.load_phase,self.save_model)
        if self.open_tensorboard:
            self.tbd = Tensorboard(self.save_name,self.sess)
    
    def run_sess(self, var_list, feed_dict):
        if self.dropout not in feed_dict.keys() : feed_dict[self.dropout] = 0.0
        if self.batch_normalization not in feed_dict.keys() : feed_dict[self.batch_normalization] = False

        result_list = self.sess.run(var_list, feed_dict = feed_dict)
        return result_list
    
    def end_sess(self):
        if self.open_tensorboard:
            self.tbd.train_writer.close()
        self.sess.close()

class Train(Loss,Sess,Message):
    def __init__(self):
        self.recording_dict = {'epoch':list(), 'time':list(), 'loss':list()}
        if self.task == 'classification':
            self.recording_dict.update({'train_accuracy':list(), 'test_accuracy':list()}) 
        else:
            self.recording_dict.update({'train_rmse':list(), 'train_R2':list(),'test_rmse':list(), 'test_R2':list()} )
    
    def training(self,**kwargs):
        if self.before_training(**kwargs) == False: return
        
        # load
        if self.saver.load_parameter('f'): return
        # pre_training
        elif hasattr(self, 'is_pre') and self.is_pre: self.pre_training(**kwargs)
        
        print('Start training '+self.name+' ...')
        time_start=time.time()
        drop_rate = self.dropout_rate
        batch_times = int(self.train_X.shape[0]/self.batch_size)
        
        Batch_data=Batch(inputs=self.train_X,
                         labels=self.train_Y,
                         batch_size=self.batch_size)
        
        for i in range(self.epoch):
            drop_rate *= self.decay_drop_rate
            
            if self.task == 'classification': 
                train_dict = {'loss':0.0, 'accuracy':0.0}
                train_list = [self.accuracy, self.loss, self.batch_training]
            else: 
                train_dict = {'loss':0.0, 'rmse':0.0, 'R2':0.0}
                train_list = [self.R2, self.rmse, self.loss, self.batch_training]
            for _ in range(batch_times):
                
                # batch_training
                batch_x, batch_y= Batch_data.next_batch()
                feed_dict={self.input: batch_x, 
                           self.label: batch_y, 
                           self.dropout: drop_rate,
                           self.batch_normalization: True}
                result_list = self.run_sess(train_list, feed_dict)
                for j, key in enumerate(train_dict.keys()): train_dict[key] += result_list[j]
            
            time_end=time.time()
            time_delta = time_end-time_start
            for key in train_dict.keys(): train_dict[key] /= batch_times
            self.train_message_str(i, time_delta, train_dict)
            
            if self.tbd is not None:
                merge = self.run_sess(self.merge, feed_dict)
                self.tdb.train_writer.add_summary(merge, i)   
            
            if self.test_Y is not None:
                # test dataset
                if self.task == 'classification': 
                    test_dict = {'accuracy':0.0, 'pred': None}
                    test_list = [self.pred, self.accuracy]
                else: 
                    test_dict = {'rmse':0.0, 'R2':0.0, 'pred': None}
                    test_list = [self.pred, self.R2, self.rmse]
                    
                feed_dict={self.input: self.test_X,
                           self.label: self.test_Y,
                           self.dropout: 0.0,
                           self.batch_normalization: False}
                
                result_list = self.run_sess(test_list, feed_dict)
                for j, key in enumerate(test_dict.keys()): test_dict[key] = result_list[j]
                self.record_best(test_dict)
                
                self.test_message_str(test_dict)
            self.update_message()
            
            # record result
            self.recording_dict['epoch'].append(i+1)
            self.recording_dict['time'].append(time_delta)
            self.recording_dict['loss'].append(train_dict['loss'])
            for key in train_dict.keys(): 
                if 'train_'+key in self.recording_dict.keys(): 
                    self.recording_dict['train_'+key].append(train_dict[key])
            for key in test_dict.keys(): 
                if 'test_'+key in self.recording_dict.keys(): 
                    self.recording_dict['test_'+key].append(test_dict[key])
        print('')
        # saver
        self.saver.save_parameter('f')
        # predicton
        if self.test_Y is None:
            feed_dict = {self.input: self.test_X,
                         self.dropout: 0.0,
                         self.batch_normalization: False}
            self.pred_Y = self.run_sess(self.pred, feed_dict)
        # save_result
        self.save_result()
        # plot
        self.plot_epoch_result()
        self.plot_pred_result()

    def pre_training(self,**kwargs):
        if self.saver.load_parameter('p'): return
        
        print('Start pre-training ...')
        pass_dict = PASS_DICT.copy()
        for key in pass_dict.keys(): 
            pass_dict[key] = self.__dict__[key]
        kwargs = dict(pass_dict, **kwargs)
        kwargs['is_sub'] = True
        
        X = self.train_X
        for sub in self.pre_model.sub_list:
            kwargs['train_X'] = X
            # sub_training
            sub.sub_training(**kwargs)
            X = np.array(X, dtype = np.float32)
            X = self.run_sess(sub.transform.output, feed_dict = {sub.input: X})
        self.pre_model.deep_feature = X
        self.saver.save_parameter('p')
            
    def sub_training(self,**kwargs):
        if self.before_training(**kwargs) == False: return
        
        print('Training '+ self.name+' ...')
        time_start=time.time()
        batch_times = int(self.train_X.shape[0]/self.batch_size)
        
        if self.label is None: labels = None
        else: labels = self.train_Y
        Batch_data=Batch(inputs=self.train_X,
                         labels=labels,
                         batch_size=self.batch_size)
        
        for i in range(self.pre_epoch):
            sum_loss=0.0
            for j in range(batch_times):
                # 有监督
                batch_x,batch_y = Batch_data.next_batch()
                feed_dict={self.input: batch_x}
                if self.recon is not None: feed_dict[self.recon]= batch_x
                if self.label is not None: feed_dict[self.label]= batch_y
                
                loss,_ = self.run_sess([self.loss,self.batch_training], feed_dict)
                sum_loss = sum_loss + loss
                
            loss = sum_loss/batch_times
            time_end=time.time()
            time_delta = time_end-time_start
            
            if self.tbd is not None:
                merge = self.run_sess(self.merge, feed_dict)
                self.tdb.train_writer.add_summary(merge, i)
            
            self.train_message_str(i, time_delta, {'loss':loss})
            self.update_message()
        print('')
