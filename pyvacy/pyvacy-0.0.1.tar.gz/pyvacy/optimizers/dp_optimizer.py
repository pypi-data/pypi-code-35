import math
import torch
from torch.optim import Optimizer
from torch.nn.utils.clip_grad import clip_grad_norm_
from torch.distributions.normal import Normal
from torch.optim import SGD, Adam, Adagrad

def make_optimizer_class(cls):

    class DPOptimizerClass(cls):

        def __init__(self, batch_size, l2_norm_clip=0.75, noise_multiplier=0.3, *args, **kwargs):
            self.l2_norm_clip = l2_norm_clip
            self.noise = Normal(0.0, (noise_multiplier ** 2) * (l2_norm_clip ** 2) / (batch_size ** 2))
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            super(DPOptimizerClass, self).__init__(*args, **kwargs)

        def step(self, closure=None):
            for i, group in enumerate(self.param_groups):
                for p in group['params']:
                    if p.grad is not None:
                        grad = p.grad.data
                        clip_grad_norm_(p, self.l2_norm_clip, norm_type=2)
                        grad.add_(self.noise.sample(grad.size()).to(self.device))
            super(DPOptimizerClass, self).step(closure)

    return DPOptimizerClass

DPAdam = make_optimizer_class(Adam)
DPAdagrad = make_optimizer_class(Adagrad)
DPSGD = make_optimizer_class(SGD)

