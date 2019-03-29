# -*- coding: utf-8 -*-
from deepfree.model.rbm import RBM
from deepfree.model.ae import AE

class PreModel(object):
    def __init__(self,**kwargs):
        for key in kwargs.keys(): setattr(self, key, kwargs[key])
        self.kwargs = kwargs
        
        self.build_model()

    def build_model(self):
        self.sub_list = list()
        for i in range(len(self.struct) -1):
            n_v = self.struct[i]
            n_h = self.struct[i+1]
            weight = self.layer_list[i].weight
            bias = self.layer_list[i].bias
            name = self.sub_type + '_' + str(i + 1)
            self.kwargs.update({'name':name, 
                                'struct':[n_v,n_h], 
                                'weight': weight, 
                                'bias': bias,
                                'is_sub': True})
            if self.sub_type == 'rbm':
                sub = RBM(**self.kwargs)
            else:
                sub = AE(**self.kwargs)
                
            self.sub_list.append(sub)
            