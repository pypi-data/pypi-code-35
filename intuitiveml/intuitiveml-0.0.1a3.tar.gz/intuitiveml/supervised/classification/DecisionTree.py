import graphviz
import numpy as np
import plotly.graph_objs as go
from plotly.tools import make_subplots
from copy import deepcopy
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.dummy import DummyRegressor
from sklearn import tree
from ipywidgets import VBox, HBox, interactive, IntSlider

def data(imbalanced=False):
    if not imbalanced:
        x = np.array([-2.2, -1.4, -.8, .2, .4, .8, 1.2, 2.2, 2.9, 4.6])
        y = np.array([0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    else:
        x = np.array([-2.2, -2.0, -1.7, -1.3, -1.1, -.8, .2, .4, .8, 1.2, 2.2, 2.5, 2.7, 2.9, 3.3, 3.9, 4.2, 4.6])
        y = np.array([0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    return x, y

class plotDecision(object):
    def __init__(self, x, y, midpoints=None, idx_mid=0, xrange=None, level=0):
        self.is_classifier = True
        if len(np.unique(y)) > 2:
            self.is_classifier = False
        self.orig_x = x
        self.orig_y = y
        self.x = x
        self.y = y
        self.level = level
        if xrange is None:
            self.x_start, self.x_end = np.floor(np.min(self.x)), np.ceil(np.max(self.x))
        else:
            self.x_start, self.x_end = xrange
        if midpoints is None:
            self.midpoints = plotDecision.calc_midpoints(self.x)
        else:
            self.midpoints = midpoints
        self.axis, self.red, self.green = self.plot_data()
        self.mid = self.plot_midpoints()
        self.idx_mid = idx_mid
        self.set_split(self.idx_mid)
        self.ensemble(n_trees=1)
        self.boosted_data = None
        self.boosted_trees = None
        self.boosted_residuals = None

    @staticmethod
    def calc_midpoints(x):
        midpoints = (x[1:] + x[:-1])/2
        return np.concatenate([[x[0] - .25], midpoints, [x[-1] + .25]])

    def fit(self, max_depth=None):
        if self.is_classifier:
            dtc = DecisionTreeClassifier(criterion='entropy', max_depth=max_depth)
        else:
            dtc = DecisionTreeRegressor(max_depth=max_depth)
        dtc.fit(X=self.x.reshape(-1, 1), y=self.y)
        return dtc

    def plot_tree(self, max_depth=None):
        dtc = self.fit(max_depth)
        class_names = None
        if self.is_classifier:
            class_names = ['Red', 'Green']
        dot_data = tree.export_graphviz(dtc, out_file=None,
                         feature_names=['X'],
                         class_names=class_names,
                         filled=True, rounded=True,
                         special_characters=True)
        graph = graphviz.Source(dot_data)
        return graph

    def predict(self, x, max_depth=None):
        dtc = self.fit(max_depth)
        if self.is_classifier:
            return dtc.predict_proba(x.reshape(-1, 1))
        else:
            return dtc.predict(x.reshape(-1, 1))

    def bootstrap(self, ratio=.8, seed=None, replace=True):
        if seed is not None:
            np.random.seed(seed)
        N = len(self.orig_x)
        if ratio == 1.0 and not replace:
            self.x = self.orig_x
            self.y = self.orig_y
        else:
            idx = np.random.choice(np.arange(N), size=int(N * ratio), replace=replace)
            self.x = np.array([x for x, y in sorted(zip(self.orig_x[idx], self.orig_y[idx]))])
            self.y = np.array([y for x, y in sorted(zip(self.orig_x[idx], self.orig_y[idx]))])

        self.midpoints = plotDecision.calc_midpoints(self.x)
        self.axis, self.red, self.green = self.plot_data()
        self.mid = self.plot_midpoints()
        self.idx_mid = 0
        self.set_split(self.idx_mid)

    def ensemble(self, n_trees=5, ratio=1.0, max_depth=None, seed=42):
        trees = []
        yhat_neg = []
        yhat_pos = []
        if self.is_classifier:
            xspace = np.arange(self.x_start, self.x_end, .05)
        else:
            xspace = np.linspace(self.x_start, self.x_end, 1000)
        replace = True
        if n_trees == 0:
            n_trees = 1
            replace = False
        for i in range(n_trees):
            np.random.seed(seed * (i + 1))
            self.bootstrap(ratio=ratio, replace=replace)
            trees.append(self.plot_tree(max_depth))
            dtc = self.fit(max_depth)
            if self.is_classifier:
                if self.y.sum() == len(self.y):
                    yhat_pos.append(np.ones_like(xspace))
                    yhat_neg.append(np.zeros_like(xspace))
                elif self.y.sum() == 0:
                    yhat_pos.append(np.zeros_like(xspace))
                    yhat_neg.append(np.ones_like(xspace))
                else:
                    yhat_neg.append(dtc.predict_proba(xspace.reshape(-1, 1))[:, 0])
                    yhat_pos.append(dtc.predict_proba(xspace.reshape(-1, 1))[:, 1])
            else:
                yhat_pos.append(dtc.predict(xspace.reshape(-1, 1)))

        self.n_trees = n_trees
        self.trees = trees
        self.ensemble_depth = max_depth
        if self.is_classifier:
            self.ensemble_pos = go.Bar(x=xspace, y=np.array(yhat_pos).mean(axis=0),
                              width=.05, marker={'opacity': .3, 'color': 'green', 'line': {'color': 'green'}})
            self.ensemble_neg = go.Bar(x=xspace, y=np.array(yhat_neg).mean(axis=0),
                                       base=np.array(yhat_pos).mean(axis=0),
                             width=.05, marker={'opacity': .3, 'color': 'red', 'line': {'color': 'red'}})
        else:
            self.ensemble_pos = go.Scatter(x=xspace, y=np.array(yhat_pos).mean(axis=0),
                                          mode='lines', line={'color': 'black', 'dash': 'dash', 'width': 2})
            self.ensemble_neg = None
        self.bootstrap(ratio=1.0, replace=False)
        return

    def calc_residual(self, previous_residual=None, previous_delta=None, max_depth=None):
        if previous_residual is None:
            residual = deepcopy(self.y)
        else:
            residual = deepcopy(previous_residual)

        if previous_delta is None:
            delta = np.zeros_like(self.y)
            pred = self.y.mean()
        else:
            delta = deepcopy(previous_delta)
            pred = self.predict(self.x, max_depth)
        delta += pred
        residual -= pred

        return residual, delta

    def boost(self, n_trees=3, max_depth=1):
        if n_trees > 6:
            n_trees = 6
        trees = []
        residuals = []
        deltas = []
        models = []
        residual, delta = self.calc_residual(max_depth=max_depth)
        residuals.append(residual)
        deltas.append(delta)
        models.append(DummyRegressor(strategy='mean').fit(self.x.reshape(-1, 1), self.y))
        trees.append(None)
        for i in range(n_trees):
            next_tree = plotDecision(x=self.x, y=residual, level=i+1)
            model = next_tree.fit(max_depth)
            residual, delta = next_tree.calc_residual(residual, delta, max_depth)
            residuals.append(residual)
            deltas.append(delta)
            models.append(model)
            trees.append(next_tree.plot_tree(max_depth))
            if not np.any(residual):
                break

        self.trees = trees

        xspace = np.linspace(self.x_start, self.x_end, 1000)
        colors = ['gray', 'green', 'red', 'blue', 'orange', 'purple', 'brown']
        self.boosted_data = go.Scatter(x=self.x, y=self.y, mode='markers', name='Data', marker={'color': 'green', 'line':{'color': 'black', 'width': 2}})
        self.boosted_trees = [go.Scatter(x=xspace, y=model.predict(xspace.reshape(-1, 1)), line={'color': colors[i]}, name='Tree {}'.format(i), stackgroup='one')
                              for i, model in enumerate(models)]
        self.boosted_residuals = [go.Scatter(x=self.x, y=residual, name='Residual', line={'color': colors[i]})
                                  for i, residual in enumerate(residuals)]
        return

    @property
    def left_split(self):
        midpoints = self.midpoints[:self.idx_mid+1]
        if self.is_classifier:
            metric = self.entropies
        else:
            metric = self.mses
        if self.Ns[0] > 0 and metric[0] > 0:
            return plotDecision(self.left_points[0], self.left_points[1], midpoints=midpoints, xrange=(self.x_start, self.x_end), level=self.level + 1, idx_mid=len(midpoints)-1)
        else:
            return None

    @property
    def right_split(self):
        midpoints = self.midpoints[self.idx_mid:]
        if self.is_classifier:
            metric = self.entropies
        else:
            metric = self.mses
        if self.Ns[1] > 0 and metric[1] > 0:
            return plotDecision(self.right_points[0], self.right_points[1], midpoints=midpoints, xrange=(self.x_start, self.x_end), level=self.level + 1)
        else:
            return None

    @property
    def traces(self):
        return dict(axis=self.axis,
                    red=self.red,
                    green=self.green,
                    mid=self.mid,
                    split=self.split,
                    left=self.left,
                    right=self.right,
                    ens_neg=self.ensemble_neg,
                    ens_pos=self.ensemble_pos,
                    boosted_trees=self.boosted_trees,
                    boosted_data=self.boosted_data,
                    boosted_residuals=self.boosted_residuals)

    @staticmethod
    def calc_entropy(y):
        entropy = 0
        if len(y) > 0:
            prob_pos = np.array(y).mean()
            prob_neg = 1 - prob_pos
            for p in [prob_pos, prob_neg]:
                if p > 0:
                    entropy += -(p * np.log2(p))
        return entropy

    @staticmethod
    def calc_mse(y):
        mse = 0
        if len(y) > 0:
            y = np.array(y)
            mse = (y - y.mean()) ** 2
        return np.array(mse).reshape(1, -1).mean()

    @staticmethod
    def build_prob(y):
        prob_pos = prob_neg = 0
        if len(y) > 0:
            prob_pos = np.array(y).mean()
            prob_neg = 1 - prob_pos
        return go.Bar(x=['Red', 'Green'], y=[prob_neg, prob_pos],
                      marker={'color': ['red', 'green'], 'line':{'color': 'black', 'width': 1}})

    @staticmethod
    def build_se(y):
        x = []
        se = []
        if len(y) > 0:
            x = np.arange(len(y))
            y = np.array(y)
            se = (y - y.mean()) ** 2
        return go.Bar(x=x, y=se, marker={'color': 'red', 'line': {'color': 'black', 'width': 1}})

    def plot_data(self):
        if self.is_classifier:
            axis_trace = go.Scatter(x=np.array([self.x_start, self.x_end]),
                                    y=np.array([0., 0.]), mode='lines',
                                    marker={'color': 'black'})
            red_trace = go.Scatter(x=self.x[self.y==0], y=np.zeros_like(self.x[self.y==0]),
                                   mode='markers', marker={'size': 13, 'color': 'red', 'line': {'width': 2, 'color': 'black'}})
            green_trace = go.Scatter(x=self.x[self.y==1], y=np.zeros_like(self.x[self.y==1]),
                                     mode='markers', marker={'size': 13, 'color': 'green', 'line': {'width': 2, 'color': 'black'}})
        else:
            axis_trace = None
            red_trace = None
            green_trace = go.Scatter(x=self.x, y=self.y,
                                     mode='markers', marker={'size': 13, 'color': 'green', 'line': {'width': 2, 'color': 'black'}})
        return axis_trace, red_trace, green_trace

    def plot_midpoints(self):
        mid_trace = go.Scatter(x=self.midpoints, y=np.zeros_like(self.midpoints),
                               mode='markers', marker={'size': 5, 'color': 'black'})
        return mid_trace

    def set_split(self, idx_mid):
        if idx_mid >= len(self.midpoints):
            idx_mid = len(self.midpoints) - 1
        self.idx_mid = idx_mid
        self.left_points, self.right_points = self.make_split(self.idx_mid)
        self.Ns = len(self.left_points[0]), len(self.right_points[0])
        if self.is_classifier:
            self.entropies = plotDecision.calc_entropy(self.left_points[1]), plotDecision.calc_entropy(self.right_points[1])
            self.total_entropy = (self.entropies[0] * self.Ns[0] + self.entropies[1] * self.Ns[1]) / (self.Ns[0] + self.Ns[1])
        else:
            self.mses = plotDecision.calc_mse(self.left_points[1]), plotDecision.calc_mse(self.right_points[1])
            self.total_mse = (self.mses[0] * self.Ns[0] + self.mses[1] * self.Ns[1]) / (self.Ns[0] + self.Ns[1])
        self.split, self.left, self.right = self.plot_split_midpoint(self.idx_mid)

    def plot_split_midpoint(self, idx_mid):
        selmid_trace = go.Scatter(x=[self.midpoints[idx_mid]], y=[0],
                                  mode='markers', marker={'size': 12, 'color': 'yellow', 'symbol': 'star', 'line': {'color': 'black', 'width': 2}})
        if self.is_classifier:
            left_trace = plotDecision.build_prob(self.left_points[1])
            right_trace = plotDecision.build_prob(self.right_points[1])
        else:
            left_trace = plotDecision.build_se(self.left_points[1])
            right_trace = plotDecision.build_se(self.right_points[1])
        return selmid_trace, left_trace, right_trace

    def make_split(self, idx_mid):
        left_points = self.x < self.midpoints[idx_mid]
        right_points = self.x > self.midpoints[idx_mid]
        x_split = [self.x[left_points], self.x[right_points]]
        y_split = [self.y[left_points], self.y[right_points]]
        return (x_split[0], y_split[0]), (x_split[1], y_split[1])

def build_figure(dt_obj, width=900):
    if dt_obj is None:
        fig = make_subplots(1, 1, print_grid=False)
        f = go.FigureWidget(fig)
        f['layout']['xaxis'].visible = False
        f['layout']['yaxis'].visible = False
        f['layout'].autosize = False
        f['layout'].showlegend = False
        f['layout'].height = 500
        f['layout'].width = width
        return (f, )
    else:
        traces = dt_obj.traces
        fig = make_subplots(2, 2, specs=[[{'colspan': 2}, None],
                                         [{}, {}]], subplot_titles=('Data', 'Left', 'Right'), print_grid=False)

        if dt_obj.is_classifier:
            fig.append_trace(traces['axis'], 1, 1)
            fig.append_trace(traces['red'], 1, 1)
        fig.append_trace(traces['green'], 1, 1)
        fig.append_trace(traces['mid'], 1, 1)
        fig.append_trace(traces['split'], 1, 1)
        fig.append_trace(traces['left'], 2, 1)
        fig.append_trace(traces['right'], 2, 2)

        f = go.FigureWidget(fig)
        if dt_obj.is_classifier:
            f['layout']['yaxis'].range = [-.1, .1]
            f['layout']['yaxis'].visible = False
            f['layout']['yaxis2'].range = [-.01, 1.01]
            f['layout']['yaxis3'].range = [-.01, 1.01]
        else:
            f['layout']['xaxis2'].showticklabels = False
            f['layout']['xaxis3'].showticklabels = False
            ymax = np.ceil(np.concatenate([np.array(traces['left'].y), np.array(traces['right'].y)]).max())
            f['layout']['yaxis2'].range = [-.01, ymax]
            f['layout']['yaxis3'].range = [-.01, ymax]

        f['layout'].autosize = False
        f['layout'].showlegend = False
        f['layout'].height = 500
        f['layout'].width = width

        if dt_obj.is_classifier:
            names = ['axis', 'red', 'green', 'mid', 'split', 'left', 'right']
        else:
            names = ['green', 'mid', 'split', 'left', 'right']

        def update(split):
            dt_obj.set_split(split)
            traces = dt_obj.traces
            values = {'left': {'y': traces['left'].y, 'x': traces['left'].x},
                      'right': {'y': traces['right'].y, 'x': traces['right'].x},
                      'split': {'x': traces['split'].x}}
            with f.batch_update():
                if dt_obj.is_classifier:
                    name = 'Entropy'
                    metrics = dt_obj.entropies
                    total = dt_obj.total_entropy
                else:
                    name = 'MSE'
                    metrics = dt_obj.mses
                    total = dt_obj.total_mse

                f['layout']['annotations'][0]['text'] = 'Split at {:.2f} - {} After: {:.4f}'.format(dt_obj.midpoints[dt_obj.idx_mid], name, total)
                f['layout']['xaxis2'].title = 'N_left = {} - {}: {:.4f}'.format(dt_obj.Ns[0], name, metrics[0])
                f['layout']['xaxis3'].title = 'N_right = {} - {}: {:.4f}'.format(dt_obj.Ns[1], name, metrics[1])
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
                #for j, (n, m) in enumerate(zip(dt_obj.Ns, metrics)):
                #    if n == 0 or np.array(m).max() == 0:
                #        f['layout']['yaxis{}'.format(j + 2)].range = [-.01, 1.01]
                #    else:
                #        f['layout']['yaxis{}'.format(j + 2)].autorange = True

        split = IntSlider(description='Split', value=dt_obj.idx_mid, min=0, max=len(dt_obj.midpoints)-1, step=1)

    return (f, interactive(update, split=split))

def build_figure_prob(dt_obj):
    dt_obj.ensemble(n_trees=0)
    traces = dt_obj.traces

    sfig = make_subplots(1, 1, subplot_titles=('Decision Tree',), print_grid=False)

    sfig.append_trace(traces['axis'], 1, 1)
    sfig.append_trace(traces['red'], 1, 1)
    sfig.append_trace(traces['green'], 1, 1)
    sfig.append_trace(traces['mid'], 1, 1)
    sfig.append_trace(traces['ens_neg'], 1, 1)
    sfig.append_trace(traces['ens_pos'], 1, 1)

    for i in range(4):
        sfig.data[i]['y'] += .5

    sf = go.FigureWidget(sfig)
    sf['layout'].showlegend = False
    sf['layout']['xaxis']['title'] = 'X'
    sf['layout']['yaxis']['title'] = 'Probability'
    sf['layout']['barmode'] = 'overlay'

    def update(max_depth):
        dt_obj.ensemble(n_trees=0, max_depth=max_depth)
        traces = dt_obj.traces
        with sf.batch_update():
            sf.data[4].x = traces['ens_neg'].x
            sf.data[4].y = traces['ens_neg'].y
            sf.data[4].base = traces['ens_neg'].base
            sf.data[5].x = traces['ens_pos'].x
            sf.data[5].y = traces['ens_pos'].y

    depth = IntSlider(description='Max. Depth', value=3, min=1, max=3, step=1)
    return (sf, interactive(update, max_depth=depth))

def build_figure_reg(dt_obj):
    traces = dt_obj.traces

    fig = make_subplots(1, 1, subplot_titles=('Ensemble',), print_grid=False)

    fig.append_trace(traces['green'], 1, 1)
    fig.append_trace(traces['mid'], 1, 1)
    fig.append_trace(traces['ens_pos'], 1, 1)

    f = go.FigureWidget(fig)
    f['layout'].showlegend = False
    f['layout']['xaxis']['title'] = 'X'

    names = ['green', 'mid', 'ens_pos']

    def update(trees, depth):
        dt_obj.ensemble(n_trees=trees, max_depth=depth, ratio=1.0)
        traces = dt_obj.traces
        values = {'ens_pos': {'y': traces['ens_pos'].y, 'x': traces['ens_pos'].x},
                  'green': {'y': traces['green'].y, 'x': traces['green'].x},
                  'mid': {'y': traces['mid'].y, 'x': traces['mid'].x},}
        with f.batch_update():
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

    trees = IntSlider(description='Trees', value=0, min=0, max=20, step=1)
    depth = IntSlider(description='Max. Depth', value=3, min=1, max=3, step=1)

    return (f, interactive(update, trees=trees, depth=depth))

if __name__ == '__main__':
    x, y = data()
    mydt = plotDecision(x=x, y=y, idx_mid=0)
    vb = VBox(build_figure(mydt), layout={'align_items': 'center'})
    mydt.plot_tree(1)

    left1, right1 = mydt.left_split, mydt.right_split
    fl1 = build_figure(left1, width=450)
    fr1 = build_figure(right1, width=450)

    vb1 = HBox((VBox(fl1, layout={'align_items': 'center'}),
                VBox(fr1, layout={'align_items': 'center'})))
    mydt.plot_tree(2)

    left2, right2 = left1.left_split, left1.right_split
    fl1l2 = build_figure(left2, width=450)
    fl1r2 = build_figure(right2, width=450)

    vb2 = HBox((VBox(fl1l2, layout={'align_items': 'center'}),
                VBox(fl1r2, layout={'align_items': 'center'})))
    mydt.plot_tree(3)

    # Regression
    xreg = np.array([750., 800., 850., 900., 950.])
    yreg = np.array([1160., 1200., 1280., 1450., 2000.])
    mydtr = plotDecision(x=xreg, y=yreg)

    vb = VBox(build_figure_boost(mydtr), layout={'align_items': 'center'})
