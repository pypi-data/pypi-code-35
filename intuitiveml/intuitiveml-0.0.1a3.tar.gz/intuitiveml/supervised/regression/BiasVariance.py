import scipy.io as sio
import numpy as np
from requests import get
from io import BytesIO
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from plotly.tools import make_subplots
from plotly import graph_objs as go
from ipywidgets import VBox, interactive, IntSlider, Checkbox, Dropdown
from intuitiveml.supervised.regression.LinearRegression import plotLinearRegression
import warnings
warnings.filterwarnings("ignore")

def data():
    #ds = get('https://utkuufuk.github.io/2018/05/04/learning-curves/water.mat')
    #dataset = sio.loadmat(BytesIO(ds.content))

    x_train, y_train = (np.array([-15.93675813, -29.15297922,  36.18954863,  37.49218733,
                                  -48.05882945,  -8.94145794,  15.30779289, -34.70626581,
                                    1.38915437, -44.38375985,   7.01350208,  22.76274892]),
                        np.array([ 2.13431051,  1.17325668, 34.35910918, 36.83795516,  2.80896507,
                                   2.12107248, 14.71026831,  2.61418439,  3.74017167,  3.73169131,
                                   7.62765885, 22.7524283 ]))

    x_val, y_val = (np.array([-16.74653578, -14.57747075,  34.51575866, -47.01007574,
                               36.97511905, -40.68611002,  -4.47201098,  26.53363489,
                              -42.7976831 ,  25.37409938, -31.10955398,  27.31176864,
                               -3.26386201,  -1.81827649, -40.7196624 , -50.01324365,
                              -17.41177155,   3.5881937 ,   7.08548026,  46.28236902,
                               14.61228909]),
                     np.array([ 4.17020201e+00,  4.06726280e+00,  3.18730676e+01,  1.06236562e+01,
                                3.18360213e+01,  4.95936972e+00,  4.45159880e+00,  2.22763185e+01,
                               -4.38738274e-05,  2.05038016e+01,  3.85834476e+00,  1.93650529e+01,
                                4.88376281e+00,  1.10971588e+01,  7.46170827e+00,  1.47693464e+00,
                                2.71916388e+00,  1.09269007e+01,  8.34871235e+00,  5.27819280e+01,
                                1.33573396e+01]))
    x_test, y_test = (np.array([-33.31800399, -37.91216403, -51.20693795,  -6.13259585,
                                  21.26118327, -40.31952949, -14.54153167,  32.55976024,
                                  13.39343255,  44.20988595,  -1.14267768, -12.76686065,
                                  34.05450539,  39.22350028,   1.97449674,  29.6217551 ,
                                 -23.66962971,  -9.01180139, -55.94057091, -35.70859752,
                                   9.51020533]),
                     np.array([ 3.31688953,  5.39768952,  0.13042984,  6.1925982 , 17.08848712,
                                0.79950805,  2.82479183, 28.62123334, 17.04639081, 55.38437334,
                                4.07936733,  8.27039793, 31.32355102, 39.15906103,  8.08727989,
                               24.11134389,  2.4773548 ,  6.56606472,  6.0380888 ,  4.69273956,
                               10.83004606]))

    return x_train.reshape(-1, 1), y_train.reshape(-1, 1),\
           x_val.reshape(-1, 1), y_val.reshape(-1, 1), \
           x_test.reshape(-1, 1), y_test.reshape(-1, 1)

def train_models(x_train, y_train, model=None, degree=1, scale_x=False):
    if model is None:
        model = 'LinearRegression'
    model = globals()[model]()
    models = [plotLinearRegression(x_train[:i], y_train[:i], model=model, degree=degree, scale_x=scale_x)
              for i in range(degree+1, len(x_train)+1)]
    return models

def evaluate(x, y, models):
    mse = [mean_squared_error(y_true=y, y_pred=model.predict(x)) / 2
           for model in models]
    return mse

