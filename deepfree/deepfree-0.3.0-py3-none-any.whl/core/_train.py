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
        else:
            self.msg_str = '>>> epoch = {}/{}  | 「Train」: '.format(i+1, self.epoch)
            for key in var_dict.keys():
                if 'accuracy' in key:
                    self.msg_str += key + ' = {:.4}% , '.format(var_dict[key]*100)
                else:
                    self.msg_str += key + ' = {:.4} , '.format(var_dict[key])
            self.msg_str += 'expend time = {:.4}'.format(time_delta)
        
    def test_message_str(self, var_dict):
        self.msg_str += '  | 「Test」: '
        for key in var_dict.keys():
            if 'pred' in key:
                continue
            elif 'accuracy' in key:
                self.msg_str += key + ' = {:.4}% , '.format(var_dict[key]*100)
            else:
                self.msg_str += key + ' = {:.4} , '.format(var_dict[key])
        self.msg_str = self.msg_str[:-3] + '                '
    
    def update_message(self):
        sys.stdout.write('\r'+ self.msg_str)
        sys.stdout.flush()

class Sess(object):
    def init_var(self):
        uninit_vars = []
        for var in tf.global_variables():
            try:
                self.sess.run(var)
            except tf.errors.FailedPreconditionError:
                uninit_vars.append(var)
        self.sess.run(tf.variables_initializer(uninit_vars))
    
    def init_sess(self):
        if self.sess is None:
            self.sess = tf.Session()
        # 初始化变量
        self.sess.run(tf.global_variables_initializer())
        
        if self.saver is None:
            self.saver = Saver(self.save_name,self.sess,self.load_phase,self.save_model)
        if self.tbd is None and self.open_tensorboard:
            self.tbd = Tensorboard(self.save_name,self.sess)
    
    
    def run_sess(self, var_list):
        
        if self.dropout not in self.feed_dict.keys() : self.feed_dict[self.dropout] = 0.0
        if self.batch_normalization not in self.feed_dict.keys() : self.feed_dict[self.batch_normalization] = False

        result_list = self.sess.run(var_list, feed_dict = self.feed_dict)
        return result_list
    
    def end_sess(self):
        if self.open_tensorboard:
            self.tbd.train_writer.close()
        self.sess.close()
        tf.reset_default_graph()

class Train(Loss,Sess,Message):
    
    def training_initialization(self, simple):
        # var_dict
        if self.task == 'classification':
            training_dict = {'loss':0.0, 'accuracy':0.0}
            test_dict = {'accuracy':0.0, 'pred': None}
        else:
            training_dict = {'loss':0.0, 'rmse':0.0, 'R2':0.0}
            test_dict = {'rmse':0.0, 'R2':0.0, 'pred': None}
        
        # 加入用户数据
        if hasattr(self, 'training_dict'):
            training_dict.update(self.training_dict)
        self.training_dict = training_dict
        if hasattr(self, 'test_dict'):
            test_dict.update(self.test_dict)
        self.test_dict = test_dict
        
        # training_list
        self.training_list = list()
        for key in self.training_dict.keys():
            self.training_list.append(eval('self.'+key))
        self.training_list.append(self.batch_training)
            
        # test_list
        if self.do_test:                
            self.test_list = list()
            for key in self.test_dict.keys():
                self.test_list.append(eval('self.'+key))
        
        # simple
        if simple:
            self.do_test = False
            self.save_result = False
            self.plot_result = False
            
        # recording_dict
        if self.save_result or self.plot_result:
            self.recording_dict = {'epoch':list(), 'time':list(), 'loss':list()}
            if self.task == 'classification':
                self.recording_dict.update({'train_accuracy':list(), 'test_accuracy':list()}) 
            else:
                self.recording_dict.update({'train_rmse':list(), 'train_R2':list(),'test_rmse':list(), 'test_R2':list()} )
                

    def training(self, simple = False, **kwargs):
        if self.before_training(**kwargs) == False: return
        
        # load
        if self.saver.load_parameter('f'): return
        # pre_training
        elif hasattr(self, 'is_pre') and self.is_pre: self.pre_training(**kwargs)
        
        print('Start training '+self.name+' ...')
        
        # init recording_dict
        self.training_initialization(simple)
        
        time_start=time.time()
        drop_rate = self.dropout_rate
        batch_times = int(self.train_X.shape[0]/self.batch_size)
        
        Batch_data=Batch(inputs=self.train_X,
                         labels=self.train_Y,
                         batch_size=self.batch_size)
        
        for i in range(self.epoch):
            drop_rate *= self.decay_drop_rate
            for _ in range(batch_times):
                # batch_training
                batch_x, batch_y= Batch_data.next_batch()
                self.feed_dict={self.input: batch_x, 
                                self.label: batch_y, 
                                self.dropout: drop_rate,
                                self.batch_normalization: True}
                # print(self.feed_dict)
                result_list = self.run_sess(self.training_list)
                for j, key in enumerate(self.training_dict.keys()): self.training_dict[key] += result_list[j]
            
            time_end=time.time()
            time_delta = time_end-time_start
            for key in self.training_dict.keys(): self.training_dict[key] /= batch_times
            self.train_message_str(i, time_delta, self.training_dict)
            
            if self.tbd is not None:
                merge = self.run_sess(self.merge)
                self.tbd.train_writer.add_summary(merge, i)   
            
            if self.do_test and self.test_Y is not None:
                # test dataset
                self.feed_dict={self.input: self.test_X,
                                self.label: self.test_Y,
                                self.dropout: 0.0,
                                self.batch_normalization: False}
                
                result_list = self.run_sess(self.test_list)
                for j, key in enumerate(self.test_dict.keys()): self.test_dict[key] = result_list[j]
                self.compare_and_record_the_best(self.test_dict)
                
                self.test_message_str(self.test_dict)
            self.update_message()
            
            # record result
            if self.save_result or self.plot_result:
                self.save_epoch_training_data(i, time_delta)
        print('')
        # saver
        self.saver.save_parameter('f')
        # predicton
        if self.do_test and self.test_X is not None:
            self.feed_dict = {self.input: self.test_X,
                              self.dropout: 0.0,
                              self.batch_normalization: False}
            self.pred_Y = self.run_sess(self.pred)
        # save_result
        if self.save_result:
            self.save_result_to_csv()
        # plot
        if self.plot_result:
            self.plot_epoch_result()
            self.plot_pred_result()

    def pre_training(self,**kwargs):
        if self.saver.load_parameter('p'): return
        
        print('Start pre-training ...')
        pass_dict = PASS_DICT.copy()
        for key in pass_dict.keys(): 
            pass_dict[key] = self.__dict__[key]
        kwargs = dict(pass_dict, **kwargs)
        
        X = self.train_X
        for sub in self.pre_model.sub_list:
            kwargs['train_X'] = X
            # sub_training
            sub.sub_training(**kwargs)
            X = np.array(X, dtype = np.float32)
            self.feed_dict = {sub.input: X}
            X = self.run_sess(sub.transform.output)
        self.pre_model.deep_feature = X
        self.saver.save_parameter('p')
    