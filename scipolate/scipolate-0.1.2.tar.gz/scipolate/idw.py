import numpy as np
from scipy.spatial.distance import cdist


class Idw:
    def __init__(self, x, y, z, radius, min_points=4, max_points=20,
                 fill_na=None, exp=2):
        # save params
        self.x = np.asarray(x)
        self.y = np.asarray(y)
        self.z = np.asarray(z)
        self.r = radius
        self.min = min_points
        self.hit_min = 0
        self.max = max_points
        self.exp = exp

        # check input data
        if not len(self.x) == len(self.y) == len(self.z):
            raise ValueError('x, y, z have to be of same length')

        if self.min > self.max:
            raise ValueError('min_points has to be smaller than max_points')

        if self.min < 1 or self.max < 1:
            raise ValueError('min_points and max_points must be larger than 0')

        if fill_na is None:
            self.na = np.nan
        elif fill_na == 'mean':
            self.na = np.nanmean(self.z)
        elif isinstance(fill_na, (int, float)):
            self.na = fill_na
        else:
            raise ValueError('fill_na has to be None, \'mean\' or a float.')

        # if input data is fine, build points
        self.p = list(zip(self.x, self.y))

    def __call__(self, xi, yi, metric='euclidean'):
        # check input
        if not len(xi) == len(yi):
            raise ValueError('xi and yi have to be of same length.')

        # build a interpolation generator
        gen = (self._point(x, y, metric=metric) for x, y in zip(xi, yi))

        # return array
        return np.fromiter(gen, dtype=float)

    def _point(self, x, y, metric='euclidean'):
        _p = [(x, y)] + self.p

        # distance matrix, only first column
        mat = cdist(_p, _p, metric=metric)[1:, 0]

        # indices is ascending order
        indices_sorted = np.argsort(mat)

        # find all within search radius
        in_radius = np.where(mat < self.r)[0]

        # intersection:
        intersect = np.intersect1d(indices_sorted, in_radius)

        # if not enough points, use na value
        if len(intersect) < self.min:
            self.hit_min += 1
            return self.na

        # if too many points, use the max closest
        if len(intersect) > self.max:
            intersect = np.argsort(mat[intersect])[:self.max:-1]

        # calculation
        _z = self.z[intersect]
        _d = mat[intersect] + 1e-15 # avoid inf weights

        # return normed
        return np.sum(_z / _d**self.exp) / np.sum(1 / _d**self.exp)