def build_figure(x_train, y_train, x_val, y_val, x_test, y_test):
    degree = 1
    min_samples = degree + 1
    max_samples = len(x_train)
    scale_x = True

    models = train_models(x_train, y_train, model=None, degree=degree, scale_x=scale_x)
    traces = models[0].traces
    traces_ant = traces

    train_mse = [model.mse / 2 for model in models]

    validation_mse = evaluate(x_val, y_val, models)
    test_mse = evaluate(x_test, y_test, models)

    fig = make_subplots(2, 4, specs=[[{'colspan': 2, 'rowspan': 2}, None, {'colspan': 2}, None],
                                     [None, None, {'colspan': 2}, None]],
                       subplot_titles=('Data', 'Coefficients', 'Error'), print_grid=False)

    fig.append_trace(traces['scatter'], 1, 1)
    fig.data[0].marker.color = 'green'
    fig.data[0].name = 'Training Data'

    fig.append_trace(traces['fit'], 1, 1)
    fig.data[1].marker.color = 'green'
    fig.data[1].name = 'fit'

    fig.append_trace(traces['coef'], 1, 3)
    fig.data[2].opacity = 0.7

    fig.append_trace(traces_ant['fit'], 1, 1)
    fig.data[3].visible = True
    fig.data[3].marker.color = 'gray'
    fig.data[3].line.dash = 'dash'
    fig.data[3].name = 'previous fit'

    fig.append_trace(traces_ant['coef'], 1, 3)
    fig.data[4].opacity = 0.5
    fig.data[4].visible = True
    fig.data[4].marker.color = 'gray'

    fig.append_trace(go.Scatter(x=np.arange(min_samples, len(x_train)+1), y=train_mse[:1], name='Train', marker={'color': 'green'}), 2, 3)
    fig.append_trace(go.Scatter(x=np.arange(min_samples, len(x_train)+1), y=validation_mse[:1], name='Validation', line={'color': 'blue'}), 2, 3)
    fig.append_trace(go.Scatter(x=np.arange(min_samples, len(x_train)+1), y=test_mse[:1], name='Test', line={'color': 'red'}), 2, 3)

    fig.append_trace(go.Scatter(x=x_val.ravel(), y=y_val.ravel(), name='Validation Data', mode='markers', marker={'color': 'blue'}), 1, 1)
    fig.data[8].visible = False
    fig.append_trace(go.Scatter(x=x_test.ravel(), y=y_test.ravel(), name='Test Data', mode='markers', marker={'color': 'red'}), 1, 1)
    fig.data[9].visible = False

    fig['layout']['barmode'] = 'overlay'
    fig['layout']['bargap'] = 0
    fig['layout']['autosize'] = False
    fig['layout']['width'] = 900
    fig['layout']['height'] = 500
    fig['layout']['xaxis'].range = [-50, 50]
    fig['layout']['yaxis'].range = [0, 40]
    fig['layout']['xaxis3'].range = [min_samples -.5, max_samples + .5]
    fig['layout']['yaxis3'].range = [-1, 50]

    f = go.FigureWidget(fig)

    names = ['scatter', 'fit', 'coef', 'fit2', 'coef2', 'train',
             'validation', 'test', 'scatter_val', 'scatter_test']

    def update(degree, samples, show_val, show_test):
        algo = 'LinearRegression'
        scale_x = True
        min_samples = degree + 1
        max_samples = len(x_train)
        if (min_samples + samples) >= 12:
            samples = 12 - min_samples

        models = train_models(x_train, y_train, model=algo, degree=degree, scale_x=scale_x)
        traces = models[samples].traces
        if samples > 0:
            traces_ant = models[samples - 1].traces
        else:
            traces_ant = traces
        train_mse = [model.mse / 2 for model in models]

        validation_mse = evaluate(x_val, y_val, models)
        test_mse = evaluate(x_test, y_test, models)

        values = {'train': {'x': np.arange(min_samples, len(x_train)+1), 'y': train_mse[:samples+1]},
                  'validation': {'x': np.arange(min_samples, len(x_train)+1), 'y': validation_mse[:samples+1]},
                  'test': {'x': np.arange(min_samples, len(x_train)+1), 'y': test_mse[:samples+1]}}

        values['scatter'] = traces['scatter']
        values['fit'] = traces['fit']
        values['coef'] = traces['coef']
        values['fit2'] = traces_ant['fit']
        values['coef2'] = traces_ant['coef']

        with f.batch_update():
            fit_ant = True
            if samples == 0:
                fit_ant = False
            f.data[names.index('fit2')].visible = fit_ant
            f.data[names.index('coef2')].visible = fit_ant
            f.data[names.index('scatter_val')].visible = show_val
            f.data[names.index('validation')].visible = show_val
            f.data[names.index('scatter_test')].visible = show_test
            f.data[names.index('test')].visible = show_test
            f['layout']['xaxis3'].range = [min_samples -.5, max_samples +.5]
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

    degree = IntSlider(description='Degree', value=1, min=1, max=8, step=1)
    #scale_x = Checkbox(description='Std.Features', value=True)
    #algo = Dropdown(options=['LinearRegression', 'Lasso','Ridge', 'ElasticNet'], value='LinearRegression', description='Model')
    samples = IntSlider(description='+Samples', value=0, min=0, max=10, stpe=1)
    show_val = Checkbox(description='Validation', value=False)
    show_test = Checkbox(description='Test', value=False)

    return (f, interactive(update, degree=degree, samples=samples, show_val=show_val, show_test=show_test))

if __name__ == '__main__':
    x_train, y_train, x_val, y_val, x_test, y_test = data()
    f = build_figure(x_train, y_train, x_val, y_val, x_test, y_test)
    vb = VBox(f, layout={'align_items': 'center'})