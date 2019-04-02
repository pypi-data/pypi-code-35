# -*- coding: utf-8 -*-
import os
import random
import numpy as np
from deepfree.base._attribute import DATA_DICT

data_list = ['train_X','train_Y','test_X','test_Y']

class Data(object):
    def __init__(self, **kwargs):
        kwargs = dict(DATA_DICT,**kwargs)
        for key in kwargs.keys():
            if key in DATA_DICT.keys():
                setattr(self, key, kwargs[key])

    def load_data(self,**kwargs):
        for key in kwargs.keys():
            if hasattr(self, key): setattr(self, key, kwargs[key])
            
        # datasets
        if self.datasets is not None:
            for j in range(len(self.datasets)):
                exec('self.'+ data_list[j] + '= self.datasets[j]')
        
        # path
        elif self.data_path is not None:
            file_list = os.listdir(self.data_path)  #列出文件夹下所有的目录与文件
            for i in range(len(file_list)):
                file = os.path.join(self.data_path,file_list[i])
                if os.path.isfile(file):
                    for j in range(len(data_list)):
                        if data_list[j] in file:
                            exec("self."+ data_list[j] + "= np.loadtxt(file, dtype = np.float32, delimiter=',')")
                        
        if self.train_X is None:
            print("Failed to load data! Please set the datasets name as 'train_X','train_Y','test_X','test_Y'")
            return None,None
        
        # shuffle,divide
        if self.test_X is None:
            if self.split_rate > 0:
                self.divide_data(rate = self.split_rate, shuffle = self.shuffle)
        
        # process X
        if self.prep_x is not '':
            self.train_X, self.test_X,_ = self.skl_preprocessing(train_data = self.train_X, test_data = self.test_X, prep = self.prep_x)
        
        # process Y
        if self.prep_y:
            if self.task == 'classification':
                # y 不是 one hot 标签
                if len(self.train_Y.shape) == 1:
                    self.n_category = np.max(self.train_Y)
                    if self.test_Y is not None:
                        self.n_category = np.maximum(self.n_category,np.max(self.test_Y))
                    if self.n_category > 1:
                        self.train_Y = self.to_one_hot(self.train_Y, self.n_category)
                        self.test_Y = self.to_one_hot(self.test_Y, self.n_category)
            else:
                # y 不在 [0,1] 之间
                max_y = np.max(self.train_Y); min_y = np.min(self.train_Y)
                if max_y > 1 or min_y < 0:
                    self.train_Y, self.test_Y, self.scaler_y = self.skl_preprocessing(train_data = self.train_Y, test_data = self.test_Y, prep = 'mm')
        
        self.datasets = [self.train_X, self.train_Y, self.test_X, self.test_Y]
        return self.datasets, self.scaler_y
        
    def to_one_hot(self,label,n_category):
        if label is not None:
            return np.eye(n_category)[label]
    
    def divide_data(self,rate = 0.7, shuffle = True):
        if shuffle:
            oder = np.array(range(self.train_X.shape[0]))
            random.shuffle(oder)                                # 随机打乱
            tup_list=list(zip(oder,self.train_X,self.train_Y))  # zip：将对象中对应的元素打包成一个个元组, 返回 tuple list
            tup_list.sort(key=lambda dic_zip: dic_zip[0])
            _, train_X, train_Y=map(list,zip(*tup_list))        # zip(* ) 将元组解压，返回 tuple list
                                                                # map() 根据提供的函数对每个 tuple 做映射
            self.train_X=np.asarray(train_X,dtype='float32')
            self.train_Y=np.asarray(train_Y,dtype='float32')
      
        split = int(self.train_X.shape[0]*rate)
        self.train_X, self.test_X = self.train_X[:split], self.train_X[split:]
        self.train_Y, self.test_Y = self.train_Y[:split], self.train_Y[split:]
        
        if shuffle:
            oder = oder[split:]
            test_X = list()
            test_Y = list()
            for index in oder:
                for tup in tup_list:
                    if index == tup[0]:
                        test_X.append(tup[1].reshape((1,-1)))
                        test_Y.append(tup[2].reshape((1,-1)))
            self.test_X = np.concatenate(test_X,axis = 0)
            self.test_Y = np.concatenate(test_Y,axis = 0)

    def skl_preprocessing(self, train_data = None, test_data = None, prep = 'st'):
        from sklearn.preprocessing import MinMaxScaler,StandardScaler
        # 对于 1 维向量需扩至 2 维
        if len(train_data.shape) == 1: train_data.reshape(-1,1)
        if len(test_data.shape) == 1: test_data.reshape(-1,1)
        if prep == 'st': # Standardization（标准化）
            scaler = StandardScaler()
        if prep == 'mm': # MinMaxScaler (归一化)
            scaler = MinMaxScaler() 
        train_data = scaler.fit_transform(train_data)
        if test_data is not None:
            test_data = scaler.transform(test_data)
        return train_data, test_data, scaler

class Batch(object):
    def __init__(self,
                 inputs=None,
                 labels=None,
                 batch_size=None,
                 shuffle=True):
        self.inputs = inputs
        if labels is None:
            self.exit_y = False
        else:
            self.exit_y = True
            self.labels = labels
        self.batch_size = batch_size
        self.shuffle = shuffle
        
        self._num_examples = inputs.shape[0]
        self._epochs_completed = 0 # 记录loop整个数据集多少次
        self._index_in_epoch = 0 # 记录当前loop的index位置
    
    def process_data_imbalance(self):
        # 统计 train 中各类样本个数 ——> 样本不平衡
        return
    
    def next_batch(self):
        """Return the next `batch_size` examples from this data set."""
        start = self._index_in_epoch
        # Shuffle for the first epoch
        if self._epochs_completed == 0 and start == 0 and self.shuffle: # 第一次的洗牌
            perm0 = np.arange(self._num_examples)
            np.random.shuffle(perm0)
            self._inputs = self.inputs[perm0]
            if self.exit_y: self._labels = self.labels[perm0]
        # Go to the next epoch
        if start + self.batch_size > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Get the rest examples in this epoch
            rest_num_examples = self._num_examples - start
            inputs_rest_part = self._inputs[start:self._num_examples]
            if self.exit_y: labels_rest_part = self._labels[start:self._num_examples]
            # Shuffle the data
            if self.shuffle:  # loop到最后洗牌
                perm = np.arange(self._num_examples)
                np.random.shuffle(perm)
                self._inputs = self.inputs[perm]
                if self.exit_y: self._labels = self.labels[perm]
            # Start next epoch
            start = 0
            self._index_in_epoch = self.batch_size - rest_num_examples
            end = self._index_in_epoch
            inputs_new_part = self._inputs[start:end]
            if self.exit_y:
                labels_new_part = self._labels[start:end]
                return np.concatenate((inputs_rest_part, inputs_new_part), axis=0), np.concatenate((labels_rest_part, labels_new_part), axis=0)
            else:
                return np.concatenate((inputs_rest_part, inputs_new_part), axis=0), None
        else:
            self._index_in_epoch += self.batch_size
            end = self._index_in_epoch
            if self.exit_y:
                return self._inputs[start:end], self._labels[start:end]
            else:
                return self._inputs[start:end], None