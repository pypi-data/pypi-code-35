from plotly import graph_objs as go
from copy import deepcopy
from deepreplay.plot import build_2d_grid
import numpy as np
from ipywidgets import VBox, interactive, IntSlider, FloatSlider, HBox, interact

def data(seed=42):
    np.random.seed(seed)
    x1 = np.random.randn(1, 20) * 1.3
    x2 = np.random.randn(1, 20)
    x1 = x1 - x1.mean()
    x2 = x2 - x2.mean()
    X = np.concatenate([x1, x2], axis=0)
    return X

def build_grid_traces(grid):
    grid_lines = (go.Scatter(x=line[:, 0], y=line[:, 1], name='grid', mode='lines', showlegend=False, line={'color': 'black', 'width': 1})
                for line in grid)
    return grid_lines

def transf_grid_traces(grid, transf):
    transf_grid = np.matmul(grid, transf.T)
    return build_grid_traces(transf_grid)

def transformation_steps(transf, steps):
    canonical = np.array([[1, 0], [0, 1]])
    can_to_transf = np.array([canonical + i * (transf - canonical) / steps for i in range(steps + 1)])
    return can_to_transf

def build_vector_trace(vector, **kwargs):
    v = vector.squeeze()
    return go.Scatter(x=[0, v[0]], y=[0, v[1]], **kwargs)

def transf_vector_trace(vector, transf, **kwargs):
    v = np.matmul(vector.squeeze(), transf.T)
    return build_vector_trace(v, **kwargs)

def build_data_trace(X, **kwargs):
    return go.Scatter(x=X[:, 0], y=X[:, 1], mode='markers', **kwargs)

def transf_data_trace(X, transf, **kwargs):
    data = np.matmul(X, transf.T)
    return build_data_trace(data, **kwargs)

class plotEigen(object):
    def __init__(self, X, steps=20):
        self.steps = steps
        self.basis1 = np.array([1, 0])
        self.basis2 = np.array([0, 1])
        if not X.shape == (2, 2):
            self.X = X
            self.cov = np.cov(X)
            self.eigenvalues, self.eigenvectors = np.linalg.eig(self.cov)

            self.ev1 = self.eigenvectors[:, 0]
            self.ev2 = self.eigenvectors[:, 1]

            self.cov_steps = transformation_steps(self.cov, self.steps)
            self.eigen_steps = transformation_steps(self.eigenvectors.T, self.steps)

            xlim = [np.floor(X[0].min()) - 1, np.ceil(X[0].max()) + 1]
            ylim = [np.floor(X[1].min()) - 1, np.ceil(X[1].max()) + 1]
            self.grid = build_2d_grid(xlim, ylim, n_lines=7, n_points=10)
            tgrid = np.dot(self.grid, self.eigenvectors.T)

            self.xrange = [tgrid[:, :, 0].min() - .25, tgrid[:, :, 0].max() + .25]
            self.yrange = [tgrid[:, :, 1].min() - .25, tgrid[:, :, 1].max() + .25]
        else:
            self.X = None
            xlim = ylim = [-1, 1]
            self.grid = build_2d_grid(xlim, ylim, n_lines=7, n_points=10)
            self.set_transf(X)

    def projection(self, data_trace, axis='x', draw_lines=False):
        assert axis in ['x', 'y']
        proj = deepcopy(data_trace)
        proj['y' if axis == 'x' else 'x'] = np.zeros_like(proj[axis])
        proj['name'] = '{} Component'.format(axis)
        proj['marker']['color'] = 'blue' if axis == 'x' else 'green'
        lines = None
        if draw_lines:
            lines = (go.Scatter(x=[dx, px], y=[dy, py], name='projection {}'.format(axis), showlegend=False,
                                mode='lines', line={'color': 'black', 'width': 1, 'dash': 'dash'})
                     for dx, px, dy, py in zip(data_trace['x'], proj['x'], data_trace['y'], proj['y']))
        return proj, lines

    def set_transf(self, transf):
        self.custom_transf = transf
        self.custom_steps = transformation_steps(self.custom_transf, self.steps)
        self.custom_eigenvalues, self.custom_eigenvectors = np.linalg.eig(self.custom_transf)
        if np.any(np.iscomplex(self.custom_eigenvectors)):
            print("Transformation yields complex eigenvectors!")
        else:
            self.custom_ev1 = self.custom_eigenvectors[:, 0]
            self.custom_ev2 = self.custom_eigenvectors[:, 1]

            tgrid = np.dot(self.grid, self.custom_transf.T)
            self.xrange = [np.minimum(tgrid[:, :, 0].min() - .25, -2.1), np.maximum(tgrid[:, :, 0].max() + .25, 2.1)]
            self.yrange = [np.minimum(tgrid[:, :, 1].min() - .25, -2.1), np.maximum(tgrid[:, :, 1].max() + .25, 2.1)]

    def transf_custom(self, step, basis=False):
        tgrid = transf_grid_traces(self.grid, self.custom_steps[step])
        if basis:
            tev1 = transf_vector_trace(self.basis1.T, self.custom_steps[step], name='Transf. i', marker={'color': 'red', 'symbol': 'triangle-up'})
            tev2 = transf_vector_trace(self.basis2.T, self.custom_steps[step], name='Transf. j', marker={'color': 'red', 'symbol': 'triangle-up'})
        else:
            tev1 = transf_vector_trace(self.custom_ev1.T, self.custom_steps[step], name='Transf. EigenVector 1', marker={'color': 'red', 'symbol': 'triangle-up'})
            tev2 = transf_vector_trace(self.custom_ev2.T, self.custom_steps[step], name='Transf. EigenVector 2', marker={'color': 'red', 'symbol': 'triangle-up'})
        tdata = None
        if self.X is not None:
            tdata = transf_data_trace(self.X.T, self.custom_steps[step], name='Transf. Data', marker={'color': 'red'})
        return tev1, tev2, tdata, tgrid

    def transf_cov(self, step):
        tgrid = transf_grid_traces(self.grid, self.cov_steps[step])
        tev1 = transf_vector_trace(self.ev1.T, self.cov_steps[step], name='Transf. EigenVector 1', marker={'color': 'red', 'symbol': 'triangle-up'})
        tev2 = transf_vector_trace(self.ev2.T, self.cov_steps[step], name='Transf. EigenVector 2', marker={'color': 'red', 'symbol': 'triangle-up'})
        tdata = transf_data_trace(self.X.T, self.cov_steps[step], name='Transf. Data', marker={'color': 'red'})
        return tev1, tev2, tdata, tgrid

    def transf_eig(self, step):
        tgrid = transf_grid_traces(self.grid, self.eigen_steps[step])
        tev1 = transf_vector_trace(self.ev1.T, self.eigen_steps[step], name='Transf. EigenVector 1', marker={'color': 'red', 'symbol': 'triangle-up'})
        tev2 = transf_vector_trace(self.ev2.T, self.eigen_steps[step], name='Transf. EigenVector 2', marker={'color': 'red', 'symbol': 'triangle-up'})
        tdata = transf_data_trace(self.X.T, self.eigen_steps[step], name='Transf. Data', marker={'color': 'red'})
        return tev1, tev2, tdata, tgrid

