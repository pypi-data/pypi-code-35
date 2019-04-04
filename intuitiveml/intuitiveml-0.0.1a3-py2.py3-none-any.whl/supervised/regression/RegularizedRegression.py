from intuitiveml.supervised.regression.LinearRegression import plotLinearRegression
import numpy as np
import plotly.graph_objs as go
from deepreplay.plot import build_2d_grid
from matplotlib import pyplot as plt
from plotly.tools import make_subplots
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from ipywidgets import VBox, interactive, IntSlider, Dropdown, Checkbox
import warnings
from copy import deepcopy
warnings.filterwarnings("ignore")

def data():
    np.random.seed(42)
    orig_x = np.linspace(-1, 3, 1000)
    orig_y = 5 * orig_x ** 2 + .3 * orig_x - 2 + 5 * np.random.randn(1000)

    additional_x = np.linspace(-2, -1, 250)
    additional_y = 5 * additional_x ** 2 + .3 * additional_x - 2 + 5 * np.random.randn(250)

    np.random.seed(42)
    shuffled = list(range(1000))
    np.random.shuffle(shuffled)
    x = orig_x[shuffled[:20]].reshape(-1, 1)
    y = orig_y[shuffled[:20]]

    shuffled = list(range(250))
    np.random.shuffle(shuffled)
    additional_x = additional_x[shuffled[:10]].reshape(-1, 1)
    additional_y = additional_y[shuffled[:10]]

    extra_x = np.concatenate([x, additional_x], axis=0)
    extra_y = np.concatenate([y, additional_y], axis=0)
    return x, y, additional_x, additional_y, extra_x, extra_y

def build_figure(lr_obj, lr_obj_addit, additional_x, additional_y):
    traces = lr_obj.traces
    traces_addit = lr_obj_addit.traces

    x, y = lr_obj.original_x, lr_obj.original_y
    extra_x, extra_y = lr_obj_addit.original_x, lr_obj_addit.original_y

    fig = make_subplots(2, 4, specs=[[{'colspan': 2, 'rowspan': 2}, None, {'colspan': 2}, None],
                                     [None, None, {'colspan': 2}, None]],
                       subplot_titles=('Data', 'Coefficients', 'Error'), print_grid=False)

    fig.append_trace(traces['scatter'], 1, 1)
    fig.append_trace(traces['fit'], 1, 1)
    fig.append_trace(traces['coef'], 1, 3)
    fig.append_trace(traces['histogram'], 2, 3)
    fig.append_trace(traces['mean_error'], 2, 3)
    fig.data[1].marker.color = 'green'
    fig.data[1].name = 'fit'
    fig.data[2].opacity = 0.7
    fig.data[3].opacity = 0.7

    fig.append_trace(traces_addit['scatter'], 1, 1)
    fig.append_trace(traces_addit['fit'], 1, 1)
    fig.append_trace(traces_addit['coef'], 1, 3)
    fig.append_trace(traces_addit['histogram'], 2, 3)
    fig.append_trace(traces_addit['mean_error'], 2, 3)

    fig.append_trace(traces['fit'], 1, 1)

    fig.data[5].visible = False
    fig.data[5].marker.color = 'red'
    fig.data[5].name = 'new data'
    fig.data[6].visible = False
    fig.data[6].marker.color = 'gray'
    fig.data[6].name = 'new fit'
    fig.data[7].opacity = 0.5
    fig.data[7].visible = False
    fig.data[7].marker.color = 'gray'
    fig.data[8].opacity = 0.5
    fig.data[8].visible = False
    fig.data[8].marker.color = 'red'
    fig.data[9].name = 'ME - unseen'
    fig.data[9].visible = False
    fig.data[9].line.color = 'red'

    fig.data[10].marker.update({'color': 'green'})
    fig.data[10].line.update({'dash': 'dash'})
    fig.data[10].visible = False

    #fig['layout']['xaxis3'].update(range=[-20, 20])
    #fig['layout']['yaxis3'].update(range=[0, .5])
    fig['layout']['barmode'] = 'overlay'
    fig['layout']['bargap'] = 0
    fig['layout']['autosize'] = False
    fig['layout']['width'] = 900
    fig['layout']['height'] = 500

    f = go.FigureWidget(fig)

    names = ['scatter', 'fit', 'coef', 'histogram', 'mean_error',
             'scatter2', 'fit2', 'coef2', 'histogram2', 'mean_error2',
             'fit3']

    def update_poly(degree, algo, additional):
        model = globals()[algo](fit_intercept=False)
        mylr = plotLinearRegression(x, y, degree=degree, model=model)
        values = deepcopy(mylr.values())
        if additional:
            f['layout']['annotations'][2].text = 'Original Fit - Errors on Unseen Data'
            yhat = mylr.predict(additional_x)
            error = (yhat - additional_y)
            xmin = np.min([-1., error.min() - .01])
            xbins = dict(start=xmin, end=error.max() + 0.01, size=(error.max() - xmin + .02)/10)
            values['histogram2'] = dict(x=error,
                                        y=None)
            values['mean_error2'] = dict(x=[error.mean(),
                                            error.mean()],
                                         y=[0, 1])

            yextra = mylr.predict(np.array(sorted(extra_x.ravel())))
            values.update({'fit3': dict(x=sorted(extra_x.ravel()), y=yextra)})

            mylr_addit = plotLinearRegression(extra_x, extra_y, degree=degree, model=model)
            addit_values = mylr_addit.values()

            values['scatter2'] = dict(x=additional_x.ravel(),
                                      y=additional_y)
            values['fit2'] = dict(x=sorted(extra_x.ravel()),
                                  y=addit_values['fit']['y'])
            values['coef2'] = addit_values['coef']
        else:
            f['layout']['annotations'][2].text = 'SSE = {:.2f} - R2 = {:.4f}'.format(mylr.sse, mylr.r2)

            values['scatter2'] = values['scatter']
            values['fit2'] = values['fit']
            values['coef2'] = values['coef']
            values['histogram2'] = values['histogram']
            values['mean_error2'] = values['mean_error']
            values['fit3'] = values['fit']

        with f.batch_update():
            if additional:
                f.data[names.index('scatter2')].visible = True
                f.data[names.index('fit2')].visible = True
                f.data[names.index('coef2')].visible = True
                f.data[names.index('histogram')].visible = False
                f.data[names.index('histogram2')].visible = True
                f.data[names.index('mean_error2')].visible = True
                f.data[names.index('fit3')].visible = True

                f.data[names.index('histogram')].xbins = xbins
                f.data[names.index('histogram2')].xbins = xbins
            else:
                f.data[names.index('scatter2')].visible = False
                f.data[names.index('fit2')].visible = False
                f.data[names.index('coef2')].visible = False
                f.data[names.index('histogram')].visible = True
                f.data[names.index('histogram2')].visible = False
                f.data[names.index('mean_error2')].visible = False
                f.data[names.index('fit3')].visible = False

                f.data[names.index('histogram')].xbins = dict(start=-20, end=20, size=4)
                f.data[names.index('histogram2')].xbins = dict(start=-20, end=20, size=4)

            for i, data in enumerate(f.data):
                if values[names[i]]['y'] is not None:
                    data.y = values[names[i]]['y']
                if values[names[i]]['x'] is not None:
                    data.x = values[names[i]]['x']

    degree = IntSlider(description='Degree', value=1, min=1, max=10, step=1)
    algo = Dropdown(options=['LinearRegression', 'Lasso','Ridge', 'ElasticNet'], value='LinearRegression', description='Model')
    additional = Checkbox(value=False, description='Add Unseen Data')

    return (f, interactive(update_poly, degree=degree, algo=algo, additional=additional))

