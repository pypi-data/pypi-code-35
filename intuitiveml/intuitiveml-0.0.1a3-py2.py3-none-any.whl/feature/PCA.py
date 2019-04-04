from intuitiveml.algebra.LinearAlgebra import *
from ipywidgets import Checkbox
from plotly.tools import make_subplots

def data(n_points=30, seed=42, scaling=(3, 1), transf=((.7, -.7), (.7, .7))):
    np.random.seed(seed)
    X = np.random.randn(n_points, 2)
    X *= np.array(scaling)
    rotation = np.array(transf)
    X = np.matmul(X, rotation.T).T
    return X

def build_figure(eigen_obj):
    explained_vars = np.diag(eigen_obj.cov)

    _, _, tdata, _ = eigen_obj.transf_eig(eigen_obj.steps)
    maxvar = np.diag(np.cov(np.array([tdata.x, tdata.y]))).max()

    tev1, tev2, tdata, tgrid = eigen_obj.transf_eig(0)

    tproj1, proj_linesx = eigen_obj.projection(tdata, axis='x', draw_lines=True)
    tproj2, proj_linesy = eigen_obj.projection(tdata, axis='y', draw_lines=True)

    traces = [tev1, tev2, tdata, tev1, tev2, tdata, *tgrid, *proj_linesx, *proj_linesy, tproj1, tproj2]

    fig = make_subplots(1, 3, specs=[[{'colspan': 2}, None, {}]], subplot_titles=('EigenVectors', 'Variance'), print_grid=False)
    for t in traces:
        fig.append_trace(t, 1, 1)
    fig.append_trace(go.Bar(x=['x', 'y'], y=explained_vars, name='explained', showlegend=False, marker={'color': ['blue', 'green']}), 1, 3)

    fig['layout']['xaxis'].update({'zeroline': False, 'range': eigen_obj.xrange})
    fig['layout']['yaxis'].update({'zeroline': False, 'range': eigen_obj.yrange})
    fig['layout']['yaxis2'].update({'range': [0, maxvar + .1]})
    fig['layout']['width'] = 800
    fig['layout']['height'] = 500
    fig['layout']['annotations'][0].text = 'EigenValues: {:.2f} / {:.2f}'.format(*eigen_obj.eigenvalues)
    fig.data[1].line.dash = 'dash'

    fig.data[3].name = 'EigenVector 1'
    fig.data[3].marker.color = 'black'
    fig.data[4].name = 'EigenVector 2'
    fig.data[4].marker.color = 'black'
    fig.data[4].line.dash = 'dash'
    fig.data[5].name = 'Data'
    fig.data[5].marker.color = 'black'

    f = go.FigureWidget(fig)

    def update_step(step, show_eigen, show_data, show_fc, show_sc):
        tev1, tev2, tdata, tgrid = eigen_obj.transf_eig(step)

        explained_vars = np.diag(np.cov(np.array([tdata.x, tdata.y])))

        tproj1, proj_linesx = eigen_obj.projection(tdata, axis='x', draw_lines=True)
        tproj2, proj_linesy = eigen_obj.projection(tdata, axis='y', draw_lines=True)
        tgrid = list(tgrid)
        proj_linesx = list(proj_linesx)
        proj_linesy = list(proj_linesy)

        values = {'Transf. EigenVector 1': {'x': tev1.x, 'y': tev1.y},
                  'Transf. EigenVector 2': {'x': tev2.x, 'y': tev2.y},
                  'Transf. Data': {'x': tdata.x, 'y': tdata.y},
                  'x Component': {'x': tproj1.x, 'y': tproj1.y},
                  'y Component': {'x': tproj2.x, 'y': tproj2.y},
                  'explained': {'x': ['First', 'Second'],'y': explained_vars}}

        with f.batch_update():
            lines = -1
            projx = -1
            projy = -1

            f.data[0].visible = show_eigen
            f.data[1].visible = show_eigen
            f.data[3].visible = show_eigen
            f.data[4].visible = show_eigen

            f.data[2].visible = show_data
            f.data[5].visible = False

            for i, data in enumerate(f.data):
                try:
                    xy = values[data['name']]
                    f.data[i].x = xy['x']
                    f.data[i].y = xy['y']
                except KeyError:
                    pass

                if data['name'] == 'grid':
                    lines += 1
                    f.data[i].x = tgrid[lines].x
                    f.data[i].y = tgrid[lines].y
                if data['name'] == 'projection x':
                    projx += 1
                    f.data[i].visible = show_fc and show_data
                    f.data[i].x = proj_linesx[projx].x
                    f.data[i].y = proj_linesx[projx].y
                if data['name'] == 'projection y':
                    projy += 1
                    f.data[i].visible = show_sc and show_data
                    f.data[i].x = proj_linesy[projy].x
                    f.data[i].y = proj_linesy[projy].y
                if data['name'] == 'x Component':
                    f.data[i].visible = show_fc
                if data['name'] == 'y Component':
                    f.data[i].visible = show_sc

    step_slider = IntSlider(description='Step', value=0, min=0, max=20, step=1)
    show_eigen = Checkbox(description='EigenVectors', value=True)
    show_data = Checkbox(description='Data', value=False)
    show_fc = Checkbox(description='x Component', value=False)
    show_sc = Checkbox(description='y Component', value=False)

    return (f, interactive(update_step, step=step_slider, show_data=show_data, show_eigen=show_eigen, show_fc=show_fc, show_sc=show_sc))

if __name__ == '__main__':
    X = data()
    eo = plotEigen(X)
    vb = VBox(build_figure(eo), layout={'align_items': 'center'})