def build_figure(eigen_obj, basis=False):
    tev1, tev2, _, tgrid = eigen_obj.transf_custom(0, basis)

    fig = go.Figure([tev1, tev2, tev1, tev2, *tgrid],
                    layout=go.Layout(xaxis={'zeroline': False, 'range': eigen_obj.xrange},
                                     yaxis={'zeroline': False, 'range': eigen_obj.yrange},
                                     width=600,
                                     height=500,
                                     title='EigenValues: {:.2f} / {:.2f}'.format(*eigen_obj.custom_eigenvalues)))
    fig.data[1].line.dash = 'dash'
    fig.data[2].name = tev1.name[8:]
    fig.data[2].marker.color = 'black'
    fig.data[3].name = tev2.name[8:]
    fig.data[3].marker.color = 'black'
    fig.data[3].line.dash = 'dash'

    f = go.FigureWidget(fig)
    if basis:
        f['layout']['title'] = 'Basis Vectors'

    step_slider = IntSlider(description='Step', value=0, min=0, max=20, step=1)

    w11 = FloatSlider(description='w11', value=1, min=-3, max=3, step=.1)
    w21 = FloatSlider(description='w21', value=0, min=-3, max=3, step=.1)

    w12 = FloatSlider(description='w12', value=0, min=-3, max=3, step=.1)
    w22 = FloatSlider(description='w22', value=1, min=-3, max=3, step=.1)

    def update_step(w11, w21, w12, w22, step):
        transf = np.array([[w11, w12], [w21, w22]])
        eigen_obj.set_transf(transf)

        ev1, ev2, _, _ = eigen_obj.transf_custom(0, basis)
        tev1, tev2, _, tgrid = eigen_obj.transf_custom(step, basis)

        tgrid = list(tgrid)

        values = {tev1.name: {'x': tev1.x, 'y': tev1.y},
                  tev2.name: {'x': tev2.x, 'y': tev2.y},
                  tev1.name[8:]: {'x': ev1.x, 'y': ev1.y},
                  tev2.name[8:]: {'x': ev2.x, 'y': ev2.y}}

        with f.batch_update():
            if basis:
                f['layout']['title'] = 'Basis Vectors'
            else:
                f['layout']['title'] = 'EigenValues: {:.2f} / {:.2f}'.format(*eigen_obj.custom_eigenvalues)
            f['layout']['xaxis'].range = eigen_obj.xrange
            f['layout']['yaxis'].range = eigen_obj.yrange
            lines = -1
            for i, data in enumerate(f.data):
                try:
                    xy = values[data['name']]
                    f.data[i].x = xy['x']
                    f.data[i].y = xy['y']
                except KeyError:
                    pass

                if data['name'] == 'grid':
                    lines += 1
                    f.data[i].x = tgrid[lines].x
                    f.data[i].y = tgrid[lines].y

    ctrls = interactive(update_step, w11=w11, w21=w21, w12=w12, w22=w22, step=step_slider)
    dials = VBox([HBox([VBox([w11, w21]), VBox([w12, w22])]), step_slider])
    return (f, dials)

if __name__ == '__main__':
    transf = np.array([[-1, -1], [-1, .4]])
    eo = plotEigen(transf)
    vb = VBox(build_figure(eo), layout={'align_items': 'center'})
