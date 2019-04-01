# -*- coding: utf-8 -*-
import time
import tensorflow as tf
from deepfree.base._data import Batch
from deepfree.core._train import Sess,Message
from deepfree.core._loss import Loss

_opt = {'sgd':'GradientDescentOptimizer',
        'adag':'AdagradOptimizer',
        'adam':'AdamOptimizer',
        'mmt':'MomentumOptimizer',
        'rmsp':'RMSPropOptimizer'}

class SubModel(Loss,Sess,Message):
    def __init__(self,**kwargs):
        ''' 
            对于未设置的属性值采用默认值:
            可设置的模型参数列表见 _attribute.py 中的 _hypp 
        '''
        for key in kwargs.keys(): setattr(self, key, kwargs[key])
        
        # build_model
        if hasattr(self, 'build_model'):
            with tf.name_scope(self.name):
                for key in self.show_dict.keys(): self.show_dict[key] = self.__dict__[key]
                print('Building '+self.name + ' ...')
                print(self.show_dict)
                self.build_model()
    
    def get_merge(self):
        self.tbd.scalars_histogram('weight',self.weight)
        self.tbd.scalars_histogram('bias_x',self.bias_x)
        self.tbd.scalars_histogram('bias_h',self.bias_h)
        
        if self.loss is not None:
            tf.summary.scalar('loss', self.loss)
        self.merge = tf.summary.merge(tf.get_collection(tf.GraphKeys.SUMMARIES,self.name))
    
    def before_training(self,**kwargs):
        for key in kwargs.keys(): setattr(self, key, kwargs[key])
        
        if self.batch_training is None:
            # loss
            if self.loss is None:
                if self.logits is None:
                    self.loss = self.get_loss(self.label, output = self.output, loss_func = 'mse')
                else:
                    self.loss = self.get_loss(self.label, logits = self.logits)
            
            # dc_lr
            lr = self.pre_lr
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
        
        # merge
        if self.tbd is not None:  
            self.get_merge()
    
    def sub_training(self,**kwargs):
        if self.before_training(**kwargs) == False: return
        
        print('Training '+ self.name+' ...')
        time_start=time.time()
        batch_times = int(self.train_X.shape[0]/self.batch_size)
        
        if hasattr(self, 'label') == False: labels = None
        else: labels = self.train_Y
        Batch_data=Batch(inputs=self.train_X,
                         labels=labels,
                         batch_size=self.batch_size)
        
        for i in range(self.pre_epoch):
            sum_loss=0.0
            for j in range(batch_times):
                # 有监督
                batch_x,batch_y = Batch_data.next_batch()
                self.feed_dict={self.input: batch_x}
                if self.recon is not None: self.feed_dict[self.recon]= batch_x
                if hasattr(self, 'label'): self.feed_dict[self.label]= batch_y
                
                loss,_ = self.run_sess([self.loss,self.batch_training])
                sum_loss = sum_loss + loss
                
            loss = sum_loss/batch_times
            time_end=time.time()
            time_delta = time_end-time_start
            
            if self.tbd is not None:
                merge = self.run_sess(self.merge)
                self.tdb.train_writer.add_summary(merge, i)
            
            self.train_message_str(i, time_delta, {'loss':loss})
            self.update_message()
        print('')