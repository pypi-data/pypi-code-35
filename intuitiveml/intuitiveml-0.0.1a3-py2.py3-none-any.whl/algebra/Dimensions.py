import numpy as np
import plotly.graph_objs as go

def build_rect(xc, yc, x, y):
    rect = {
                'type': 'rect',
                'xref': 'x',
                'yref': 'y',
                'x0': xc,
                'y0': yc,
                'x1': x,
                'y1': y,
                'line': {
                    'color': 'black',
                    'width': 3,
                },
            }
    return rect

def build_circle(xc, yc, r):
    x0 = xc - r
    y0 = yc - r
    x1 = xc + r
    y1 = yc + r
    circle = {
                'type': 'circle',
                'xref': 'x',
                'yref': 'y',
                'x0': x0,
                'y0': y0,
                'x1': x1,
                'y1': y1,
                'visible': True,
                'name': 'empty',
                'line': {
                    'color': 'black'
                },
            }
    return circle

def calc_radius(dim):
    return np.linalg.norm([1] * dim, 2) - 1

def build_figure_2d():
    vertices = np.array([[-1, -1], [-1, 1], [1, 1], [1, -1]])
    data_trace = go.Scatter(x=vertices[:, 0], showlegend=False, y=vertices[:, 1], mode='markers', marker={'color': 'black', 'size': 10})
    r = calc_radius(2)
    radius_trace = go.Scatter(x=[-r, r], name='diameter', y=[0, 0], showlegend=False, mode='lines', line={'color': 'red', 'width': 3})
    fig = go.Figure([data_trace, radius_trace])

    fig['layout']['shapes'] = [build_rect(-1, -1, 1, 1)] + [build_circle(v[0], v[1], 1) for v in vertices] + [build_circle(0, 0, np.linalg.norm(vertices[0], 2) - 1)]
    fig['layout']['width'] = 800
    fig['layout']['height'] = 800
    fig['layout']['title'] = 'Diameter / Edge = {:.4f}'.format(r)
    return fig

def build_figure_3d():
    theta = np.linspace(0, 2*np.pi, 100)
    phi = np.linspace(0, np.pi, 100)
    x = np.outer(np.cos(theta),np.sin(phi))
    y = np.outer(np.sin(theta),np.sin(phi))
    z = np.outer(np.ones(100),np.cos(phi))

    vertices = np.array([[-1, -1, -1], [-1, 1, -1], [1, 1, -1], [1, -1, -1],
                         [-1, -1, 1], [-1, 1, 1], [1, 1, 1], [1, -1, 1]])

    r = calc_radius(3)

    cube_lines = [
     go.Scatter3d(x=[-1, -1], y=[-1, -1], z=[-1, 1], showlegend=False, mode='lines', line={'color': 'black', 'width': 3}),
     go.Scatter3d(x=[-1, -1], y=[1, 1], z=[-1, 1], showlegend=False, mode='lines', line={'color': 'black', 'width': 3}),
     go.Scatter3d(x=[-1, -1], y=[-1, 1], z=[-1, -1], showlegend=False, mode='lines', line={'color': 'black', 'width': 3}),
     go.Scatter3d(x=[-1, -1], y=[-1, 1], z=[1, 1], showlegend=False, mode='lines', line={'color': 'black', 'width': 3}),

     go.Scatter3d(x=[1, 1], y=[-1, -1], z=[-1, 1], showlegend=False, mode='lines', line={'color': 'black', 'width': 3}),
     go.Scatter3d(x=[1, 1], y=[1, 1], z=[-1, 1], showlegend=False, mode='lines', line={'color': 'black', 'width': 3}),
     go.Scatter3d(x=[1, 1], y=[-1, 1], z=[-1, -1], showlegend=False, mode='lines', line={'color': 'black', 'width': 3}),
     go.Scatter3d(x=[1, 1], y=[-1, 1], z=[1, 1], showlegend=False, mode='lines', line={'color': 'black', 'width': 3}),

     go.Scatter3d(x=[-1, 1], y=[-1, -1], z=[1, 1], showlegend=False, mode='lines', line={'color': 'black', 'width': 3}),
     go.Scatter3d(x=[-1, 1], y=[-1, -1], z=[-1, -1], showlegend=False, mode='lines', line={'color': 'black', 'width': 3}),
     go.Scatter3d(x=[-1, 1], y=[1, 1], z=[-1, -1], showlegend=False, mode='lines', line={'color': 'black', 'width': 3}),
     go.Scatter3d(x=[-1, 1], y=[1, 1], z=[1, 1], showlegend=False, mode='lines', line={'color': 'black', 'width': 3}),
    ]

    radius_trace = go.Scatter3d(x=[-r, r],
                                y=[0, 0],
                                z=[0, 0], showlegend=False, mode='lines', line={'color': 'red', 'width': 6})

    data = [
        go.Surface(
            x=x + v[0],
            y=y + v[1],
            z=z + v[2],
            showscale=False,
            visible=True,
            opacity=.5
        ) for v in vertices
    ] + [go.Surface(x=x*r, y=y*r, z=z*r ,showscale=False, opacity=.8), radius_trace] + cube_lines


    layout = go.Layout(
        autosize=False,
        width=800,
        height=800,
        margin=dict(
            l=20,
            r=20,
            b=20,
            t=70,
        ),
        title='Diameter / Edge = {:.4f}'.format(r)
    )
    fig = go.Figure(data=data, layout=layout)
    return fig