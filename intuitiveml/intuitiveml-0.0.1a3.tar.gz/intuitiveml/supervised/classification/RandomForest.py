import plotly.graph_objs as go
from plotly.tools import make_subplots
from ipywidgets import interactive, IntSlider
from intuitiveml.supervised.classification.DecisionTree import *

def build_figure_ensemble(dt_obj):
    traces = dt_obj.traces
    fig = make_subplots(1, 1, subplot_titles=('Ensemble',), print_grid=False)

    fig.append_trace(traces['axis'], 1, 1)
    fig.append_trace(traces['red'], 1, 1)
    fig.append_trace(traces['green'], 1, 1)
    fig.append_trace(traces['mid'], 1, 1)
    fig.append_trace(traces['ens_neg'], 1, 1)
    fig.append_trace(traces['ens_pos'], 1, 1)

    for i in range(4):
        fig.data[i]['y'] += .5

    f = go.FigureWidget(fig)
    f['layout'].showlegend = False
    f['layout']['xaxis']['title'] = 'X'
    f['layout']['yaxis']['title'] = 'Probability'
    f['layout']['barmode'] = 'overlay'

    names = ['axis', 'red', 'green', 'mid', 'ens_neg', 'ens_pos']

    def update(trees, depth):
        dt_obj.ensemble(n_trees=trees, max_depth=depth, ratio=1.0)
        traces = dt_obj.traces
        values = {'ens_neg': {'y': traces['ens_neg'].y, 'base': traces['ens_pos'].y},
                  'ens_pos': {'y': traces['ens_pos'].y},
                  'axis': {'y': traces['axis'].y + .5, 'x': traces['axis'].x},
                  'red': {'y': traces['red'].y + .5, 'x': traces['red'].x},
                  'green': {'y': traces['green'].y + .5, 'x': traces['green'].x},
                  'mid': {'y': traces['mid'].y + .5, 'x': traces['mid'].x}}

        with f.batch_update():
            for i, data in enumerate(f.data):
                try:
                    if values[names[i]]['base'] is not None:
                        data.base = values[names[i]]['base']
                except KeyError:
                    pass

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

    trees = IntSlider(description='Trees', value=0, min=0, max=50, step=5)
    depth = IntSlider(description='Max. Depth', value=3, min=1, max=3, step=1)

    return (f, interactive(update, trees=trees, depth=depth))
