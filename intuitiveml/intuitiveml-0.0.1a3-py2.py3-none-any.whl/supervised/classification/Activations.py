import plotly.graph_objs as go
from ipywidgets import VBox, FloatSlider, HBox, Dropdown, interactive
import numpy as np
from deepreplay.plot import build_2d_grid
from deepreplay.datasets.parabola import load_data

def transf_grid(grid, transf):
    return np.dot(grid, transf.T)

def shift_grid(grid, biases):
    return grid + biases

def sigmoid(z):
    return 1. / (1. + np.exp(-z))

def tanh(z):
    return (1. - np.exp(-2.*z)) / (1. + np.exp(-2.*z))

def relu(z):
    return np.maximum(0., z)

def activate(z, func='linear'):
    if func == 'linear':
        return z
    elif func == 'sigmoid':
        return sigmoid(z)
    elif func == 'tanh':
        return tanh(z)
    elif func == 'relu':
        return relu(z)

def combine(grid, transf, biases, activation):
    return activate(shift_grid(transf_grid(grid, transf), biases), activation)

def boundary(weights, bias, x1=(-1, 1)):
    num = weights[1]
    if num == 0:
        num = .1
    return [(-bias-weights[0]*v)/num for v in x1]

class plotActivations(object):
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.grid = build_2d_grid([-1, 1], [-1, 1])
        self.pos = X[y.squeeze() == 1]
        self.neg = X[y.squeeze() == 0]

        transf = np.array([[1, 0], [0, 1]])
        biases = [0, 0]
        activation = 'linear'
        self.transform(transf, biases, activation)
        self.bound_trace = self.boundary_trace([0, 1], 0)

    @property
    def traces(self):
        return dict(grid=self.grid_traces,
                    pos=self.pos_trace,
                    neg=self.neg_trace,
                    bound=self.bound_trace)

    def build_trace(self, X, color):
        return go.Scatter(x=X[:, 0], y=X[:, 1], name=color, mode='markers', marker={'color': color, 'opacity': .2})

    def build_grid_traces(self, grid):
        grid_lines = [go.Scatter(x=line[:, 0], y=line[:, 1], name='grid', mode='lines', showlegend=False, line={'color': 'black', 'width': 1})
                      for line in grid]
        return grid_lines

    def transform(self, transf, biases, activation):
        self.new_grid = combine(self.grid, transf, biases, activation)
        self.xrange = [np.minimum(-1, self.new_grid[:, :, 0].min()) -.05, np.maximum(1, self.new_grid[:, :, 0].max()) + .05]
        self.yrange = [np.minimum(-1, self.new_grid[:, :, 1].min()) -.05, np.maximum(1, self.new_grid[:, :, 1].max()) + .05]

        self.grid_traces = self.build_grid_traces(self.new_grid)
        self.pos_trace = self.build_trace(combine(self.pos, transf, biases, activation), 'green')
        self.neg_trace = self.build_trace(combine(self.neg, transf, biases, activation), 'blue')

    def boundary_trace(self, weights, bias):
        return go.Scatter(x=[-1, 1], y=boundary(weights, bias), name='boundary', mode='lines', line={'color': 'black', 'width': 2, 'dash': 'dash'})

def build_figure(act_obj):
    traces = act_obj.traces
    fig = go.Figure(traces['grid'] + [traces['pos'], traces['neg'], traces['bound']])
    f = go.FigureWidget(fig)

    f['layout']['xaxis'].range = act_obj.xrange
    f['layout']['yaxis'].range = act_obj.yrange
    f['layout']['xaxis'].zeroline = False
    f['layout']['yaxis'].zeroline = False
    f['layout'].width = 600
    f['layout'].height = 500

    w11 = FloatSlider(description='w11', value=1, min=-3, max=3, step=.1)
    w21 = FloatSlider(description='w21', value=0, min=-3, max=3, step=.1)

    w12 = FloatSlider(description='w12', value=0, min=-3, max=3, step=.1)
    w22 = FloatSlider(description='w22', value=1, min=-3, max=3, step=.1)

    b11 = FloatSlider(description='b11', value=0, min=-3, max=3, step=.1)
    b12 = FloatSlider(description='b12', value=0, min=-3, max=3, step=.1)

    activ = Dropdown(description='Activation', options=['linear', 'sigmoid', 'tanh', 'relu'], value='linear')

    w13 = FloatSlider(description='w13', value=0, min=-3, max=3, step=.1)
    w23 = FloatSlider(description='w23', value=1, min=-3, max=3, step=.1)

    b13 = FloatSlider(description='b23', value=0, min=-3, max=3, step=.1)

    def update(w11, w12, w21, w22, b11, b12, activ, w13, w23, b13):
        transf = np.array([[w11, w12], [w21, w22]])
        biases = [b11, b12]

        act_obj.transform(transf, biases, activ)
        traces = act_obj.traces

        with f.batch_update():
            f['layout']['xaxis'].range = act_obj.xrange
            f['layout']['yaxis'].range = act_obj.yrange

            for i, t in enumerate(traces['grid']):
                f.data[i].x = t.x
                f.data[i].y = t.y
            f.data[-3].x = traces['pos'].x
            f.data[-3].y = traces['pos'].y
            f.data[-2].x = traces['neg'].x
            f.data[-2].y = traces['neg'].y
            f.data[-1].x = act_obj.xrange
            f.data[-1].y = boundary([w13, w23], b13, act_obj.xrange)

    ctrls = interactive(update, w11=w11, w12=w12, w21=w21, w22=w22, b11=b11, b12=b12, activ=activ, w13=w13, w23=w23, b13=b13)
    dials = VBox([HBox([VBox([w11, w21]), VBox([w12, w22]), VBox([b11, b12])]), activ,
                  HBox([VBox([w13, w23]), b13], layout={'align_items': 'center'})],
                layout={'align_items': 'center'})

    return (f, dials)

if __name__ == '__main__':
    X, y = load_data()
    myact = plotActivations(X, y)
    vb = VBox(build_figure(myact), layout={'align_items': 'center'})