import numpy as np
import plotly.graph_objs as go
from plotly.tools import make_subplots
from ipywidgets import VBox, interactive, IntSlider

def data(n_points=10):
    np.random.seed(238)
    x1 = np.random.randn(n_points * 2)
    X = np.array([np.array([x, y]) for x, y in zip(x1[:n_points], x1[n_points:])])
    y = np.ones(n_points)
    return X, y

class plotInfo(object):
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.n = len(y)
        self.green, self.red = self.plot_data()
        self.dist = self.plot_dist()
        self.gini, self.sel_gini = self.plot_gini()
        self.entropy, self.sel_entropy = self.plot_entropy()

    @property
    def traces(self):
        return dict(green=self.green,
                    red=self.red,
                    dist=self.dist,
                    gini=self.gini,
                    sel_gini=self.sel_gini,
                    entropy=self.entropy,
                    sel_entropy=self.sel_entropy)

    def plot_data(self):
        green = go.Scatter(x=self.X[self.y==1, 0], y=self.X[self.y==1, 1],
                           showlegend=False, mode='markers', marker={'color': 'green', 'size': 20, 'line': {'color': 'black', 'width': 2}})
        red = go.Scatter(x=self.X[self.y==0, 0], y=self.X[self.y==0, 1],
                         showlegend=False, mode='markers', marker={'color': 'red', 'size': 20, 'line': {'color': 'black', 'width': 2}})
        return green, red

    def plot_dist(self):
        dist = go.Bar(x=['Red', 'Green'], y=[(self.y==0).sum()/self.n, (self.y==1).sum()/self.n],
                      showlegend=False, marker={'color': ['red', 'green'], 'line': {'color': 'black', 'width': 2}})
        return dist

    def plot_gini(self):
        pred = np.linspace(0, 1, self.n + 1)
        self.ginies = (pred * pred[::-1]) * 2
        gin = go.Scatter(x=np.linspace(0, self.n, self.n + 1), y=self.ginies,
                         showlegend=False, marker={'size': 1}, line={'color': 'black', 'width': 2})
        sel_gin = go.Scatter(x=[np.linspace(0, self.n, self.n + 1)[(self.y==0).sum()]], y=[self.ginies[(self.y==0).sum()]],
                             showlegend=False, mode='markers', marker={'size': 12, 'symbol': 'star', 'color': 'red'})
        return gin, sel_gin

    def plot_entropy(self):
        pred = np.linspace(0, 1, self.n + 1)
        logpred = np.concatenate([[0.], np.log2(pred[1:])])
        self.entropies = (-logpred * pred) + (-logpred * pred)[::-1]
        ent = go.Scatter(x=np.linspace(0, self.n, self.n + 1), y=self.entropies,
                         showlegend=False, marker={'size': 1}, line={'color': 'black', 'width': 2})
        sel_ent = go.Scatter(x=[np.linspace(0, self.n, self.n + 1)[(self.y==0).sum()]], y=[self.entropies[(self.y==0).sum()]],
                             showlegend=False, mode='markers', marker={'size': 12, 'symbol': 'star', 'color': 'red'})
        return ent, sel_ent

def build_figure(info_obj):
    traces = info_obj.traces
    fig = make_subplots(2, 2, subplot_titles=('Data', 'Distribution', 'Entropy', 'Gini'), print_grid=False)

    fig.append_trace(traces['green'], 1, 1)
    fig.append_trace(traces['red'], 1, 1)
    fig.append_trace(traces['dist'], 1, 2)
    fig.append_trace(traces['entropy'], 2, 1)
    fig.append_trace(traces['sel_entropy'], 2, 1)

    fig.append_trace(traces['gini'], 2, 2)
    fig.append_trace(traces['sel_gini'], 2, 2)

    f = go.FigureWidget(fig)

    f['layout']['xaxis'].visible = False
    f['layout']['yaxis'].visible = False
    f['layout']['yaxis'].range = [-4, 4]
    f['layout']['yaxis2'].range = [0, 1.01]
    f['layout']['yaxis3'].range = [0, 1.1]
    f['layout']['xaxis3'].range = [-.1, info_obj.n + .1]
    f['layout']['xaxis3'].title = '# Red Balls'
    f['layout']['yaxis4'].range = [-.1, 1.1]
    f['layout']['xaxis4'].range = [-.1, info_obj.n + .1]
    f['layout']['xaxis4'].title = '# Red Balls'

    def update(idx):
        y = np.ones(info_obj.n)
        y[:idx] = 0

        with f.batch_update():
            f.data[0].update({'x': info_obj.X[y==1, 0], 'y': info_obj.X[y==1, 1]})
            f.data[1].update({'x': info_obj.X[y==0, 0], 'y': info_obj.X[y==0, 1]})
            f.data[2].update({'y': [(y==0).sum()/info_obj.n, (y==1).sum()/info_obj.n]})
            f.data[4].update({'x': [np.linspace(0, info_obj.n, info_obj.n + 1)[(y==0).sum()]],
                              'y': [info_obj.entropies[(y==0).sum()]]})
            f.data[6].update({'x': [np.linspace(0, info_obj.n, info_obj.n + 1)[(y==0).sum()]],
                              'y': [info_obj.ginies[(y==0).sum()]]})

    idx = IntSlider(description='Red Balls', value=2, min=0, max=info_obj.n, step=1)
    return (f, interactive(update, idx=idx))

if __name__ == '__main__':
    X, y = data()
    myinfo = plotInfo(X, y)
    vb = VBox(build_figure(myinfo), layout={'align_items': 'center'})