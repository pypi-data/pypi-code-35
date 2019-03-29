# -*- coding: utf-8 -*-
import tensorflow as tf
from deepfree.core._layer import Activation

class Loss(object):
    def get_loss(self, label, logits=None, output=None, loss_func=None):
        if loss_func is None :
            loss_func = self.loss_func
        # logits
        if loss_func=='cross_entropy':
            # 使用 cross_entropy 的时候，应尽量让 label 和 func(logits) 处于0~1之间
            label = tf.clip_by_value(label,0, 1.0)
            if self.output_func=='softmax':
                return tf.losses.softmax_cross_entropy(label, logits)
            if self.output_func=='sigmoid':
                return tf.losses.sigmoid_cross_entropy(label, logits)
        # output
        if loss_func=='mse':
            if output is None:
                output = Activation.get(self.output_func)(logits)
            return tf.losses.mean_squared_error(label, output)
        
    def get_loss_with_co(self,co_mat = None):
        # 计算 loss mat <未取均值之前>
        y = self.label
        p = self.output
        if co_mat is None:
            co_mat = tf.ones_like(y)
        if self.loss_func=='mse':
            loss_mat=tf.square(p-y)
        elif self.loss_func=='cross_entropy':
            y = tf.clip_by_value(y,0, 1.0)
            p = tf.clip_by_value(p,1e-10, 1.0-1e-10)
            if self.output_func=='sigmoid':
                """
                    let `z = logits`, `y = labels`.
                    loss_mat = y * -log(sigmoid(z)) + (1 - y) * -log(1 - sigmoid(z))
                    log1p(x) = log(1 + x)
                """
                loss_mat=-y * tf.log(p) - (1 - y)* tf.log(1 - p)
            elif self.output_func=='softmax':
                loss_mat=-y * tf.log(p)
        # 乘以系数项
        loss_mat *= co_mat
        # 计算 loss
        if self.loss_func =='cross_entropy' and self.output_func=='softmax':
            loss = tf.reduce_mean(tf.reduce_sum(loss_mat,axis=1))
        else:
            loss = tf.reduce_mean(loss_mat)
        return loss_mat,loss
    
    def get_sparse_loss(self,h):
        q = tf.clip_by_value(tf.reduce_mean(h,axis=0),1e-10, 1.0-1e-10)
        p = tf.clip_by_value(tf.constant(self.prob, shape=[1,self.n_h]),1e-10, 1.0-1e-10)
        KL=p*tf.log(p/q)+(1-p)*tf.log((1-p)/(1-q))
        return tf.reduce_sum(KL)
    
    def get_domain_loss(self,source_x, target_x):
        source_center = tf.reduce_mean(source_x, axis=0)
        target_center = tf.reduce_mean(target_x, axis=0)
        return tf.reduce_sum(tf.square(source_center - target_center))