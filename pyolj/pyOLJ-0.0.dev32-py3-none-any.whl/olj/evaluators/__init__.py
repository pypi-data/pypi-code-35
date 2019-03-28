from .lab00 import *


def get_evaluator(fn):
    if fn.__name__ == 'dot':
        return DotEvaluator
    elif fn.__name__ == 'linear_stretch':
        return LinearStretchEvaluator
    elif fn.__name__ == 'histogram':
        return HistogramEvaluator
    elif fn.__name__ == 'threshold':
        return ThresholdEvaluator
    elif fn.__name__ == 'conv2d':
        return Conv2DEvaluator
    elif fn.__name__ == 'linear':
        return LinearEvaluator
    elif fn.__name__ == 'matchTemplate':
        return MatchTemplateEvaluator
