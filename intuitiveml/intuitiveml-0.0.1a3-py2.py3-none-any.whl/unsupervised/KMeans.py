import numpy as np
import plotly.graph_objs as go
from plotly.tools import make_subplots
from ipywidgets import VBox, interactive, IntSlider
from scipy.spatial import distance_matrix

def data():
    np.random.seed(1)
    c1 = np.random.randn(30).reshape(15, 2) + np.array([2, 3])
    c2 = np.random.randn(20).reshape(10, 2) + np.array([5, 1])
    c3 = np.random.randn(20).reshape(10, 2) + np.array([3, -1])
    X = np.concatenate([c1, c2, c3], axis=0)
    y = np.concatenate([[0] * 15, [1] * 10, [2] * 10])
    return X, y

def get_colors(cl):
    return [['green', 'red', 'blue', 'orange', 'purple'][v] for v in cl]

class plotKMeans(object):
    def __init__(self, X, y, n_centroids):
        self.orig_X = X
        self.orig_y = y
        self.X = X
        self.y = y

        self.n_centroids = 0
        self.n_iterations = 0
        self.set_centroids(n_centroids)
        self.data = self.data_trace(self.X, 'black')

    @property
    def traces(self):
        return dict(data=self.data,
                    centroids=self.centroids,
                    within=self.within)

    def set_iteration(self, iter):
        iter = np.minimum(iter, self.n_iterations)
        self.centroids = self.centroids_trace(self.centroids_hist[iter], get_colors(range(self.n_centroids)))
        self.within = self.within_trace(self.within_hist[iter], get_colors(range(self.n_centroids)))

    def set_centroids(self, n_centroids):
        if self.n_centroids != n_centroids:
            self.n_centroids = n_centroids
            self.clusters_hist, self.centroids_hist, self.within_hist = self.compute(self.n_centroids)
            self.set_iteration(0)

    def data_trace(self, c, colors):
        return go.Scatter(x=c[:, 0], y=c[:, 1], showlegend=False, mode='markers', marker={'opacity': .5, 'color': colors, 'size': 12, 'line': {'color': 'black', 'width': 2}})

    def centroids_trace(self, centroids, colors):
        return go.Scatter(x=centroids[:, 0], y=centroids[:, 1], name='Centroids', mode='markers', marker={'symbol': 'cross', 'size': 15, 'color': colors})

    def within_trace(self, within, colors):
        names = colors[:]
        if len(within) == 1:
            colors = 'gray'
            names = ['']
        return go.Bar(x=names, y=within, showlegend=False, marker={'color': colors, 'line': {'color': 'black', 'width': 2}})

    def compute(self, n_centroids):
        centroids = self.X[np.random.choice(range(self.X.shape[0]), n_centroids, replace=False), :]
        clusters = np.zeros(self.X.shape[0], dtype=np.int)
        centroids_history = []
        clusters_history = [clusters]
        within_history = [[(distance_matrix(self.X, self.X.mean(axis=0).reshape(1, -1), p=2) ** 2).sum()]]

        rounds = 0
        while rounds < 10:
            centroids_history.append(centroids)
            old_clusters = clusters
            distances = distance_matrix(self.X, centroids, p=2)
            clusters = np.argmin(distances, axis=1)
            within = [(distances.min(axis=1)[clusters == i] ** 2).sum() for i in range(n_centroids)]
            if np.all(clusters == old_clusters):
                break
            clusters_history.append(clusters)
            within_history.append(within)
            centroids = np.array([self.X[clusters==i].mean(axis=0) for i in range(n_centroids)])
            rounds += 1
            self.n_iterations = rounds

        return clusters_history, centroids_history, within_history

def build_figure(k_obj):
    traces = k_obj.traces

    fig = make_subplots(1, 3, specs=[[{'colspan': 2}, None, {}]], subplot_titles=('Data', 'Within SSE'), print_grid=False)
    fig.append_trace(traces['data'], 1, 1)
    fig.append_trace(traces['centroids'], 1, 1)
    fig.append_trace(traces['within'], 1, 3)

    f = go.FigureWidget(fig)
    f['layout']['xaxis'].zeroline = False
    f['layout']['yaxis'].zeroline = False
    f['layout']['yaxis2'].range = [0, np.maximum(k_obj.within_hist[0], np.max(k_obj.within_hist[1:]))[0] + 1]

    def update(iteration, n_centroids):
        recompute = False
        if k_obj.n_centroids != n_centroids:
            k_obj.set_centroids(n_centroids)
            recompute = True

        rounds = len(k_obj.centroids_hist) - 1
        i = iteration // 2
        if i > rounds:
            i = rounds

        k_obj.set_iteration(i)
        traces = k_obj.traces

        colors = 'black'
        if iteration > 1:
            colors = get_colors(k_obj.clusters_hist[i])

        total_within = sum(k_obj.within_hist[i])

        with f.batch_update():
            f['layout']['yaxis2'].range = [0, np.maximum(k_obj.within_hist[0], np.max(k_obj.within_hist[1:]))[0] + 1]
            f['layout']['annotations'][1]['text'] = 'Within SSE: {:.2f}'.format(total_within)
            if iteration % 2 or recompute:
                f.data[1].x = traces['centroids'].x
                f.data[1].y = traces['centroids'].y
                f.data[1].marker.color = traces['centroids'].marker.color
            f.data[2].x = traces['within'].x
            f.data[2].y = traces['within'].y
            f.data[2].marker.color = traces['within'].marker.color
            f.data[0].marker.color = colors

    iteration = IntSlider(description='Iteration', value=1, min=1, max=20, step=1)
    centr = IntSlider(description='Clusters', value=3, min=2, max=5, step=1)

    return (f, interactive(update, iteration=iteration, n_centroids=centr))

if __name__ == '__main__':
    X, y = data()
    n_centroids = 3
    myk = plotKMeans(X, y, n_centroids)
    vb = VBox(build_figure(myk), layout={'align_items': 'center'})