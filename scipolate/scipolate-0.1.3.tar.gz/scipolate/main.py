from time import time

import numpy as np

from . import methods


class Interpolator:
    def __init__(self, method, x, y, z, validate=True, **kwargs):
        # user settings
        self._method = method
        self._f = None
        self.method = method
        self.x = x
        self.y = y
        self.z = z
        self.settings = kwargs
        # always pass a reference to the class to each method
        self.settings['Intp'] = self

        # internal settings
        self.observations = np.array([])
        self.model = np.array([])
        self.result = None
        self.took = 0
        self.score_took = 0

        # check validation
        if validate:
            self.validate()

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, name):
        if not hasattr(methods, name):
            raise ValueError('method %s not known' % name)
        else:
            self._f = getattr(methods, name)
            self._method = name

    def validate(self, n=None):
        n = len(self.x) if n is None else n

        # reset the obs and model
        self.observations = np.empty(n)
        self.model = np.empty(n)

        # do a leave one out cross validation
        idx = np.random.permutation(n)
        t0 = time()
        for i, j in enumerate(idx):
            obs = self._f(
                np.delete(self.x, i),
                np.delete(self.y, i),
                np.delete(self.z, i),
                (np.array(self.x[i]), np.array(self.y[i])),
                **self.settings
            )
            self.observations[j] = self.z[i]
            self.model[j] = obs

        t1 = time()
        self.score_took = t1 - t0

        return self.score

    @property
    def score(self):
        # rmse
        return self.rmse

    @property
    def rmse(self):
        return np.sqrt(np.nanmean(np.power(self.observations - self.model, 2)))

    @property
    def residual(self):
        return np.nanmean(np.abs(self.observations - self.model))

    def run(self, grid):
        t0 = time()
        res = self._f(self.x, self.y, self.z, grid, **self.settings)
        t1 = time()

        # set result
        self.result = res
        self.took = t1 - t0

        # return
        return self.result

    def __call__(self, grid):
        return self.run(grid=grid)
