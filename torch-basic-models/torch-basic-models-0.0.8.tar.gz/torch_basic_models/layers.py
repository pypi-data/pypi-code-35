import torch
from torch import nn
from torch.nn import functional


class GlobalPooling(nn.Module):
    def forward(self, x: torch.Tensor):
        return functional.adaptive_avg_pool2d(x, 1)


class Flatten(nn.Module):
    def forward(self, x: torch.Tensor):
        return x.view((x.size(0), -1))


class InplaceReLU(nn.ReLU):
    def __init__(self):
        super().__init__(inplace=True)


class InplaceReLU6(nn.ReLU6):
    def __init__(self):
        super().__init__(inplace=True)
