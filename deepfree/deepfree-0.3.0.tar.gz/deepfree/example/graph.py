# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 20:22:21 2019

@author: Fuzz4
"""
import tensorflow as tf 


init_dict = {'layer_list':[]}

class Layer(object):
    def __init__(self):
        self.weight = tf.Variable(tf.truncated_normal( 
                      shape=[10, 5], stddev = 0.1), trainable = True, name='weight')

class B(object):
    def __init__(self):
        for key in init_dict.keys(): setattr(self, key, init_dict[key])
        
        print(self.layer_list)
        
    def add_layer(self,layer):
        self.layer_list.append(layer)
        
b = B()
b.add_layer(Layer())
b.add_layer(Layer())
b.add_layer(Layer())
print(b.layer_list)