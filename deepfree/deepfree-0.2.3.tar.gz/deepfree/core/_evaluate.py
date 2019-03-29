# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np

class Evaluate(object):
    def __init__(self):
        self.best_dict =  {'accuracy':0.0,
                           'rmse':np.inf,
                           'R2':0.0,
                           'FDR':None,
                           'FPR':None,
                           'pred_cnt':None,
                           'pred_cnt_pro': None
                           }    
        self.pred_Y = None
        self.real_Y = None
        self.n_real_sample = None
        self.n_real_sample_i = None
    
    def get_accuracy(self):
        if self.label.shape[1]>1:
            self.output_arg = tf.argmax(self.output,axis=1)
            self.label_arg = tf.argmax(self.label,axis=1)
        else:
            self.output_arg = tf.to_int(tf.ones_like(self.output) < self.output)
            self.label_arg = tf.to_int(tf.ones_like(self.label_arg) < self.label_arg)
        return tf.reduce_mean(tf.cast(tf.equal(self.output_arg,self.label_arg),tf.float32))
    
    def get_rmse(self):
        return tf.sqrt(tf.losses.mean_squared_error(self.label, self.output))
    
    def get_R2(self):
        total_error = tf.reduce_sum(tf.square(tf.sub(self.label, tf.reduce_mean(self.label))))
        unexplained_error = tf.reduce_sum(tf.square(tf.sub(self.label, self.output)))
        R_squared = tf.sub(1, tf.div(unexplained_error, total_error))
        return R_squared
    
    def get_FDR(self,pred):
        '''
            正分率:
            FDR_i = pred_cnt[i][i] / n_real_sample_i[i]
            
            误分率:
            FPR_i = ∑_j pred_cnt[i][j ≠ i] / ∑_j n_real_sample_i[j ≠ i]
        '''
        pred_cnt = np.zeros((self.n_category,self.n_category))
        for i in range(self.n_real_sample):
            # 第 r 号分类 被 分到了 第 p 号分类
            p = self.pred_Y[i]
            r = self.real_Y[i]
            pred_cnt[p][r] += 1
        pred_cnt_pro = pred_cnt / self.n_real_sample_i
        # array是一个1维数组时，形成以array为对角线的对角阵；array是一个2维矩阵时，输出array对角线组成的向量
        FDR = np.diag(pred_cnt_pro)
        FPR = [(self.n_real_sample_i[i]-pred_cnt[i][i])/
               (self.n_real_sample-self.n_real_sample_i[i]) for i in range(self.n_category)]
        
        self.best_dict['pred_cnt'] = pred_cnt
        self.best_dict['pred_cnt_pro'] = pred_cnt_pro
        self.best_dict['FDR'] = FDR
        self.best_dict['FPR'] = FPR
    
    def compare_and_record_the_best(self, var_dict):
        if self.task == 'classification':
            self.statistics_number_in_each_category()
            if var_dict['accuracy'] > self.best_dict['accuracy']:
                self.pred_Y = var_dict['pred']
                self.best_dict['accuracy'] = var_dict['accuracy']
                self.get_FDR(self.pred_Y)
                
        else:
            if var_dict['rmse'] < self.best_dict['rmse']:
                self.pred_Y = var_dict['pred']
                self.best_dict['rmse'] = var_dict['rmse']
                self.best_dict['R2'] = var_dict['R2']
    
    def save_epoch_training_data(self, i, time_delta):
        self.recording_dict['epoch'].append(i+1)
        self.recording_dict['time'].append(time_delta)
        self.recording_dict['loss'].append(self.train_dict['loss'])
        for key in self.train_dict.keys(): 
            if 'train_'+key in self.recording_dict.keys(): 
                self.recording_dict['train_'+key].append(self.train_dict[key])
        for key in self.test_dict.keys(): 
            if 'test_'+key in self.recording_dict.keys(): 
                self.recording_dict['test_'+key].append(self.test_dict[key])
    
    def statistics_number_for_in_category(self):
        if self.real_Y is None: 
            self.real_Y = np.argmax(self.test_Y,axis = 1)
        if self.n_real_sample is None:
            # 第 i 类样本总数, 样本总数
            self.n_real_sample_i = np.sum(self.test_Y,axis = 0,dtype = np.int)
            self.n_real_sample = np.sum(self.n_real_sample_i,dtype = np.int)
        if self.n_category is None:
            self.n_category = self.test_Y.shape[1]
            