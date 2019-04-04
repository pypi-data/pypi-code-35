import numpy as np
import plotly.graph_objs as go
from plotly.tools import make_subplots
from ipywidgets import interactive, IntSlider
from intuitiveml.supervised.classification.DecisionTree import *

def build_figure_boost(dt_obj):
    n_trees = 6
    dt_obj.boost(n_trees, 1)
    traces = dt_obj.traces

    fig = make_subplots(1, 2, subplot_titles=('Ensemble', 'Residuals'), print_grid=False)

    fig.append_trace(traces['boosted_data'], 1, 1)
    for i, tree in enumerate(traces['boosted_trees']):
        fig.append_trace(tree, 1, 1)
        if i == n_trees and n_trees > 0:
            fig.append_trace(tree, 1, 2)
            fig.data[-1].showlegend = False
    res = traces['boosted_residuals'][n_trees-1]
    res['line']['color'] = 'red'
    fig.append_trace(res, 1, 2)

    f = go.FigureWidget(fig)

    def update(trees, depth):
        dt_obj.boost(n_trees=6, max_depth=depth)
        traces = dt_obj.traces
        trees = np.minimum(trees, len(traces['boosted_trees'])-1)

        with f.batch_update():
            for i in range(7):
                if i > trees:
                    f.data[i+1].visible = False
                else:
                    f.data[i+1].visible = True
                    f.data[i+1].x = traces['boosted_trees'][i].x
                    f.data[i+1].y = traces['boosted_trees'][i].y

            if trees > 0:
                f.data[8].visible = True
                f.data[8].x = traces['boosted_trees'][trees].x
                f.data[8].y = traces['boosted_trees'][trees].y
                f.data[8].line.color = traces['boosted_trees'][trees].line.color
            else:
                f.data[8].visible = False
            i = trees - 1
            if i < 0:
                i = 0
            f.data[-1].x = traces['boosted_residuals'][i].x
            f.data[-1].y = traces['boosted_residuals'][i].y

    trees = IntSlider(description='Trees', value=0, min=0, max=6, step=1)
    depth = IntSlider(description='Max. Depth', value=1, min=1, max=3, step=1)

    return (f, interactive(update, trees=trees, depth=depth))

