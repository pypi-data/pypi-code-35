import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.tools import make_subplots
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, precision_recall_curve, confusion_matrix, roc_auc_score
from ipywidgets import VBox, HBox, interactive, FloatSlider

class plotLogistic(object):
    def __init__(self, x, y=None, n_samples=100, betas=None, positive=.5):
        if len(x) == 2 and y is None:
            self.c1, self.c2 = x
            x, y = plotLogistic.generate_samples(self.c1, self.c2, n_samples=n_samples, positive=positive)
        else:
            self.c1 = x[y==0].mean()
            self.c2 = x[y==1].mean()
        self.orig_x = x
        self.orig_y = y
        self.x = x
        self.y = y
        self.betas = betas
        if self.betas is None:
            self.logr = self.fit(self.x, self.y)
            self.coef_ = np.append(self.logr.intercept_, self.logr.coef_)
        self.yhat = self.predict(self.x, self.betas)
        self.positive, self.negative = self.plot_lines(x.min() - 1, x.max() + 1)
        self.positive_samples, self.negative_samples, _ = self.plot_samples(self.x, self.y)
        self.positive_hist, self.negative_hist, self.layout_hist = self.plot_samples(self.x, self.y, hist=True)
        self.prob_positive, self.prob_negative = self.plot_probabilities(self.x, self.y, self.yhat)
        self.regression = self.plot_regression(betas=self.betas)
        self.losses, self.mean_loss = self.plot_loss(self.x, self.y, self.yhat)
        self.roc = self.plot_roc()
        self.pr = self.plot_pr()
        self.cm = self.calc_cm()
        self.roc_thresh = self.plot_roc_thresh(thresh=.5)
        self.pr_thresh = self.plot_pr_thresh(thresh=.5)
        self.fp, self.fn = self.plot_falses(thresh=.5)
        self.thresh_line, self.sep_line = self.plot_threshold(thresh=.5)
        self.cm_thresh = self.plot_cm_thresh(thresh=.5)

    def recenter(self, cneg, cpos):
        x = self.x[:]

        diff1 = cneg - self.c1
        x[self.y==0] += diff1

        diff2 = cpos - self.c2
        x[self.y==1] += diff2

        self.__init__(x, self.y)

    @staticmethod
    def sigmoid_curve(x, b0, b1):
        return 1 / (1 + np.exp(-(b0 + b1 * x)))

    @staticmethod
    def plot_sigmoid_curve(x):
        fig = go.Figure(data=[go.Scatter(x=x, y=plotLogistic.sigmoid_curve(x, 0, 1), name='Sigmoid', line={'color': 'black'}),
                              go.Scatter(x=[x.min(), x.max()], y=[0, 0], name='Negative', line={'dash': 'dash', 'width': 4, 'color': 'red'}),
                              go.Scatter(x=[x.min(), x.max()], y=[1, 1], name='Positive', line={'dash': 'dash', 'width': 4, 'color': 'green'})],
                        layout={'title': 'Sigmoid'})
        f = go.FigureWidget(fig)

        def update_betas(beta0, beta1):
            f.data[0].y = plotLogistic.sigmoid_curve(f.data[0].x, beta0, beta1)

        beta0 = FloatSlider(description=r'\(b\)', value=0, min=-5.0, max=5.0, step=0.1)
        beta1 = FloatSlider(description=r'\(w_1\)', value=0.2, min=-5.0, max=5.0, step=0.1)

        vb = VBox((f, interactive(update_betas, beta0=beta0, beta1=beta1)))
        vb.layout.align_items = 'center'
        return vb

    @staticmethod
    def generate_samples(center_neg=-1, center_pos=1, n_samples=10, positive=.5):
        #y = np.random.randint(0, 2, size=n_samples)
        y = (np.random.rand(n_samples) >= (1 - positive)).astype(np.int)
        y_neg = y[y == 0]
        y_pos = y[y == 1]
        x_neg = np.random.randn(len(y_neg))
        x_neg -= x_neg.mean()
        x_neg += center_neg
        x_pos = np.random.randn(len(y_pos))
        x_pos -= x_pos.mean()
        x_pos += center_pos
        all_x = np.concatenate([x_neg, x_pos])
        all_y = np.concatenate([y_neg, y_pos])
        return all_x, all_y

    def fit(self, x, y):
        self.betas = None
        logr = LogisticRegression(solver='lbfgs', C=100)
        logr.fit(x.reshape(-1, 1), y)
        return logr

    def predict(self, x, betas=None):
        if betas is None:
            y_hat = self.logr.predict_proba(x.reshape(-1, 1))
        else:
            y_hat = plotLogistic.sigmoid_curve(x, betas[0], betas[1]).reshape(-1, 1)
            y_hat = np.concatenate([1 - y_hat, y_hat], axis=1)
        return y_hat

    def update_threshold(self, thresh):
        self.roc_thresh = self.plot_roc_thresh(thresh=thresh)
        self.pr_thresh = self.plot_pr_thresh(thresh=thresh)
        self.cm_thresh = self.plot_cm_thresh(thresh=thresh)

        self.fp, self.fn = self.plot_falses(thresh=thresh)
        self.thresh_line, self.sep_line = self.plot_threshold(thresh=thresh)

    @property
    def traces(self):
        return dict(positive=self.positive,
                    negative=self.negative,
                    positive_samples=self.positive_samples,
                    negative_samples=self.negative_samples,
                    prob_positive=self.prob_positive,
                    prob_negative=self.prob_negative,
                    regression=self.regression,
                    losses=self.losses,
                    mean_loss=self.mean_loss,
                    positive_hist=self.positive_hist,
                    negative_hist=self.negative_hist,
                    fp=self.fp,
                    fn=self.fn,
                    threshold=self.thresh_line,
                    separation=self.sep_line,
                    roc=self.roc,
                    pr=self.pr,
                    roc_thresh=self.roc_thresh,
                    pr_thresh=self.pr_thresh,
                    cm_thresh=self.cm_thresh)

    def plot_lines(self, xmin, xmax):
        positive = go.Scatter(x=[xmin, xmax], y=[0, 0], name='Negative', line={'dash': 'dash', 'width': 3, 'color': 'red'})
        negative = go.Scatter(x=[xmin, xmax], y=[1, 1], name='Positive', line={'dash': 'dash', 'width': 3, 'color': 'green'})
        return positive, negative

    def plot_samples(self, x, y, hist=False):
        xpos, xneg = x[y==1], x[y==0]
        ypos, yneg = np.ones_like(xpos), np.zeros_like(xneg)
        if not hist:
            positive = go.Scatter(x=xpos, y=ypos, mode='markers', name='Positive Samples',
                                  marker={'color': 'green', 'size': 15,
                                          'line': {'color': 'black', 'width': 2}})
            negative = go.Scatter(x=xneg, y=yneg, mode='markers', name='Negative Samples',
                                  marker={'color': 'red', 'size': 15,
                                          'line': {'color': 'black', 'width': 2}})
            layout = dict()
        else:
            positive = go.Histogram(x=xpos, name='Positive Samples', opacity=.65, xbins=dict(start=-6, end=6, size=.5), marker=dict(color='green'))
            negative = go.Histogram(x=xneg, name='Negative Samples', opacity=.65, xbins=dict(start=-6, end=6, size=.5), marker=dict(color='red'))
            layout = dict(barmode='overlay', yaxis2={'range': [0, 1.01], 'side': 'right', 'overlaying': 'y'})
        return positive, negative, layout

    def plot_regression(self, x_space=None, betas=None):
        if x_space is None:
            x_space = np.linspace(self.x.min() - 1, self.x.max() + 1, 201)
        if betas is None:
            sigmoid = self.logr.predict_proba(x_space.reshape(-1, 1))
            y = sigmoid[:, 1].ravel()
        else:
            y = plotLogistic.sigmoid_curve(x_space, betas[0], betas[1])
        curve = go.Scatter(x=x_space, y=y, name='Logistic Regression', mode='lines', marker={'color': 'black'})
        return curve

    def plot_probabilities(self, x, y, y_hat):
        positive = go.Bar(x=x[::-1], y=y_hat[:, 1].ravel()[::-1], name='Prob.Positive',
                          width=.2,
                          marker={'color': ['green' if v else 'rgba(0,0,0,0)' for v in y[::-1]],
                                  'line': {'width': 2, 'color': ['black' if v else 'rgba(0,0,0,0)' for v in y[::-1]]}})

        negative = go.Bar(x=x, y=y_hat[:, 0].ravel(), base=(y_hat[:, 1].ravel()),
                          width=.2, name='Prob.Negative',
                          marker={'color': ['rgba(0,0,0,0)' if v else 'red' for v in y],
                                  'line': {'width': 2, 'color': ['rgba(0,0,0,0)' if v else 'black' for v in y]}})
        return positive, negative

    def plot_loss(self, x, y, y_hat):
        loglosses = np.array([np.array([-np.log(yhat[y]), y]) for x, y, yhat in sorted(zip(x, y, y_hat))])
        losses = go.Bar(x=np.arange(1, loglosses.shape[0] + 1), y=loglosses[:, 0].ravel(), name='Loss',
                        marker={'color': ['green' if v else 'red' for v in loglosses[:, 1].ravel()],
                                'line': {'width': 2, 'color': 'black'}})
        avg = loglosses[:, 0].mean()
        mean_loss = go.Scatter(x=[0.5, loglosses.shape[0] + .5], y=[avg, avg], mode='lines', line={'dash': 'dash', 'color': 'black', 'width': 3}, name='Log Loss')
        return losses, mean_loss

    def plot_falses(self, thresh):
        reg = self.regression
        above = reg.y >= thresh
        if not np.any(above):
            above[-1] = True

        fp = [x for x, y in zip(self.x, (self.yhat[:, 1] >= thresh) & (1 - self.y)) if y]
        fn = [x for x, y in zip(self.x, (self.yhat[:, 1] < thresh) & self.y) if y]

        false_positive = go.Histogram(x=fp, name='False Positive', opacity=.85, xbins=dict(start=-6, end=6, size=.5), marker=dict(color='darkred'))
        false_negative = go.Histogram(x=fn, name='False Negative', opacity=.85, xbins=dict(start=-6, end=6, size=.5), marker=dict(color='darkgreen'))
        return false_positive, false_negative

    def plot_threshold(self, thresh):
        reg = self.regression
        above = reg.y >= thresh
        if not np.any(above):
            above[-1] = True
        xsep = reg.x[np.argmax(above)]

        thresh_line = go.Scatter(x=[-6, 6], y=[thresh, thresh], name='Threshold',
                                 mode='lines', yaxis='y4', line=dict(color='black', dash='dot'))
        sep_line = go.Scatter(x=[xsep, xsep], y=[0, 1], name='Separation', mode='lines',
                              yaxis='y4', line=dict(color='black', dash='dash'))
        return thresh_line, sep_line

    def plot_roc(self):
        self.fpr, self.tpr, self.roc_thresholds = roc_curve(y_true=self.y, y_score=self.yhat[:, 1])
        self.auc = roc_auc_score(y_true=self.y, y_score=self.yhat[:, 1])
        return go.Scatter(x=self.fpr, y=self.tpr, mode='lines', fill='tozeroy', name='ROC', line=dict(color='gray'))

    def plot_roc_thresh(self, thresh):
        above = thresh >= self.roc_thresholds
        if not np.any(above):
            above[-1] = True
        roc_thresh = np.argmax(above)
        return go.Scatter(x=[self.fpr[roc_thresh]], y=[self.tpr[roc_thresh]], name='Threshold',
                          mode='markers', marker={'size': 12, 'symbol': 'star', 'color': 'black'})

    def plot_pr(self):
        precision, recall, thresholds = precision_recall_curve(y_true=self.y, probas_pred=self.yhat[:, 1])
        self.precision = np.append([0], precision)
        self.recall = np.append([1], recall)
        self.pr_thresholds = np.append([0], thresholds)
        return go.Scatter(x=self.recall, y=self.precision, mode='lines', fill='tozeroy', name='PR', line=dict(color='gray'))

    def plot_pr_thresh(self, thresh):
        above = thresh >= self.pr_thresholds
        if np.all(above):
            above[-1] = False
        pr_thresh = np.argmin(above)
        if not np.any(above):
            pr_thresh = 0
        return go.Scatter(x=[self.recall[pr_thresh]], y=[self.precision[pr_thresh]], name='Threshold',
                          mode='markers', marker={'size': 12, 'symbol': 'star', 'color': 'black'})

    def plot_cm_thresh(self, thresh):
        tn, fp, fn, tp = self.cm
        above = thresh >= self.roc_thresholds
        idx = np.argmax(above)
        if not np.any(above):
            idx = -1
        df = pd.DataFrame({'Predicted Negative': [tn[idx], fn[idx]],
                           'Predicted Positive': [fp[idx], tp[idx]]},
                          index=['Negative', 'Positive'])
        trace = go.Table(
            header=dict(values=[''] + list(df.columns),
                        fill=dict(color='lightgray'),
                        align = ['center']),
            cells=dict(values=[df.index, df.iloc[:, 0], df.iloc[:, 1]],
                       fill=dict(color=['lightgray', 'white', 'white']),
                       align = ['center']))
        return trace

    def calc_cm(self):
        _, _, thresholds = roc_curve(y_true=self.y, y_score=self.yhat[:, 1])
        cm = [confusion_matrix(y_true=self.y, y_pred=(self.yhat[:, 1] > t).astype(np.int)) for t in thresholds]
        tn, fp, fn, tp = np.array([v.ravel() for v in cm]).T
        fp = np.append(fp, fp[-1] + tn[-1])
        tn = np.append(tn, 0)
        fn = np.append(fn, fn[-1])
        tp = np.append(tp, tp[-1])
        return tn, fp, fn, tp

