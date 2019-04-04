import numpy as np
import plotly.graph_objs as go
from copy import deepcopy
from ipywidgets import VBox, interactive, FloatSlider, Checkbox, Dropdown
from sklearn.preprocessing import MinMaxScaler, Normalizer, StandardScaler
from sklearn.decomposition import PCA
from scipy.stats import chi2
from deepreplay.plot import build_2d_grid

def data(scaling=(3, 1), rotation=((.7, -.7), (.7, .7))):
    np.random.seed(42)
    X = np.random.randn(200, 2)
    X *= np.array(scaling)
    rotation = np.array(rotation)
    X = np.matmul(X, rotation.T)
    return X

def calc_coord(prob):
    return chi2.ppf(prob, 2)

def calc_fences(v, k=1.5):
    q1, q3 = np.percentile(v, q=[25, 75])
    iqr = q3 - q1
    lfence = q1 - (k * iqr)
    ufence = q3 + (k * iqr)
    return lfence, ufence

def fence_trace(fence, axis):
    v = [fence, fence]
    if axis == 'x':
        x = v
        y = [-10, 10]
    else:
        y = v
        x = [-10, 10]
    return go.Scatter(x=x, y=y, mode='lines', line={'color': 'red', 'dash': 'dash'}, showlegend=False, visible=False)

class plotScaling(object):
    def __init__(self, X, outlier=None):
        self.orig_X = X
        self.X = X
        self.n_features = X.shape[1]

        if outlier is not None:
            self.add_outlier(outlier)

        self.grid = build_2d_grid(xlim=[-10, 10], ylim=[-10, 10], n_lines=100, n_points=100)

        sts = StandardScaler(with_mean=True, with_std=True)
        sts.fit(X)
        Sinv = np.linalg.inv(np.cov(sts.transform(X).T))
        def calc_dist(v):
            return np.matmul(np.matmul(v, Sinv), v)
        mah_dist = np.apply_along_axis(func1d=calc_dist, axis=2, arr=self.grid)
        # norms = np.apply_along_axis(func1d=lambda v: np.linalg.norm(v, ord=2), axis=2, arr=self.grid)
        self.chi_surface = chi2.cdf(mah_dist, self.n_features)

        self.data, self.outlier = self.plot_data()
        self.contour = self.plot_contour()
        self.lfence1, self.ufence1, self.lfence2, self.ufence2 = self.plot_fences()
        self.circle = self.plot_probability(.991)

    @property
    def traces(self):
        return dict(data=self.data,
                    outlier=self.outlier,
                    contour=self.contour,
                    lfence1=self.lfence1,
                    ufence1=self.ufence1,
                    lfence2=self.lfence2,
                    ufence2=self.ufence2,
                    circle=self.circle)

    def add_outlier(self, outlier):
        self.outlier = np.array(outlier).reshape(-1, 2)
        self.X = np.concatenate([self.orig_X, self.outlier], axis=0)

    def plot_data(self):
        data = go.Scatter(x=self.X[:, 0], y=self.X[:, 1], mode='markers', showlegend=False)
        try:
            outlier = go.Scatter(x=self.outlier[:, 0], y=self.outlier[:, 1], mode='markers', marker={'color': 'red'}, showlegend=False)
        except AttributeError:
            outlier = go.Scatter(x=[], y=[], mode='markers', marker={'color': 'red'}, showlegend=False)
        return data, outlier

    def plot_fences(self):
        lfence1, ufence1 = calc_fences(self.X[:, 0])
        lfence2, ufence2 = calc_fences(self.X[:, 1])

        lfence1 = fence_trace(lfence1, 'x')
        ufence1 = fence_trace(ufence1, 'x')
        lfence2 = fence_trace(lfence2, 'y')
        ufence2 = fence_trace(ufence2, 'y')
        return lfence1, ufence1, lfence2, ufence2

    def plot_contour(self):
        contour = go.Contour(x=self.grid[:, 0, 0],
                             y=self.grid[0, :, 1],
                             z=self.chi_surface,
                             autocontour=False,
                             colorscale='Jet',
                             opacity=.5,
                             contours=dict(
                                start=0.,
                                end=1.,
                                size=.05,
                            ),)
        return contour

    def plot_probability(self, probability):
        points = self.grid.reshape(-1, 2)[((self.chi_surface >= (probability - .001)) & (self.chi_surface <= (probability + .0005))).reshape(-1),]
        circle = go.Scatter(x=points[:, 0], y=points[:, 1], mode='markers', marker={'color': 'black'}, opacity=.3, showlegend=False)
        return circle