def plot_surfaces(x, y):
    plt.style.use('fivethirtyeight')
    models = [LinearRegression(fit_intercept=False),
              Lasso(fit_intercept=False),
              Ridge(fit_intercept=False),
              ElasticNet(fit_intercept=False)
    ]

    pipelines = [make_pipeline(PolynomialFeatures(degree=1, include_bias=True), model) for model in models]

    for pipeline in pipelines:
        pipeline.fit(x, y)

    #coefs = np.array([[pipeline.steps[1][1].intercept_, pipeline.steps[1][1].coef_] for pipeline in pipelines])
    coefs = np.array([pipeline.steps[1][1].coef_ for pipeline in pipelines])

    def regularization(v, ratio):
        return ratio * np.linalg.norm(v, ord=1) + ((1 - ratio) / 2) * (np.linalg.norm(v, ord=2) ** 2)

    grid = build_2d_grid([-25, 20], [25, -20], n_lines=200, n_points=200)
    norms = [np.apply_along_axis(func1d=lambda v: regularization(v, ratio), axis=2, arr=grid) for ratio in [1, 0, .5]]

    predictions = np.dot(grid, np.concatenate([np.ones_like(x), x], axis=1).T)
    losses = np.apply_along_axis(func1d=lambda v: mean_squared_error(y, v), axis=2, arr=predictions)
    figure, axes = plt.subplots(3, 3, figsize=(12, 12))
    for model in range(1, 4):
        axes[model-1, 0].contourf(grid[:, :, 0], grid[:, :, 1], norms[model-1], cmap=plt.cm.brg, alpha=0.3, levels=np.linspace(0, 80, 11))

        axes[model-1, 1].contourf(grid[:, :, 0], grid[:, :, 1], losses, cmap=plt.cm.brg, alpha=0.3, levels=np.linspace(0, 200, 11))
        axes[model-1, 1].scatter(coefs[0, 0:1], coefs[0, 1:2])

        axes[model-1, 2].contourf(grid[:, :, 0], grid[:, :, 1], losses, cmap=plt.cm.brg, alpha=0.4, levels=np.linspace(0, 200, 11))
        axes[model-1, 2].contourf(grid[:, :, 0], grid[:, :, 1], norms[model-1], cmap=plt.cm.brg, alpha=0.2, levels=np.linspace(0, 80, 11))
        axes[model-1, 2].scatter(coefs[0, 0:1], coefs[0, 1:2])
        axes[model-1, 2].scatter(coefs[model, 0:1], coefs[model, 1:2], c='r')
    figure.tight_layout()
    return figure

if __name__ == '__main__':
    x, y, additional_x, additional_y, extra_x, extra_y = data()
    mylr = plotLinearRegression(x, y)
    mylr.histogram, _ = mylr.plot_histogram(-20, 20, 10)

    mylr_addit = plotLinearRegression(extra_x, extra_y)
    mylr_addit.histogram, _ = mylr_addit.plot_histogram(-20, 20, 10)

    vb = VBox(build_figure(mylr, mylr_addit, additional_x, additional_y))
    vb.layout.align_items = 'center'
