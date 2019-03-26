from bokeh.io import output_notebook, show
from bokeh.models import HoverTool
from bokeh.models.ranges import Range1d
from bokeh.plotting import ColumnDataSource, figure
import warnings


def format_time_to_s(values):
    return list(map(lambda x: str(x / 1000) + ' s', values))


def visualize_mouse_data(data, width=None, height=None, discrete=False):
    output_notebook()
    if width is not None and height is not None:
        p = figure(plot_width=width, plot_height=height)
    elif width is None and height is None:
        p = figure()
    else:
        warnings.warn("You have to set both dimensions")
        p = figure()

    mouse_move_data = data[(data['eventType'] == 'MOUSE_MOVE')]
    line_data_source = ColumnDataSource(data=dict(
        x=mouse_move_data['payload_positionX'].values,
        y=mouse_move_data['payload_positionY'].values,
        eventType=mouse_move_data['eventType'].values,
        time=format_time_to_s(mouse_move_data['timeStamp'].values)
    ))

    if discrete is False:
        p.line('x', 'y', source=line_data_source, line_width=2)
    else:
        p.circle('x', 'y', source=line_data_source, size=5)

    mouse_up_down_data = data[(data['eventType'] == 'MOUSE_UP') | (
                data['eventType'] == 'MOUSE_DOWN')]
    events_source = ColumnDataSource(data=dict(
        x=mouse_up_down_data['payload_positionX'].values,
        y=mouse_up_down_data['payload_positionY'].values,
        eventType=mouse_up_down_data['eventType'].values,
        time=format_time_to_s(mouse_up_down_data['timeStamp'].values)
    ))

    p.circle('x', 'y', source=events_source, size=8, color="red", alpha=0.5)

    tooltips = [
        ('X', '@x'),
        ('Y', '@y'),
        ('eventType', '@eventType'),
        ('time', '@time')
    ]

    p.add_tools(HoverTool(tooltips=tooltips))
    p.y_range = Range1d(data['payload_positionY'].max(),
                        data['payload_positionY'].min())
    show(p)
