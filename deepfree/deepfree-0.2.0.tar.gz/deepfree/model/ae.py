# -*- coding: utf-8 -*-
import tensorflow as tf
from deepfree.core._model import Model
from deepfree.core._layer import PHVariable,Dense
from deepfree.base._attribute import _AE_DICT

class AE(Model):
    def __init__(self,**kwargs):
        self.show_dict = _AE_DICT.copy()
        kwargs = dict(_AE_DICT, **kwargs)
        super(AE, self).__init__(**kwargs)
        
        self.hidden_func = self.sub_func[0]
        self.output_func = self.sub_func[1]
        self.alpha = 1-self.beta
        
        # sae: KL 要求 h 必须是0~1之间的数
        if self.sub_type=='sae' and (self.hidden_func not in ['softmax','sigmoid','gaussian']):
            self.hidden_func = 'sigmoid'
    
    def build_model(self):
        
        # variable
        self.input = PHVariable([None, self.struct[0]])('input')
        self.recon = PHVariable([None, self.struct[0]])('recon')
        
        ''' 自编码器 [ae] '''
        x=self.input
        # encoder
        Encoder = Dense(self.struct[1], weight = self.weight, bias = self.bias, activation = self.hidden_func)
        h = Encoder(x)
        
        
        # decoder
        Decoder = Dense(self.struct[0], weight=tf.transpose(Encoder.weight), activation = self.output_func)
        y = Decoder(h)
        
        
        # save variable
        self.transform = Encoder
        self.logits = Decoder.add_in
        self.output = y
        
        # save bias
        self.bias_x = Encoder.bias
        self.bias_h = Decoder.bias
        
        # loss
        self.loss = self.get_loss(self.recon, logits = self.logits, output = self.output)
        
        if self.model_type=='dae':
            ''' 去噪自编码器 [dae] '''
            x_noise = self.add_noise(x)
            h = Encoder(x_noise)
            y = Decoder(h)
            self.loss = self.get_loss_with_co(self.alpha * self.A_co + self.beta * self.N_co)
        
        elif self.model_type=='sae':
            ''' 稀疏自编码器 [sae] '''
            self.loss = self.alpha * self.loss + self.beta * self.sparse_loss(h)
    
    def add_noise(self,x):
        """
            A为损失系数矩阵，一行对应一个样本，引入噪声的变量的系数为alpha，未引入噪声的为beta
            当噪声类型为 Masking noise (mn) 时，相当于做 dropout
        """ 
        rand_mat = tf.random_uniform(shape=tf.shape(x),minval=0,maxval=1)
        self.N_co = tf.to_float(rand_mat<self.prob,name='Noise') # 噪声系数矩阵
        self.A_co = 1-self.N_co # 保留系数矩阵
        if self.noise_type=='gs':
            rand_gauss = tf.truncated_normal(x.shape, mean=0.0, stddev=1.0, dtype=tf.float32)
            x_noise = x * self.A_co + rand_gauss * self.N_co
        else:
            x_noise = x * self.A_co
        return x_noise