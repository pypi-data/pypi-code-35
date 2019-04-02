# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 10:15:52 2019

@author: Administrator
"""

train_dict = {'loss':0.1, 'accuracy':0.0}
print(train_dict.values())
print(train_dict.keys())
train_list = list()
for key in train_dict.keys():
    train_list.append(train_dict[key])

for train in train_list:
    print(train)
    
import tensorflow as tf
a = tf.placeholder(shape = 1, name = 'dropout', dtype = tf.float32)
b = tf.Variable(tf.truncated_normal(shape=[1, 1], stddev = 0), name = 'hehehe', dtype = tf.float32)
for v in tf.global_variables():
    print(v.name)