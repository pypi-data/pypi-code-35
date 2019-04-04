import numpy as np
import plotly.graph_objs as go
from plotly.tools import make_subplots
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.metrics import r2_score, mean_squared_error
from ipywidgets import VBox, interactive, FloatSlider

def data():
    np.random.seed(42)
    x = np.random.randn(100, 1)
    y = 1.015 + np.pi * x + 0.5 * np.random.randn(100, 1)
    return x, y

class plotLinearRegression(object):
    def __init__(self, x, y, model=None, degree=1, scale_x=False):
        self.fit_intercept = True
        if model is None:
            model = LinearRegression()
        else:
            self.fit_intercept = model.fit_intercept

        if scale_x:
            self.scaler = StandardScaler(with_mean=True, with_std=True)
            self.scaler.fit(x)
            self.x = self.scaler.transform(x).ravel()
        else:
            self.scaler = None
            self.x = x.ravel()
        self.y = y.ravel()
        self.original_x = x.ravel()
        self.original_y = y.ravel()
        self.scatter = go.Scatter(x=self.original_x, y=self.y, mode='markers', name='data')

        self.yhat = None
        self.errors = None
        self.r2 = None
        self.sse = None
        self.mse = None

        self.model = model
        self.degree = degree
        if degree > 1 or (not self.fit_intercept):
            self.make_polynomial(self.degree)
            if not self.fit_intercept:
                degree += 1
        self.linr = model.fit(self.x.reshape(-1, degree), self.y.reshape(-1, 1))
        if self.fit_intercept:
            self.coef_ = np.append(self.linr.intercept_, self.linr.coef_)
        else:
            self.coef_ = self.linr.coef_.squeeze()
        self.evaluate()

    def make_polynomial(self, degree):
        self.degree = degree
        x = self.original_x.reshape(-1, 1)
        if self.scaler is not None:
            x = self.scaler.transform(x)
        self.x = PolynomialFeatures(degree=degree, include_bias=not self.fit_intercept).fit_transform(x)

    def predict(self, x):
        x = x.reshape(-1, 1)
        if self.scaler is not None:
            x = self.scaler.transform(x)
        x = PolynomialFeatures(degree=self.degree, include_bias=not self.fit_intercept).fit_transform(x)
        yhat = self.linr.predict(x)
        return yhat.ravel()

    def evaluate(self, betas=None):
        degree = self.degree
        if not self.fit_intercept:
            degree += 1
        x = self.x.reshape(-1, degree)
        if (betas is None) or (self.degree > 1):
            yhat = self.linr.predict(x)
        else:
            if self.scaler is not None:
                x = self.scaler.transform(x).ravel()
            yhat = (np.array(betas[0]).reshape(-1, 1) + np.dot(x, np.array(betas[1:]).reshape(-1, 1)))
        self.yhat = yhat.ravel()

        self.errors = self.yhat - self.y
        self.sse = (self.errors ** 2).sum()
        self.r2 = r2_score(y_true=self.y, y_pred=self.yhat)
        self.mse = mean_squared_error(y_true=self.y, y_pred=self.yhat)

        self.line = self.plot_line()
        self.histogram, self.mean = self.plot_histogram()
        self.coef = self.plot_coef()

    def plot_coef(self):
        coef = go.Bar(x=['b{}'.format(i) for i in np.arange(self.degree + 1)],
                           y=self.coef_,
                           showlegend=False, marker={'color': 'green'})
        return coef

    def plot_line(self):
        xy = np.array([np.array([x, y]) for x, y in sorted(zip(self.original_x, self.yhat))])
        line = go.Scatter(x=xy[:, 0], y=xy[:, 1], mode='lines', name='Linear')
        return line

    def plot_histogram(self, xmin=-10, xmax=10, nbins=10):
        histogram = go.Histogram(x=self.errors, histnorm='probability',
                                      marker=dict(color='orange'),
                                      name='Errors',
                                      xbins=dict(start=xmin, end=xmax, size=(xmax - xmin)/nbins))
        mean = go.Scatter(x=[self.errors.mean(), self.errors.mean()], y=[0, 1],
                               mode='lines', name='Mean Error',
                               line=dict(color='black', width=1, dash='dash'))
        return histogram, mean

    @property
    def traces(self):
        return dict(scatter=self.scatter,
                    fit=self.line,
                    histogram=self.histogram,
                    mean_error=self.mean,
                    coef=self.coef)

    def values(self, betas=None):
        if betas is not None:
            self.evaluate(betas)
        yhat = np.array([y for _, y in sorted(zip(self.original_x, self.yhat))])
        values = dict(scatter=dict(x=None, y=None),
                      fit=dict(x=None, y=yhat),
                      histogram=dict(x=self.errors, y=None),
                      mean_error=dict(x=[self.errors.mean(), self.errors.mean()], y=None),
                      coef=dict(x=['b{}'.format(i) for i in np.arange(self.degree + 1)],
                                y=self.coef_))
        return values

def build_figure(lr_obj):
    traces = lr_obj.traces

    fig = make_subplots(1, 2, subplot_titles=('Mean = {:.3f}'.format(lr_obj.y.mean()), 'Error'), print_grid=False)
    fig.append_trace(traces['scatter'], 1, 1)
    fig.append_trace(traces['fit'], 1, 1)
    fig.append_trace(traces['histogram'], 1, 2)
    fig.append_trace(traces['mean_error'], 1, 2)
    names = ['scatter', 'fit', 'histogram', 'mean_error']

    fig['layout'].update(title='Linear Regression')
    fig['layout']['xaxis2'].update(range=[-20, 20])
    fig['layout']['showlegend'] = False

    f = go.FigureWidget(fig)

    def update(beta0, beta1):
        values = lr_obj.values((beta0, beta1))
        with f.batch_update():
            f['layout']['annotations'][1].text = 'SSE = {:.2f} - R2 = {:.4f}'.format(lr_obj.sse, lr_obj.r2)
            for i, data in enumerate(f.data):
                if values[names[i]]['y'] is not None:
                    data.y = values[names[i]]['y']
                if values[names[i]]['x'] is not None:
                    data.x = values[names[i]]['x']

    beta0 = FloatSlider(description=r'\(b\)', value=0.0, min=-5.0, max=5.0, step=0.1)
    beta1 = FloatSlider(description=r'\(w_1\)', value=1.0, min=-5.0, max=5.0, step=0.1)

    return (f, interactive(update, beta0=beta0, beta1=beta1))

if __name__ == '__main__':
    x, y = data()
    mylr = plotLinearRegression(x, y)
    vb = VBox(build_figure(mylr))
    vb.layout.align_items = 'center'
