import numpy as np
import plotly.graph_objs as go
from ipywidgets import VBox, interactive, IntSlider, FloatSlider, Checkbox
from scipy.spatial import distance_matrix
from sklearn.neighbors import KNeighborsClassifier
from deepreplay.plot import build_2d_grid
from intuitiveml.unsupervised.KMeans import get_colors, data

def colorscale(k):
    return list(map(list, list(zip(np.linspace(0, 1, k), get_colors(range(k))))))

def knn(X, y, new_sample, k):
    new_distances = distance_matrix(X, new_sample, p=2)
    neighbors = np.array(sorted(np.concatenate([new_distances, X, y.reshape(-1, 1)], axis=1), key=lambda r: r[0]))[:k, 1:]
    clusters = neighbors[:, 2].astype(np.int)
    neighbors = neighbors[:, :2]
    assignment = np.argmax(np.bincount(clusters))
    return neighbors, clusters, assignment

class plotKNN(object):
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.k = 5

        self.grid = build_2d_grid([0, 8], [-3, 5], n_lines=200, n_points=200)

        self.data = self.data_trace(X, get_colors(y))
        self.set_new_sample()
        self.set_k(self.k)

    @property
    def traces(self):
        return dict(data=self.data,
                    new_data=self.new_data,
                    contour=self.contour,
                    new_lines=self.new_lines)

    def set_k(self, k):
        self.k = k
        self.contour = self.contour_trace()
        self.new_data, self.new_lines = self.newdata_trace()

    def set_new_sample(self, new_sample=None):
        if new_sample is None:
            new_sample = self.X.mean(axis=0).reshape(1, -1)
        self.new_sample = new_sample
        self.new_data, self.new_lines = self.newdata_trace()

    def newdata_trace(self):
        new_data = self.data_trace(self.new_sample, 'black')
        neighbors, clusters, assignment = knn(self.X, self.y, self.new_sample, self.k)
        new_data['marker']['opacity'] = 1.
        new_data['marker']['color'] = get_colors([assignment])[0]

        new_lines = [go.Scatter(x=[self.new_sample[0, 0], v[0]],
                                y=[self.new_sample[0, 1], v[1]],
                                showlegend=False,
                                mode='lines',
                                line={'color': get_colors([c])[0], 'dash': 'dash'}) for v, c in zip(neighbors, clusters)]
        return new_data, new_lines

    def data_trace(self, c, colors):
        return go.Scatter(x=c[:, 0], y=c[:, 1], showlegend=False, mode='markers', marker={'opacity': .5, 'color': colors, 'size': 12, 'line': {'color': 'black', 'width': 2}})

    def contour_trace(self):
        self.clf = KNeighborsClassifier(self.k, weights='uniform')
        self.clf.fit(self.X, self.y)

        Z = self.clf.predict(np.c_[self.grid[:, :, 0].ravel(), self.grid[:, :, 1].ravel()]).reshape(200, 200)
        contour = go.Contour(x=self.grid[:, 0, 0],
                             y=self.grid[0, :, 1],
                             z=Z.T,
                             showscale=False,
                             colorscale=colorscale(len(np.unique(self.y))),
                             autocontour=False,
                             opacity=.3)
        return contour

def build_figure(k_obj):
    traces = k_obj.traces

    fig = go.Figure([traces['data'], traces['new_data'], traces['contour']] + traces['new_lines'])
    f = go.FigureWidget(fig)
    f['layout']['xaxis'].zeroline = False
    f['layout']['yaxis'].zeroline = False
    f['layout']['xaxis'].range = [0, 8]
    f['layout']['yaxis'].range = [-3, 5]

    def update(xn, yn, kn, show):
        new_sample = np.array([[xn, yn]])

        k_obj.set_k(kn)
        k_obj.set_new_sample(new_sample)
        traces = k_obj.traces

        with f.batch_update():
            f.data[1]['marker']['color'] = traces['new_data']['marker']['color']
            f.data[1].x = [xn]
            f.data[1].y = [yn]
            f.data[2].z = traces['contour'].z
            f.data[2].visible = show
            for i in range(5):
                if i < kn:
                    f.data[3 + i].visible = True
                    f.data[3 + i].x = traces['new_lines'][i].x
                    f.data[3 + i].y = traces['new_lines'][i].y
                    f.data[3 + i].line.color = traces['new_lines'][i].line.color
                else:
                    f.data[3 + i].visible = False

    xn = FloatSlider(description='X1', value=3.3, min=1, max=7, step=.1)
    yn = FloatSlider(description='X2', value=1.2, min=-2, max=4, step=.1)
    kn = IntSlider(description='k neighbors', value=3, min=1, max=5, step=1)
    boundaries = Checkbox(description='Show Boundaries', value=False)

    return (f, interactive(update, xn=xn, yn=yn, kn=kn, show=boundaries))

if __name__ == '__main__':
    X, y = data()
    myk = plotKNN(X, y)
    vb = VBox(build_figure(myk), layout={'align_items': 'center'})