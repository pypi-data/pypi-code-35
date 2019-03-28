import numpy as np
import random
import cv2
import torch
import torch.nn.functional as F
from .base import BaseEvaluator


class DotEvaluator(BaseEvaluator):
    def __init__(self, fn):
        self.fn = fn
        self.Fn = np.dot
        self.tests = [self.assertAllClose, self.assertAllClose]
        super(DotEvaluator, self).__init__()

    def inputs(self):
        sha, shb, shc = random.randint(1, 4),  random.randint(1, 4), random.randint(1, 4)
        a = np.random.random((sha, shb))
        b = np.random.random((shb, shc))
        return a, b


class LinearStretchEvaluator(BaseEvaluator):
    def __init__(self, fn):
        self.fn = fn
        self.tests = [self.assertType, self.assertAttribute('dtype'), self.assertAttribute('shape'), ]
        self.tests += [self.assertAllClose, ] * 100
        super(LinearStretchEvaluator, self).__init__()

    def Fn(self, im, alpha, beta):
        return np.clip(np.rint(im.astype(np.float32) * alpha + beta), 0, 255).astype(np.uint8)

    def inputs(self):
        sh = (random.choice([1,3]), random.randint(1, 10), random.randint(1, 10))
        if sh[0] == 0:
            sh = sh[1:]
        im = np.random.randint(0, 256, sh).astype(np.uint8)
        if random.randint(0, 1) == 0:
            alpha, beta = random.randint(0, 256),  random.randint(0, 256)
        else:
            alpha, beta = random.random()*256, random.random()*256
        return im, alpha, beta


class HistogramEvaluator(BaseEvaluator):
    def __init__(self, fn):
        self.fn = fn
        self.tests = [self.assertType, self.assertAttribute('shape'), self.assertAllClose, self.assertAllClose]
        super(HistogramEvaluator, self).__init__()

    def Fn(self, im, n_bins):
        hists = []
        for c in range(3):
            hists.append(cv2.calcHist([im[c]], [0], None, [n_bins], [0, 256]).T[0])
        return np.concatenate(hists) / im.size

    def inputs(self):
        im = np.random.randint(0, 256, ((3, 256, 256))).astype(np.uint8)
        n_bins = np.random.randint(0, 256)
        return im, n_bins


class ThresholdEvaluator(BaseEvaluator):
    def __init__(self, fn):
        self.fn = fn
        self.tests = [self.assertType, self.assertAttribute('shape'), self.assertAllClose, self.assertAllClose]
        super(ThresholdEvaluator, self).__init__()

    def Fn(self, im, value):
        return cv2.threshold(im, value, 255, cv2.THRESH_BINARY)[1]

    def inputs(self):
        im = np.random.randint(0, 256, ((256, 256))).astype(np.uint8)
        value = np.random.randint(0, 256)
        return im, value


class Conv2DEvaluator(BaseEvaluator):
    def __init__(self, fn):
        self.fn = fn
        self.tests = [self.assertType, self.assertAttribute('shape')]
        self.tests += [self.assertAllClose, ] * 10
        super(Conv2DEvaluator, self).__init__()

    def Fn(self, input, weight):
        input = torch.from_numpy(input)
        weight = torch.from_numpy(weight)
        return F.conv2d(input, weight).numpy()

    def inputs(self):
        choice = random.choice([1,2,3])
        kH, kW = random.choice([1, 3, 5]), random.choice([1, 3, 5])
        if choice == 1:
            input = np.random.rand(1, 1, 32, 32).astype(np.float32)
            weight = np.random.rand(1, 1, kH, kW).astype(np.float32)
        elif choice == 2:
            input = np.random.rand(1, 3, 32, 32).astype(np.float32)
            weight = np.random.rand(5, 3, kH, kW).astype(np.float32)
        else:
            input = np.random.rand(3, 3, 32, 32).astype(np.float32)
            weight = np.random.rand(5, 3, kH, kW).astype(np.float32)

        return input, weight

class LinearEvaluator(BaseEvaluator):
    def __init__(self, fn):
        self.fn = fn
        self.tests = [self.assertType, self.assertAttribute('shape')]
        self.tests += [self.assertAllClose, ] * 10
        super(LinearEvaluator, self).__init__()

    def Fn(self, input, weight, bias):
        input = torch.from_numpy(input)
        weight = torch.from_numpy(weight)
        bias = torch.from_numpy(bias)
        return F.linear(input, weight, bias).numpy()

    def inputs(self):
        b_s = random.randint(1, 100)
        d_o = random.randint(1, 100)
        d_i = random.randint(1, 100)
        n_intermediate = random.choice([0, 1, 2])

        input_shape = [b_s, ] + [random.randint(0, 100) for _ in range(n_intermediate)] + [d_i, ]
        input = np.random.rand(*input_shape)
        weight = np.random.rand(d_o, d_i)
        bias = np.random.rand(d_o)
        return input, weight, bias

class MatchTemplateEvaluator(BaseEvaluator):
    def __init__(self, fn):
        self.fn = fn
        self.tests = [self.assertType, self.assertAttribute('shape')]
        self.tests += [self.assertAllClose, ] * 10
        super(MatchTemplateEvaluator, self).__init__()

    def Fn(self, input, templ):
        out = []
        for i in input:
            out.append(cv2.matchTemplate(i, templ, method=cv2.TM_SQDIFF))

        return np.stack(out)

    def inputs(self):
        b_s = random.randint(1, 100)
        input_shape = [b_s, random.randint(10, 100), random.randint(10, 100)]
        input = np.random.rand(*input_shape).astype(np.float32)
        templ = np.random.rand(np.random.randint(3, 7), np.random.randint(3, 7)).astype(np.float32)
        return input, templ