def build_figure(sc_obj):
    traces = sc_obj.traces

    fig = go.Figure([traces['data'], traces['outlier'], traces['contour'], traces['lfence1'], traces['ufence1'], traces['lfence2'], traces['ufence2'], traces['circle']])
    f = go.FigureWidget(fig)
    f.data[1].visible = False
    f.data[2].visible = False
    f['layout']['xaxis'].range = [-10, 10]
    f['layout']['yaxis'].range = [-10, 10]
    #f['layout']['shapes'] = [traces['circle']]

    def update(method, outlier, fence1, fence2, chisq, prob):
        x = deepcopy(sc_obj.X)
        with f.batch_update():
            last = -1
            if outlier:
                last = None
            circle = sc_obj.plot_probability(prob)
            #if chisq:
                #coord = calc_coord(prob)
                #f['layout']['shapes'][0].update({'x0': -coord, 'y0': -coord, 'x1': coord, 'y1': coord})

            mms = MinMaxScaler(feature_range=(-5, 5))
            mms.fit(x[:last, :])
            sts = StandardScaler(with_mean=True, with_std=True)
            sts.fit(x[:last, :])
            nrs = Normalizer(norm='l2')
            nrs.fit(x[:last, :])

            axisrange = [-10, 10]
            if method == 'MinMax Scaling':
                x = mms.transform(x)
            elif method == 'Standard Scaling':
                x = sts.transform(x)
            elif method == 'Normalizing':
                x = nrs.transform(x)
                axisrange = [-2, 2]
            else:
                axisrange = [-10, 10]

            f['layout']['xaxis'].range = axisrange
            f['layout']['yaxis'].range = axisrange

            f.data[0].update({'x': x[:-1, 0], 'y': x[:-1, 1]})
            f.data[1].update({'x': x[-1:, 0], 'y': x[-1:, 1]})

            f.data[1].visible = outlier
            if method == 'Standard Scaling':
                f.data[2].visible = chisq
                f.data[7].visible = chisq
                f.data[7].update({'x': circle['x'], 'y': circle['y']})
                #f['layout']['shapes'][0].visible = chisq
            else:
                f.data[2].visible = False
                f.data[7].visible = False
                #f['layout']['shapes'][0].visible = False

            if fence1:
                lfence1, ufence1 = calc_fences(x[:, 0])
                lfence1 = fence_trace(lfence1, 'x')
                ufence1 = fence_trace(ufence1, 'x')
                f.data[3].visible = True
                f.data[4].visible = True
                f.data[3].update({'x': lfence1.x})
                f.data[4].update({'x': ufence1.x})
            else:
                f.data[3].visible = False
                f.data[4].visible = False

            if fence2:
                lfence2, ufence2 = calc_fences(x[:, 1])
                lfence2 = fence_trace(lfence2, 'y')
                ufence2 = fence_trace(ufence2, 'y')
                f.data[5].visible = True
                f.data[6].visible = True
                f.data[5].update({'y': lfence2.y})
                f.data[6].update({'y': ufence2.y})
            else:
                f.data[5].visible = False
                f.data[6].visible = False

    method = Dropdown(description='Method', options=['No Scaling', 'MinMax Scaling', 'Standard Scaling', 'Normalizing'], value='No Scaling')
    inc_outlier = Checkbox(description='Include Outlier', value=False)
    fence1 = Checkbox(description='Tukey\'s fences (horizontal)', value=False)
    fence2 = Checkbox(description='Tukey\'s fences (vertical) ', value=False)
    inc_chisq = Checkbox(description='ChiSq. Prob. for L2 Norm', value=False)
    prob = FloatSlider(description='Probability', value=.991, min=.991, max=.999, step=.001, readout_format='.3f',)

    return (f, interactive(update, method=method, outlier=inc_outlier, fence1=fence1, fence2=fence2, chisq=inc_chisq, prob=prob))

if __name__ == '__main__':
    X = data()
    mysc = plotScaling(X, outlier=(-9, 6))
    vb = VBox(build_figure(mysc), layout={'align_items': 'center'})
