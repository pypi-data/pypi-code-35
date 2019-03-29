# -*- coding: utf-8 -*-
import tensorflow as tf
from deepfree.core._model import Model
from deepfree.core._layer import phvariable,Dense
from deepfree.base._attribute import RBM_DICT

prob_func = {'gaussian': 'linear', 'binary': 'sigmoid'}

class RBM(Model):
    def __init__(self, **kwargs):
        self.show_dict = RBM_DICT.copy()
        kwargs = dict(RBM_DICT, **kwargs)
        super(RBM, self).__init__(**kwargs)
    
    def build_model(self):
        
        # variable
        self.input = phvariable([None, self.struct[0]],'input')
        
        with tf.name_scope('CD-k'):
            
            v0 = self.input          # v_0
            # hidden layer
            V2H = Dense(self.struct[1], activation = prob_func[self.unit_type[0]]) 
            p_h0 = V2H(v0)        # p(h|v)_0
            h0 = self.sample(p_h0,0) # h_0
            
            # visible layer
            H2V = Dense(self.struct[0], weight=tf.transpose(V2H.weight), activation = prob_func[self.unit_type[1]])
            p_vk = H2V(h0)       # p(v|h)_k
            vk = self.sample(p_vk,1) # v_k
            
            # save variable
            self.transform = V2H
            
            # save bias
            self.bias_x = V2H.bias
            self.bias_h = H2V.bias
            
            # cd-k
            for k in range(self.cd_k-1):
                p_hk = V2H(vk)
                hk = self.sample(p_hk,0)
                p_vk = H2V(hk)
                vk = self.sample(p_vk,0)
            
            p_hk = V2H(vk)        # p(h|v)_k
            hk = p_hk                # 根据 Hinton 论文，这里不采样 
            vk = p_vk                # 根据 Hinton 论文，这里不采样 
            
            # loss
            self.maximum_likelihood(v0, vk, h0, hk)
    
    def sample(self,p,index):
        '''
            二值单元：
            p(h|v) = sigmoid(v) -> sample: if p<p(h|v): h = 1 , else: h = 0
            高斯单元：
            p(h|v) ~ N(u,s) -> sample: h = u = linear(v)
        '''
        if self.unit_type[index] == 'gaussian':
            return p
        else:
            rand_mat = tf.random_uniform(shape=tf.shape(p),minval=0,maxval=1)
            return tf.to_float(rand_mat<p) # sample
    
    def maximum_likelihood(self, v0, vk, h0, hk):
        with tf.name_scope('Gradient_Descent'):
            # loss = Maximum likelihood (vk=v0)
            
            positive=tf.matmul(tf.expand_dims(v0,-1), tf.expand_dims(h0,1))
            negative=tf.matmul(tf.expand_dims(vk,-1), tf.expand_dims(hk,1))
            
            grad_w= tf.reduce_mean(tf.subtract(positive, negative), 0)
            grad_v= tf.reduce_mean(tf.subtract(h0, hk), 0) 
            grad_h= tf.reduce_mean(tf.subtract(v0, vk), 0) 

            self.w_upd8 = self.weight.assign_add(grad_w *self.pre_lr)
            self.v_upd8 = self.bias_x.assign_add(grad_v *self.pre_lr) 
            self.h_upd8 = self.bias_h.assign_add(grad_h *self.pre_lr)
            
            # 构建训练步
            self.loss = tf.reduce_mean(grad_w)
            self.batch_training =  [self.w_upd8, self.v_upd8, self.h_upd8]