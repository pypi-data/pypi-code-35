import time
import base64
from io import BytesIO

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm
from pyproj import Proj, transform

from .main import Interpolator


def nanminmaxscaler(x):
    return (x - np.nanmin(x)) / (np.nanmax(x) - np.nanmin(x))


class InterpolatorError(RuntimeError):
    pass


class WebInterface:
    def __init__(self, x, y, z, settings, src_epsg=25832, tgt_epsg=4326):
        # load
        self.agg = settings['agg']
        self.interp = settings['interpolator']
        self.params = self.interp.get('params', dict())
        self.report = dict(init_settings=settings)

        self.srcProj = Proj(init='epsg:%d' % src_epsg)
        self.tgtProj = Proj(init='epsg:%d' % tgt_epsg)

        # build the grid
        self.xx, self.yy = self.build_grid(x, y, self.params)

        # get the method
        if not 'func' in self.interp:
            raise AttributeError('No interpolation method has been specified.')
        method = self.interp['func']
        val = True if 'validation' in self.params else False

        # build the Interpolator
        self.Intp = Interpolator(method, x, y, z, validate=val, **self.params)

    @staticmethod
    def build_grid(x, y, params):
        spacing = params.get('gridsize', 10)
        min_x = np.min(x)
        max_x = np.max(x)
        min_y = np.min(y)
        max_y = np.max(y)

        return np.meshgrid(np.arange(min_x, max_x, spacing), np.arange(min_y, max_y, spacing))

    def run(self):
        grid = (self.xx.flatten(), self.yy.flatten())
        self.result = self.Intp.run(grid).reshape(self.xx.shape)

        # create the output
        self.create_output()

    def create_output(self):
        # get the image
        im = self.build_image()

        # create the buffer and save
        buffer = BytesIO()
        im.save(buffer, format='png')
        data = 'data:image/png;base64, %s' % base64.b64encode(buffer.getvalue()).decode()

        self.report['output'] = dict(
            took=self.Intp.took,
            img=data,
            bbox=self.bbox
        )

        # add the validation data
        if 'validation' in self.params:
            # create scatter
            scatter_data = self.create_validation_image()

            # meta data
            self.report['validation'] = dict(
                took=self.Intp.score_took,
                residual=self.Intp.residual,
                rmse=self.Intp.rmse,
                scatterplot=scatter_data
            )

    def __call__(self):
        self.run()
        return self.result

    @property
    def bbox(self):
        x = self.Intp.x
        y = self.Intp.y
        # leaflet needs latlon bounds
        return [
            transform(self.srcProj, self.tgtProj, np.min(x), np.max(y))[::-1],
            transform(self.srcProj, self.tgtProj, np.max(x), np.min(y))[::-1]
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

        obs = self.Intp.observations
        mod = self.Intp.model

        # create the subfig
        fig, ax = plt.subplots(1, 1, figsize=(4, 4))
        ax.scatter(obs, mod, 50, c="red")
        ax.scatter(obs, mod, 30, c="white", alpha=0.5)
        ax.set_ylabel('Model')
        ax.set_xlabel('Observation')

        if not as_base64:
            return ax
        
        return self.img_to_base64(fig)

    @staticmethod
    def img_to_base64(fig, fmt='png'):
        buffer = BytesIO()
        fig.savefig(buffer, format=fmt)
        buffer.seek(0)
        data = base64.b64encode(buffer.read()).decode()

        return 'data:image/%s;base64, %s' % (fmt, data)
