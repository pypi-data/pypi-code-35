import numpy as np
import plotly.graph_objs as go
from plotly.tools import make_subplots
from sklearn.svm import LinearSVC
from deepreplay.plot import build_2d_grid
from ipywidgets import VBox, interactive, FloatSlider, Checkbox, FloatLogSlider

def data():
    x = np.array([-2.8, -2.2, -1.8, -1.3, -.4, 0.7, 1.1, 1.3, 1.9, 2.5])
    y = np.array([0., 0., 0., 0., 0., 1., 1., 1., 1., 1.])
    return x, y

class plotSVM(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        self.b = np.array([0.])
        self.dim = 1
        if len(x.shape) > 1:
            self.dim = x.shape[1]
        if self.dim > 1:
            self.grid_lines = build_2d_grid(xlim=(self.x[:, 0].min(), self.x[:, 0].max()),
                                            ylim=(self.x[:, 1].min(), self.x[:, 1].max()),
                                            n_points=10)
        self.w = np.array([1.] * self.dim)
        self.is_soft = True
        self.C = 1.0
        self.fit()
        self.green, self.red = self.plot_data()
        self.update_decision()

    @property
    def traces(self):
        return dict(green=self.green,
                    red=self.red,
                    decision=self.decision,
                    hneg=self.hneg,
                    h0=self.h0,
                    hpos=self.hpos,
                    objective=self.objective,
                    violations=self.violations,
                    grid=self.grid)

    def set_decision(self, b, w, is_soft=True, C=1.0):
        self.b = np.array(b)
        self.w = np.array(w).reshape(1, -1)
        self.is_soft = is_soft
        self.C = C
        self.update_decision()

    def fit(self, is_soft=None):
        if is_soft is None:
            is_soft = self.is_soft
        C = self.C
        if not is_soft:
            C = np.inf

        self.svc = LinearSVC(fit_intercept=True, C=C, loss='hinge')
        self.svc.fit(X=self.x.reshape(-1, self.dim), y=self.y)
        if self.dim > 1:
            self.update_decision()

    def update_decision(self):
        self.grid = self.plot_grid()
        self.decision = self.plot_decision()
        self.hneg, self.h0, self.hpos = self.plot_hs()
        self.hinge_loss = self.calc_loss()
        self.norm, self.slack = self.calc_cost()
        self.objective = self.plot_objective()
        self.violations = self.plot_violations()

    def calc_loss(self):
        t = -1 * (self.y==0) + (self.y==1)

        wtxb = (np.matmul(self.w.T, self.x.reshape(self.dim, -1)) + self.b).ravel()
        restriction = wtxb * t

        hinge_loss = np.maximum(0, 1 - restriction)
        return hinge_loss

    def calc_cost(self):
        norm = np.dot(self.w.T, self.w).ravel()[0] / 2
        slack = 0
        if self.is_soft:
            slack = self.hinge_loss.sum()
            if slack > 0:
                    slack *= self.C
        return norm, slack

    def vector(self, y, h=0):
        b = self.svc.intercept_[0]
        w1, w2 = self.svc.coef_[0]
        return (h - b - w2 * y) / w1

    def plot_objective(self):
        trace_objective = go.Bar(x=['weights', 'slack'], y=[self.norm, self.slack], name='Cost', marker={'color': 'gray'})
        return trace_objective

    def plot_violations(self):
        trace_violations = go.Bar(x=np.arange(len(self.x)), y=self.hinge_loss, name='Loss', marker={'color': ['green' if v else 'red' for v in self.y]})
        return trace_violations

    def plot_data(self):
        positive_x = self.x[self.y==1]
        negative_x = self.x[self.y==0]
        if self.dim == 1:
            trace_green = go.Scatter(x=positive_x, y=np.zeros_like(positive_x), name='Green', mode='markers', marker={'color': 'green', 'size': 12, 'line': {'color': 'black', 'width': 2}})
            trace_red = go.Scatter(x=negative_x, y=np.zeros_like(negative_x), name='Red', mode='markers', marker={'color': 'red', 'size': 12, 'line': {'color': 'black', 'width': 2}})
        else:
            trace_green = go.Scatter3d(x=positive_x[:, 0],
                                       y=positive_x[:, 1],
                                       z=np.zeros_like(positive_x[:, 0]),
                                       name='Green', mode='markers', marker={'size': 5, 'color': 'green'})
            trace_red = go.Scatter3d(x=negative_x[:, 0],
                                     y=negative_x[:, 1],
                                     z=np.zeros_like(negative_x[:, 0]),
                                     name='Red', mode='markers', marker={'size': 5, 'color': 'red'})
        return trace_green, trace_red

    def plot_grid(self):
        trace_grid = None
        if self.dim > 1:
            trace_grid = [go.Scatter3d(x=line[:, 0],
                                       y=line[:, 1],
                                       z=np.zeros_like(line[:, 0]),
                                       name='grid', mode='lines', line={'color': 'black'}, showlegend=False) for line in self.grid_lines]
        return trace_grid

    def plot_decision(self):
        if self.dim == 1:
            x = np.array(sorted(self.x))
            y = self.w[0] * x + self.b
            trace_decision = go.Scatter(x=x, y=y, name='Decision', mode='lines', line={'color': 'black'})
        else:
            trace_decision = [go.Scatter3d(x=line[:, 0],
                                           y=line[:, 1],
                                           z=(np.matmul(line, self.svc.coef_.T) + self.svc.intercept_).ravel(),
                                           name='plane', mode='lines', line={'color': 'orange'}, showlegend=False) for line in self.grid_lines]
        return trace_decision

    def plot_hs(self):
        if self.dim == 1:
            hs = np.array([(v - self.b) / self.w[0] for v in [-1., 0., 1.]]).ravel()
            trace_hneg = go.Scatter(x=[hs[0], hs[0]], y=[-1.0, 0.], name='h=-1', mode='lines', line={'color': 'red', 'dash': 'dash'})
            trace_h0 = go.Scatter(x=[hs[1], hs[1]], y=[-.5, .5], name='h=0', mode='lines', line={'color': 'black'})
            trace_hpos = go.Scatter(x=[hs[2], hs[2]], y=[0., 1.0], name='h=1', mode='lines', line={'color': 'green', 'dash': 'dash'})
        else:
            trace_h0 = go.Scatter3d(x=self.vector(self.grid_lines[0, :, 1], h=0),
                                    y=self.grid_lines[0, :, 1],
                                    z=np.zeros_like(self.grid_lines[0, :, 1]),
                                    name='Support Vector', mode='lines', line={'color': 'black', 'width': 3})
            trace_hneg = [go.Scatter3d(x=self.vector(self.grid_lines[0, :, 1], h=-1),
                                      y=self.grid_lines[0, :, 1],
                                      z=np.zeros_like(self.grid_lines[0, :, 1]),
                                      name='Margin', mode='lines', line={'color': 'red', 'width': 5, 'dash': 'dash'}),
                          go.Scatter3d(x=self.vector(self.grid_lines[0, :, 1], h=-1),
                                       y=self.grid_lines[0, :, 1],
                                       z=-1*np.ones_like(self.grid_lines[0, :, 1]),
                                       name='plane', showlegend=False, mode='lines', line={'color': 'red', 'width': 3})]
            trace_hpos = [go.Scatter3d(x=self.vector(self.grid_lines[0, :, 1], h=1),
                                      y=self.grid_lines[0, :, 1],
                                      z=np.zeros_like(self.grid_lines[0, :, 1]),
                                      name='Margin', mode='lines', line={'color': 'green', 'width': 5, 'dash': 'dash'}),
                          go.Scatter3d(x=self.vector(self.grid_lines[0, :, 1], h=1),
                                       y=self.grid_lines[0, :, 1],
                                       z=np.ones_like(self.grid_lines[0, :, 1]), name='plane', showlegend=False, mode='lines', line={'color': 'green', 'width': 3})]

        return trace_hneg, trace_h0, trace_hpos

def build_figure(svm_obj):
    traces = svm_obj.traces

    fig = make_subplots(2, 3, specs=[[{'colspan': 2, 'rowspan': 2}, None, {}],
                                     [None, None, {}]], subplot_titles=('Data', 'Loss/Slack', 'Costs'), print_grid=False)
    fig.append_trace(traces['green'], 1, 1)
    fig.append_trace(traces['red'], 1, 1)
    fig.append_trace(traces['decision'], 1, 1)
    fig.append_trace(traces['hneg'], 1, 1)
    fig.append_trace(traces['h0'], 1, 1)
    fig.append_trace(traces['hpos'], 1, 1)
    fig.append_trace(traces['violations'], 1, 3)
    fig.append_trace(traces['objective'], 2, 3)

    f = go.FigureWidget(fig)
    f['layout']['yaxis'].range = [-3, 3]
    f['layout']['xaxis'].range = [-3, 3]
    f['layout']['yaxis2'].range = [0, 1]
    f['layout']['yaxis3'].update({'range': [-2, 3], 'type': 'log'})

    names = ['positive', 'negative', 'decision', 'h-1', 'h0', 'h1', 'violations', 'objective']

    def update(b, w, soft, C):
        if w == 0:
            w = 0.01
        svm_obj.set_decision(b=b, w=w, is_soft=soft, C=C)
        traces = svm_obj.traces

        values = {'decision': {'y': traces['decision'].y, 'x': traces['decision'].x},
                  'h-1': {'x': traces['hneg'].x},
                  'h0': {'x': traces['h0'].x},
                  'h1': {'x': traces['hpos'].x},
                  'violations': {'y': traces['violations'].y},
                  'objective': {'y': traces['objective'].y}}
        with f.batch_update():
            f['layout']['annotations'][1]['text'] = 'Loss/Slack = {:.2f}'.format(traces['violations'].y.sum())
            f['layout']['annotations'][2]['text'] = 'Costs = {:.2f}'.format(sum(traces['objective'].y))
            for i, data in enumerate(f.data):
                try:
                    if values[names[i]]['y'] is not None:
                        data.y = values[names[i]]['y']
                except KeyError:
                    pass

                try:
                    if values[names[i]]['x'] is not None:
                        data.x = values[names[i]]['x']
                except KeyError:
                    pass

    intercept = FloatSlider(description=r'$b$', value=0.0, min=-1.0, max=1.0, step=.1)
    w1 = FloatSlider(description=r'$w_1$', value=1.0, min=-5.0, max=5.0, step=.1)
    soft = Checkbox(description='Use Soft Margin', value=False)
    multiplier = FloatLogSlider(description='C', value=1.0, min=-3., max=2., step=1.)

    return (f, interactive(update, b=intercept, w=w1, soft=soft, C=multiplier))

def build_3dfigure(svm_obj):
    svm_obj.fit(is_soft=False)
    traces = svm_obj.traces

    fig2 = go.Figure([traces['green'], traces['red'], traces['h0']] + traces['hneg'] + traces['hpos'] + traces['decision'] + traces['grid'])

    f2 = go.FigureWidget(fig2)

    f2['layout']['scene']['xaxis'].update({'visible': False, 'range': (svm_obj.x[:, 0].min()-.01, svm_obj.x[:, 0].max()+.01)})
    f2['layout']['scene']['yaxis'].update({'visible': False, 'range': (svm_obj.x[:, 1].min()-.01, svm_obj.x[:, 1].max()+.01)})
    f2['layout']['scene']['zaxis'].update({'visible': True, 'range': (-2, 2)})

    def update2(plane):
        with f2.batch_update():
            for data in f2.data:
                if data.name == 'plane':
                    data.visible = plane

    plane = Checkbox(description='Show Plane', value=False)
    return (f2, interactive(update2, plane=plane))

if __name__ == '__main__':
    x, y = data()
    mysvm = plotSVM(x, y)
    vb1 = VBox(build_figure(mysvm), layout={'align_items': 'center'})

    from sklearn import datasets
    iris = datasets.load_iris()

    y = iris['target']
    x = iris['data'][y != 2][:, (2, 3)]
    y = y[y != 2]

    # quadratic
    #x = np.array([-2.8, -2.2, -1.8, -1.3, -.4, 0.7, 1.1, 1.3, 1.9, 2.5])
    #x2 = x ** 2
    #x = np.concatenate([x.reshape(-1, 1), x2.reshape(-1, 1)], axis=1)
    #y = np.array([0., 0., 0., 0., 0., 1., 1., 1., 0., 0.])
    mysvm2 = plotSVM(x=x, y=y)
    mysvm2.fit(is_soft=False)
    vb2 = VBox(build_3dfigure(mysvm2), layout={'align_items': 'center'})