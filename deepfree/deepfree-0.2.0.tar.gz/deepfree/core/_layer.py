# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np

dropout = None
batch_normalization = None

#######################
#      激活函数
#######################

class Activation(object):    
    def get(name):
        func = getattr(Activation, name, None)
        if func is not None:
            return func
        else:
            return getattr(tf.nn, name, None)
    
    '''在这里自定义激活函数'''
    def gaussain(z):
        return 1-tf.exp(-tf.square(z)) 
    def linear(z):
        return z*tf.constant(1.0)

#######################
#      不带参 Layer
#######################

class PHVariable(object):
    def __init__(self,
                 inpuit_dim,
                 dtype = tf.float32,
                 unique = False):
        self.inpuit_dim = inpuit_dim
        self.dtype = dtype
        self.unique = unique
    def __call__(self,var_name):
        global dropout, batch_normalization
        if self.unique:
            if var_name == 'dropout':
                if dropout is None: dropout = tf.placeholder(self.dtype, name= var_name)
                return dropout
            elif var_name == 'batch_normalization':
                if batch_normalization is None: batch_normalization = tf.placeholder(self.dtype, name= var_name)
                return batch_normalization
        elif var_name in ['input','label']:
            # input
            return tf.placeholder(self.dtype, [None, self.inpuit_dim],name=var_name)
        elif var_name == 'img':
            # img_dim = [长 宽 张]
            full_size = self.inpuit_dim[0]*self.inpuit_dim[1]*self.inpuit_dim[2]
            vector = tf.placeholder(self.dtype, [None, full_size])
            return tf.reshape(vector, shape=[-1, self.inpuit_dim[0], self.inpuit_dim[1], self.inpuit_dim[2]], name=var_name)
        else:
            return tf.placeholder(self.dtype, self.inpuit_dim, name= var_name)

class MaxPooling2D(object):
    def __init__(self,
                 pool_size,
                 strides=(1, 1),
                 padding='VALID'):
        self.pool_size = pool_size
        self.strides = strides
        self.padding = padding
    
    def __call__(self, inputs):
        pool_size = list(np.concatenate(([1],self.pool_size,[1]),axis=0))
        strides = list(np.concatenate(([1],self.strides,[1]),axis=0))
        return tf.nn.max_pool(inputs, ksize = pool_size, strides = strides, padding = self.padding)

class Flatten(object):    
    def __call__(self, inputs):
        return tf.layers.flatten(inputs)
    
class Concatenate(object):
    def __call__(self, inputs):
        return tf.concat(inputs,axis=-1)

#######################
#      带参 Layer
#######################
        
class Layer(object):
    def __init__(self,
                 weight = None,
                 bias = None,
                 activation = 'linear',
                 trainable = True,
                 is_dropout = False,
                 is_bn = False):
        self.weight = weight
        self.bias = bias
        self.activation = Activation.get(activation)
        self.trainable = trainable
        self.is_dropout = is_dropout
        self.is_bn = is_bn
        
    def __call__(self, inputs):
        if hasattr(self, 'output') == False: 
            self.build_layer(inputs)
        return self.output
        
    def build_layer(self, inputs):
        if type(inputs) == list:
            # MultipleInput
            self.input_dim = 0
            for x in inputs:
                self.input_dim += x.shape.as_list()[1]
        else:
            # Dense, Conv2D
            self.input_dim = inputs.shape.as_list()[1]
            # dropout
            if self.is_dropout:
                inputs = tf.nn.dropout(inputs, 1 - dropout)
        
        # weight
        if self.weight is None:
            if self.name =='Dense' or self.name =='MultipleInput':
                glorot_normal = np.sqrt(2 / (self.input_dim + self.output_dim))
                self.weight = tf.Variable(tf.truncated_normal(
                                          shape=[self.input_dim, self.output_dim], 
                                          stddev = glorot_normal), 
                                          trainable = self.trainable,
                                          name='weight')
            elif self.name =='Conv2D':
                self.input_dim = inputs.shape.as_list()[1:]
                img_size = self.input_dim[0]* self.input_dim[1]
                glorot_uniform = np.sqrt(6 / (img_size* self.input_dim[-1] + img_size* self.output_dim))
                self.weight = tf.Variable(tf.random_uniform(
                                          shape=[self.kernel_size[0], self.kernel_size[1],self.input_dim[-1],self.output_dim], 
                                          minval=glorot_uniform*-1,
                                          maxval=glorot_uniform),
                                          trainable = self.trainable,
                                          name='weight')
            

        # add_in
        self.add_in = self.get_add_in(inputs)
        
        if self.is_bn:
            # batch_normalization
            self.add_in = tf.layers.batch_normalization(self.add_in, training = batch_normalization)
        elif self.bias is None:
            # bias
            self.bias = tf.Variable(tf.constant(0.0, 
                                    shape=[self.output_dim]),
                                    trainable = self.trainable,
                                    name='bias')
            self.add_in += self.bias
        
        # output
        self.output = self.activation(self.add_in)
    

class Dense(Layer):
    def __init__(self, 
                 output_dim, 
                 **kwargs):
        self.output_dim = output_dim
        self.name = 'Dense'
        super(Dense, self).__init__(**kwargs)
    
    def get_add_in(self, inputs):
        return tf.matmul(inputs, self.weight)
   
class MultipleInput(Layer):
    def __init__(self, 
                 output_dim, 
                 **kwargs):
        self.output_dim = output_dim
        self.name = 'MultipleInput'
        super(MultipleInput, self).__init__(**kwargs)
    
    def get_add_in(self, inputs):
        add_in = 0
        # pointer
        start = 0
        end = 0
        for x in inputs:
            end += x.shape.as_list()[1]
            # dropout
            if self.dropout is not None:
                x = tf.nn.dropout(x, 1 - self.dropout)
            add_in += tf.matmul(x, self.weight[start:end,:])
            start = end
        
        return add_in
    
class Conv2D(Layer):
    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='VALID',
                 batch_normalization=True,
                 **kwargs):
        self.output_dim = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.batch_normalization = batch_normalization
        self.name = 'Conv2D'
        super(Conv2D, self).__init__(**kwargs)
    
    def get_add_in(self, inputs):
        strides = list(np.concatenate(([1],self.strides,[1]),axis=0))
        add_in = tf.nn.conv2d(inputs, self.weight, strides=strides, padding=self.padding)
        return add_in

#def example():
#    # 多输入多输出
#    x1 = PHVariable(5)('input')
#    x2 = PHVariable(5)('input')
#    x = Concatenate(2,activation = 'sigmoid')([x1,x2])
#    y1 = Dense(1,activation = 'sigmoid')(x)
#    y2 = Dense(2,activation = 'sigmoid')(x)
#    
#    # 权值共享
#    v = PHVariable(7)('input')
#    d = PHVariable(1)('const')
#    H = Dense(4, activation = 'sigmoid')
#    h = H(v)
#    v2 = Dense(7, weight=tf.transpose(H.weight), activation = 'sigmoid')(h)
#    
#    # 图像处理
#    img = PHVariable((28,28,3))('img')
#    x = Conv2D(2,(3,3),activation = 'sigmoid')(img)
#    x = Conv2D(2,(2,2),activation = 'sigmoid')(x)