def build_figure_fit(lr_obj):
    traces = lr_obj.traces

    fig = make_subplots(2, 3, specs=[[{'colspan': 2, 'rowspan': 2}, None, {}],
                                     [None, None, None]], subplot_titles=('Probabilities', 'Losses'), print_grid=False)
    fig.append_trace(traces['positive'], 1, 1)
    fig.append_trace(traces['negative'], 1, 1)
    fig.append_trace(traces['positive_samples'], 1, 1)
    fig.append_trace(traces['negative_samples'], 1, 1)
    fig.append_trace(traces['regression'], 1, 1)
    fig.append_trace(traces['prob_positive'], 1, 1)
    fig.append_trace(traces['prob_negative'], 1, 1)
    fig.append_trace(traces['losses'], 1, 3)
    fig.append_trace(traces['mean_loss'], 1, 3)

    f = go.FigureWidget(fig)

    f['layout'].update(title='Logistic Regression')
    f['layout']['yaxis'].update(range=[-0.05, 1.05])
    f['layout']['xaxis2']['visible'] = False
    f['layout']['autosize'] = False
    f['layout']['width'] = 900
    f['layout']['height'] = 500
    f['layout']['annotations'] = (*f['layout']['annotations'], dict(x=0, y=traces['mean_loss'].y[0], xref='x2', yref='y2', text='{:.4f}'.format(traces['mean_loss'].y[0])))

    names = ['positive', 'negative', 'positive_samples', 'negative_samples', 'regression', 'prob_positive', 'prob_negative', 'losses', 'mean_loss']

    def update(beta0, beta1):
        traces = plotLogistic(x=lr_obj.x, y=lr_obj.y, betas=(beta0, beta1)).traces
        values = {'regression': {'x': traces['regression'].x, 'y': traces['regression'].y},
                  'prob_positive': {'x': traces['prob_positive'].x, 'y': traces['prob_positive'].y},
                  'prob_negative': {'x': traces['prob_negative'].x, 'y': traces['prob_negative'].y,
                                    'base': traces['prob_positive'].y[::-1]},
                  'losses': {'x': traces['losses'].x, 'y': traces['losses'].y},
                  'mean_loss': {'x': traces['mean_loss'].x, 'y': traces['mean_loss'].y}}
        with f.batch_update():
            f['layout']['annotations'][2]['y'] = traces['mean_loss'].y[0]
            f['layout']['annotations'][2]['text'] = '{:.4f}'.format(traces['mean_loss'].y[0])
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

    beta0 = FloatSlider(description=r'\(b\)', value=0, min=-3.0, max=3.0, step=0.1)
    beta1 = FloatSlider(description=r'\(w_1\)', value=0, min=-5.0, max=5.0, step=0.1)

    return (f, interactive(update, beta0=beta0, beta1=beta1))

