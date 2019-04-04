from plotly import graph_objs as go
from deepreplay.plot import build_2d_grid
import numpy as np
from ipywidgets import FloatSlider, VBox, interactive
from matplotlib import pyplot as plt

class plotNorm(object):
    def __init__(self, order=1, xlim=[-25, 25], ylim=[-25, 25]):
        self.grid = build_2d_grid(xlim, ylim, n_lines=200, n_points=200)
        self.set_norm(order)

    @property
    def traces(self):
        return dict(contour=self.contour)

    def set_norm(self, order):
        self.order = order
        self.calc_norm()
        self.contour = self.plot_contour()

    def calc_norm(self):
        self.norm = np.apply_along_axis(func1d=lambda v: np.linalg.norm(v, ord=self.order), axis=2, arr=self.grid)

    def plot_contour(self):
        contour = go.Contour(x=self.grid[:, 0, 0],
                             y=self.grid[0, :, 1],
                             z=self.norm,
                             autocontour=False,
                             contours={'start': 0, 'end': 50, 'size': 5})
        return contour

def build_figure(n_obj):
    traces = n_obj.traces
    fig = go.Figure([traces['contour']])
    f = go.FigureWidget(fig)
    f['layout']['width'] = 500
    f['layout']['height'] = 500

    def update(order):
        n_obj.set_norm(order)
        contour = n_obj.traces['contour']
        if order == 1:
            name = 'Manhtattan'
        elif order == 2:
            name = 'Euclidean'
        else:
            name = 'Minkowski'

        with f.batch_update():
            f['layout']['title'] = 'L{} Norm - {} Distance'.format(int(order), name)
            f.data[0].z = contour.z

    order = FloatSlider(description=r'\(p\)', value=1, min=1, max=10, step=1)

    return (f, interactive(update, order=order))

def plot_norms():
    plt.style.use('fivethirtyeight')
    orders = [.5, 1, 1.5, 2, 10, 100]
    grid = build_2d_grid([-25, 20], [25, -20], n_lines=200, n_points=200)
    norms = [np.apply_along_axis(func1d=lambda v: np.linalg.norm(v, ord=order), axis=2, arr=grid) for order in orders]
    figure, axes = plt.subplots(2, 3, figsize=(12, 8))
    for i in range(6):
        r = i // 3
        c = i - r * 3
        axes[r, c].contourf(grid[:, :, 0], grid[:, :, 1], norms[i], cmap=plt.cm.brg, alpha=0.3, levels=np.linspace(0, 20, 11))
        axes[r, c].set_title('p = {}'.format(orders[i]))
    figure.tight_layout()
    return figure

if __name__ == '__main__':
    norm = plotNorm()
    vb = VBox(build_figure(norm), layout={'align_items': 'center'})
