# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
from deepfree.core._layer import phvariable
from deepfree.base._attribute import DATA_DICT, SHOW_DICT, MODEL_DICT
from deepfree.base._data import Data
from deepfree.core._train import Train
from deepfree.core._evaluate import Evaluate
from deepfree.base._result import Result


_opt = {'sgd':'GradientDescentOptimizer',
        'adag':'AdagradOptimizer',
        'adam':'AdamOptimizer',
        'mmt':'MomentumOptimizer',
        'rmsp':'RMSPropOptimizer'}

class Model(Train,Evaluate,Result):
    def __init__(self,**kwargs):
        ''' 
            对于未设置的属性值采用默认值:
            可设置的模型参数列表见 _attribute.py 中的 _hypp 
        '''
        kwargs = dict(MODEL_DICT,**kwargs)
        for key in kwargs.keys(): setattr(self, key, kwargs[key])
        if self.save_name is None: self.save_name = self.name        
        
        # 创建唯一变量
        self.dropout = phvariable(1,'dropout',unique = True)()
        self.batch_normalization = phvariable(1,'batch_normalization',dtype = tf.bool,unique = True)
        
        # 基（父）类初始化
        Evaluate.__init__(self)
        
        # build_model
        if hasattr(self, 'build_model'):
            if self.n_category is None: self.n_category = self.struct[-1]
            with tf.name_scope(self.name):
                if hasattr(self, 'show_dict') == False:
                    self.show_dict = SHOW_DICT.copy()
                for key in self.show_dict.keys(): self.show_dict[key] = self.__dict__[key]
                print('Building '+self.name + ' ...')
                print(self.show_dict)
                self.build_model()
    
    def add_layer(self,layer,x = None):
        '''x为空时，调用此函数需前先设置 Model.input'''
        # 确定x
        if x is None:
            if len(self.layer_list) > 0:
                x = self.layer_list[-1].output
            elif self.input is not None:
                x = self.input
            else: 
                return
        
        # 构建层
        if type(layer) == list:
            for l in layer:
                x = l(x)
                self.layer_list.append(l)
        else:
            layer(x)
            self.layer_list.append(layer)
            
    
    def next_hidden_activation(self):
        if type(self.hidden_func) == list:
            activation = self.hidden_func[self.hidden_activation_loc]
            self.hidden_activation_loc = np.mod(self.hidden_activation_loc + 1, len(self.hidden_func))
            return activation
        else:
            return self.hidden_func
    
    def load_data(self):
        if self.train_X is not None: 
            return True
        else:
            data_dict = DATA_DICT.copy()
            for key in data_dict.keys(): 
                data_dict[key] = self.__dict__[key]
            self.datasets,self.scaler_y = Data(**data_dict).load_data()
            if self.datasets is not None:
                self.train_X, self.train_Y, self.test_X, self.test_Y = self.datasets
                return True
        return False
    
    def get_merge(self):
        if self.is_sub:
            self.tbd.scalars_histogram('weight',self.weight)
            self.tbd.scalars_histogram('bias_x',self.bias_x)
            self.tbd.scalars_histogram('bias_h',self.bias_h)
        else:
            v_list = tf.global_variables()
            for v in v_list:
                if 'weight' in v.name or 'bias' in v.name:
                    name = np.split(v.name,'/')[-1]
                    self.tbd.scalars_histogram(name,v)
        for index in ['loss','accuracy','rmse','R2']:
            if eval('self.'+index) is not None:
                tf.summary.scalar(index, eval('self.'+index))
        self.merge = tf.summary.merge(tf.get_collection(tf.GraphKeys.SUMMARIES,self.name))
    
    def before_training(self,**kwargs):
        for key in kwargs.keys(): setattr(self, key, kwargs[key])
        
        if self.input is None:
            # input
            print("Please set Model.input before calling Model.add_layer()!"); return False
        
        if self.is_sub == False:
            if self.output is None:
                # output
                self.deep_feature = self.layer_list[-2].output
                self.logits = self.layer_list[-1].add_in
                self.output = self.layer_list[-1].output
            
            if self.task == 'classification':
                # accuracy
                if self.accuracy is None:
                    self.accuracy = self.get_accuracy()
                # pred
                if self.pred is None:
                    self.pred = self.output_arg
            else:
                # rmse
                if self.rmse is None:
                    self.rmse = self.get_rmse()
                # R2
                if self.accuracy is None:
                    self.R2 = self.get_R2()
                # pred
                if self.pred is None:
                    self.pred = self.output
        
        if self.batch_training is None:
            # loss
            if self.loss is None:
                if self.logits is None:
                    self.loss = self.get_loss(self.label, output = self.output, loss_func = 'mse')
                else:
                    self.loss = self.get_loss(self.label, logits = self.logits)
            
            # dc_lr
            if self.is_sub: lr = self.pre_lr
            else: lr = self.lr
            if self.opt == 'adam' or self.opt == 'rmsp': 
                self.global_step =  None
                dc_lr = lr
            else: 
                self.global_step =  tf.Variable(0, trainable=False) # minimize 中会对 global_step 自加 1
                # dc_lr = lr * decay_rate ^ (global_step / decay_steps)
                dc_lr = tf.train.exponential_decay(learning_rate=lr, 
                                                   global_step=self.global_step, 
                                                   decay_steps=100, 
                                                   decay_rate=0.96, 
                                                   staircase=True)
            # batch_training
            trainer = eval('tf.train.' + _opt[self.opt])
            self.batch_training = trainer(learning_rate=dc_lr).minimize(self.loss,global_step=self.global_step)
        
        #sess
        if self.sess is None:  
            self.start_sess()
        
        # merge
        if self.tbd is not None:  
            self.get_merge()
        
        # data
        if self.load_data() == False:
            print("Please load dataset success first!"); return False
        return True