def build_figure_thresh(lr_obj):
    traces = lr_obj.traces

    fig = make_subplots(2, 3, specs=[[{'colspan': 2, 'rowspan': 2}, None, {}],
                                     [None, None, {}]],
                        subplot_titles=('Data', 'ROC Curve', 'PR Curve'),
                       horizontal_spacing=0.12, print_grid=False)

    fig.append_trace(traces['positive_hist'], 1, 1)
    fig.append_trace(traces['negative_hist'], 1, 1)
    fig.append_trace(traces['fp'], 1, 1)
    fig.append_trace(traces['fn'], 1, 1)
    fig.append_trace(traces['regression'], 1, 1)
    fig.append_trace(traces['threshold'], 1, 1)
    fig.append_trace(traces['separation'], 1, 1)
    fig.append_trace(traces['roc'], 1, 3)
    fig.append_trace(traces['roc_thresh'], 1, 3)
    fig.append_trace(traces['pr'], 2, 3)
    fig.append_trace(traces['pr_thresh'], 2, 3)

    fig.data[4].update(yaxis='y5')
    fig.data[5].update(yaxis='y5')
    fig.data[6].update(yaxis='y5')

    f = go.FigureWidget(fig)

    f['layout'].update(title='Logistic Regression')
    f['layout']['xaxis'].update(range=[-6, 6])
    f['layout']['autosize'] = False
    f['layout']['width'] = 900
    f['layout']['height'] = 500
    f['layout']['barmode'] = 'overlay'
    f['layout']['yaxis'].update(range=(0, np.maximum(np.histogram(bins=list(np.linspace(-6, 6, 21)),
                                                       a=traces['negative_hist'].x)[0].max(),
                                                     np.histogram(bins=list(np.linspace(-6, 6, 21)),
                                                       a=traces['positive_hist'].x)[0].max())))
    f['layout']['yaxis5'] = {'overlaying': 'y', 'range': [0, 1.01], 'side': 'right'}
    f['layout'].update(xaxis2=dict(title='FPR'))
    f['layout'].update(yaxis2=dict(title='TPR'))
    f['layout'].update(yaxis3=dict(title='Precision'))
    f['layout'].update(xaxis3=dict(title='Recall'))

    names = ['positive_hist', 'negative_hist', 'fp', 'fn', 'regression', 'threshold', 'separation', 'roc', 'roc_thresh', 'pr', 'pr_thresh']

    trace2 = lr_obj.plot_cm_thresh(.5)
    fig2 = go.Figure([trace2])
    fig2['layout']['autosize'] = False
    fig2['layout']['width'] = 400
    fig2['layout']['height'] = 300
    f2 = go.FigureWidget(fig2)
    f2['layout']['margin'] = dict(l=50, r=50, t=10, b=10)

    def update(threshold, cneg, cpos):
        lr_obj.recenter(cneg, cpos)
        lr_obj.update_threshold(threshold)
        traces = lr_obj.traces
        values = {k: {'x': traces[k].x, 'y': traces[k].y} for k in names}
        with f.batch_update():
            for i, data in enumerate(f.data):
                f['layout']['annotations'][1]['text'] = 'ROC Curve / AUC = {:.3f}'.format(lr_obj.auc)

                try:
                    if names[i] in ['positive_hist', 'negative_hist', 'fp', 'fn']:
                        data.xbins=dict(start=-5, end=5, size=.5)
                except KeyError:
                    pass

                if names[i] in ['regression', 'threshold', 'separation']:
                    data.yaxis = 'y5'

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

        trace = lr_obj.plot_cm_thresh(threshold)
        with f2.batch_update():
            f2.data[0]['cells']['values'] = trace['cells']['values']

    threshold = FloatSlider(description='Threshold', value=0.5, min=0, max=1.0, step=0.01)
    cneg = FloatSlider(description='Neg.Center', value=-1, min=-3, max=0, step=.2)
    cpos = FloatSlider(description='Pos.Center', value=1, min=0, max=3, step=.2)

    return (f, HBox((f2, interactive(update, threshold=threshold, cneg=cneg, cpos=cpos))))

if __name__ == '__main__':
    mylr = plotLogistic(x=(-2, 1), n_samples=8, betas=(2, 1))
    vb1 = VBox(build_figure_fit(mylr))
    vb1.layout.align_items = 'center'

    mylr2 = plotLogistic(x=(-1, 1), n_samples=500)
    vb2 = VBox(build_figure_thresh(mylr2))
    vb2.layout.align_items = 'center'
