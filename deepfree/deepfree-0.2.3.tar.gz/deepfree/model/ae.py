# -*- coding: utf-8 -*-
import tensorflow as tf
from deepfree.core._model import Model
from deepfree.core._layer import phvariable, noise, Dense
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
        self.input = phvariable([None, self.struct[0]],'input')
        self.recon = phvariable([None, self.struct[0]],'recon')
        
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
            x_noise, noise_co = noise(x, self.prob, noise_type = self.noise_type)
            non_noise_co = 1- noise_co
            h = Encoder(x_noise)
            y = Decoder(h)
            self.loss = self.get_loss_with_co(co_mat = self.alpha * non_noise_co + self.beta * noise_co)
        
        elif self.model_type=='sae':
            ''' 稀疏自编码器 [sae] '''
            self.loss = self.alpha * self.loss + self.beta * self.get_sparse_loss(h)
    