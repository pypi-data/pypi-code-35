# -*- coding: utf-8 -*-

__all__ = ['ae','ft_model','pre_model','rbm']
# deprecated to keep older scripts who import this from breaking
from deepfree.model.ae import AE
from deepfree.model.ft_model import DBN, SAE, FTModel
from deepfree.model.pre_model import PreModel
from deepfree.model.rbm import RBM
