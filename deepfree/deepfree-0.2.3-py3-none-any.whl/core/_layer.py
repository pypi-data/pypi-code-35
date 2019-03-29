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

def phvariable(inpuit_dim,
               var_name,
               dtype = tf.float32,
               unique = False):
    global dropout, batch_normalization
    if unique:
        if var_name == 'dropout':
            if dropout is None: dropout = tf.placeholder(dtype, name= var_name)
            return dropout
        elif var_name == 'batch_normalization':
            if batch_normalization is None: batch_normalization = tf.placeholder(dtype, name= var_name)
            return batch_normalization
    elif var_name in ['input','label']:
        # input
        return tf.placeholder(dtype, [None, inpuit_dim],name=var_name)
    elif var_name == 'img':
        # img_dim = [长 宽 张]
        full_size = inpuit_dim[0]* inpuit_dim[1]* inpuit_dim[2]
        vector = tf.placeholder(dtype, [None, full_size])
        return tf.reshape(vector, shape=[-1, inpuit_dim[0], inpuit_dim[1], inpuit_dim[2]], name=var_name)
    else:
        return tf.placeholder(dtype, inpuit_dim, name= var_name)

def maxpooling2d(inputs,
                 pool_size,
                 strides=(1, 1),
                 padding='VALID'):
    pool_size = list(np.concatenate(([1],pool_size,[1]),axis=0))
    strides = list(np.concatenate(([1],strides,[1]),axis=0))
    return tf.nn.max_pool(inputs, ksize = pool_size, strides = strides, padding = padding)

def flatten(inputs):
    return tf.layers.flatten(inputs)
    
def concatenate(inputs):
    return tf.concat(inputs,axis=-1)
    
def noise(inputs,
          prob,
          noise_type = 'mask'):
    rand_mat = tf.random_uniform(shape=tf.shape(inputs),minval=0,maxval=1)
    noise_co = tf.to_float(rand_mat < prob,name='Noise') # 噪声系数矩阵
    non_noise_co = 1-noise_co # 保留系数矩阵
    if noise_type=='gaussian':
        rand_gauss = tf.truncated_normal(inputs.shape, mean=0.0, stddev=1.0, dtype=tf.float32)
        output = inputs * non_noise_co + rand_gauss * noise_co
    else:
        output = inputs * non_noise_co
    return output, noise_co

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
        if type(activation) == str:
            self.activation = Activation.get(activation)
        else:
            self.activation = activation
        self.trainable = trainable
        self.is_dropout = is_dropout
        self.is_bn = is_bn
        
    def __call__(self, inputs):
        if hasattr(self, 'output') == False: 
            self.build_layer(inputs)
        return self.output
        
    def build_layer(self, inputs):
        if type(inputs) == list:
            inputs = concatenate(inputs)

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
    
    
class Conv2D(Layer):
    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='VALID',
                 **kwargs):
        self.output_dim = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.name = 'Conv2D'
        super(Conv2D, self).__init__(**kwargs)
    
    def get_add_in(self, inputs):
        strides = list(np.concatenate(([1],self.strides,[1]),axis=0))
        add_in = tf.nn.conv2d(inputs, self.weight, strides=strides, padding=self.padding)
        return add_in
        