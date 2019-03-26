import time
import base64
from io import BytesIO

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm
from pyproj import Proj, transform

from . import methods


def nanminmaxscaler(x):
    return (x - np.nanmin(x)) / (np.nanmax(x) - np.nanmin(x))


class InterpolatorError(RuntimeError):
    pass


class Interpolator:
    def __init__(self, x, y, z, settings, src_epsg=25832, tgt_epsg=4326):
        # load
        self.agg = settings['agg']
        self.interp = settings['interpolator']
        self.params = self.interp.get('params', dict())
        self.report = dict(init_settings=settings)

        # get the data
        self.x = np.asarray(x)
        self.y = np.asarray(y)
        self.z = z

        self.srcProj = Proj(init='epsg:%d' % src_epsg)
        self.tgtProj = Proj(init='epsg:%d' % tgt_epsg)

        # set interpolation method
        self.method = self.get_method(self.interp)

        # build the grid
        self.xx, self.yy = self.build_grid(self.x, self.y, self.params)

        # add a validation object
        self.modeled = list(),
        self.observation = list()

    @staticmethod
    def get_method(settings):
        _f = settings.get('func')

        # switch
        if not hasattr(methods, _f.lower()):
            raise InterpolatorError('%s is not a known method.' % _f)
        else:
            return getattr(methods, _f)

    @staticmethod
    def build_grid(x, y, params):
        spacing = params.get('gridsize', 10)
        min_x = np.min(x)
        max_x = np.max(x)
        min_y = np.min(y)
        max_y = np.max(y)

        return np.meshgrid(np.arange(min_x, max_x, spacing), np.arange(min_y, max_y, spacing))

    def run(self):
        t1 = time.time()
        self.result = self.method(self, self.x, self.y, self.z, (self.xx, self.yy), **self.params)
        t2 = time.time()

        # should be validated?
        if 'validation' in self.params.keys():
            val = self.params.get('validation', dict())
            if val.get('func') == 'jacknife':
                self.jacknife(n=val.get('n'))
            else:
                raise InterpolatorError('Only Jacknife validation available')

        # create the output
        self.create_output()

        self.report['took'] = t2 - t1

    def create_output(self):
        # get the image
        im = self.build_image()

        # create the buffer and save
        buffer = BytesIO()
        im.save(buffer, format='png')
        data = 'data:image/png;base64, %s' % base64.b64encode(buffer.getvalue()).decode()

        self.report['output'] = dict(
            img=data,
            bbox=self.bbox
        )

    def __call__(self):
        self.run()
        return self.result

    @property
    def bbox(self):
        # leaflet needs latlon bounds
        return [
            transform(self.srcProj, self.tgtProj, np.min(self.x), np.max(self.y))[::-1],
            transform(self.srcProj, self.tgtProj, np.max(self.x), np.min(self.y))[::-1]
        ]

    @property
    def normalized_result(self):
        if not hasattr(self, 'result'):
            raise InterpolatorError('trying to normalize the result, before created')
        else:
            return nanminmaxscaler(self.result)

    def build_image(self):
        # get the image
        arr = np.flipud(self.normalized_result)

        # check if a color ramp is set in settings
        colormap = getattr(cm, self.params.get('colormap', 'RdYlBu_r'))

        return Image.fromarray(np.uint8(colormap(arr) * 255))

    def jacknife(self, n=None):
        # if n is None, use all
        if n is None:
            n = len(self.x)

        # choose indices
        try:
            indices = np.random.choice(range(len(self.x)), n, replace=False)
        except ValueError as e:
            raise InterpolatorError
            (str(e))

        def step(i):
            return self.method(self, np.delete(self.x, i), np.delete(self.y, i),
                np.delete(self.z, i),
                (np.asarray([self.x[i]]), np.asarray([self.y[i]])),
                **self.params)

        # run
        t1 = time.time()
        self.modeled = np.asarray([step(i) for i in indices]).flatten()
        t2 = time.time()

        # calc statistics
        self.observation = np.asarray(self.z)[indices]
        n = len(indices)

        # use an iterator over all pairs
        def pairs():
            for m, o in zip(self.modeled, self.observation):
                yield m, o

        residual = np.nanmean([np.abs(m - o) for m, o in pairs()])
        rmse = np.sqrt((1 / n) * np.nansum([(m - o)**2 for m, o in pairs()]))

        # create scatter
        scatter_data = self.create_validation_image()

        # meta data
        self.report['validation'] = dict(
            took=t2 - t1,
            residual=residual if not np.isnan(residual) else None,
            rmse=rmse if not np.isnan(rmse) else None,
            scatterplot=scatter_data
        )

    def create_validation_image(self, as_base64=True):
        plt.style.use('ggplot')

        # create the subfig
        fig, ax = plt.subplots(1, 1, figsize=(4, 4))
        ax.scatter(self.observation, self.modeled, 50, c="red")
        ax.scatter(self.observation, self.modeled, 30, c="white", alpha=0.5)
        ax.set_ylabel('Model')
        ax.set_xlabel('Observation')

        if not as_base64:
            return ax
        
        return self.img_to_base64(fig)
        # create the output figure
        #buffer = BytesIO()
        #fig.savefig(buffer, format="png")
        #buffer.seek(0)
        #data = base64.b64encode(buffer.read()).decode()

        # return
        #return 'data:image/png;base64, %s' % data

    @staticmethod
    def img_to_base64(fig, fmt='png'):
        buffer = BytesIO()
        fig.savefig(buffer, format=fmt)
        buffer.seek(0)
        data = base64.b64encode(buffer.read()).decode()

        return 'data:image/%s;base64, %s' % (fmt, data)
