"""This module includes functions to format output displays of
PairedCompResultSet data,
in either graphic or textual form.

Some formatting details are defined by module global variables,
which can be easily changed by users.

*** Version History:

2018-02-06, simplified table generation, generate only one selected table type
2018-02-18, use module variable FMT['table_format'] where needed
2018-04-19, minor changes to include population quality params
2018-08-11, minor cleanup

2018-08-29, fix percent sign switch by table_format
2018-10-02, use general FMT dict, fix table file suffix
2018-10-08, allow cat_limits in fig_percentiles and fig_indiv_boxplot
2018-11-24, changed 'x_label' to 'tested_objects' in FMT params
2019-03-27, include marginal credibility values in percentile tables
"""

import numpy as np
from itertools import cycle
import matplotlib.pyplot as plt
import logging

plt.rcParams.update({'figure.max_open_warning': 0})
# suppress warning for many open figures

logger = logging.getLogger(__name__)


# --------------------------- Default format parameters:
FMT = {'colors': 'rbgk',  # to separate results in plots
       'markers': 'oxs*_',
       'table_format': 'latex',  # or 'tab' for tab-delimited tables
       'figure_format': 'eps',   # or 'png', or 'pdf', for saved plots
       'credibility': 'Credibility',  # heading in tables
       'tested_objects': 'Tested Objects',  # x_axis plot label
       'attribute': 'Attribute',  # heading in tables
       'group': 'Group',  # heading in tables
       'correlation': 'Correlation',  # heading in tables
       'significance': 'Signif.'  # heading in Likelihood Ratio result table
       }
# = module-global dict with default settings for display details
# that may be changed by user

TABLE_FILE_SUFFIX = {'latex': '.tex', 'tab': '.txt'}
# = mapping table_format -> file suffix


def set_format_param(**kwargs):
    """Set / modify module-global format parameters
    :param kwargs: dict with format variables
        to replace the default values in FMT
    :return: None
    """
    for (k, v) in kwargs.items():
        k = k.lower()
        if k not in FMT:
            logger.warning(f'Format setting {k}={repr(v)} is not known, not used')
        FMT[k] = v


def _percent():
    """Percent sign for tables
    :return: str
    """
    return '\%' if FMT['table_format'] == 'latex' else '%'


# ---------------------------- Main Result Classes
class FigureRef():
    """Reference to a single graph instance
    """
    def __init__(self, ax, path=None, name=None):
        """
        :param ax: Axes instance containing the graph
        :param path: Path to directory where figure has been saved
        :param name: (optional) updated name of figure file
        """
        self.ax = ax
        self.path = path
        self.name = name

    def __repr__(self):
        return (f'FigureRef(ax= {repr(self.ax)}, ' +
                f'path= {repr(self.path)}, name= {repr(self.name)})')

    @property
    def fig(self):
        return self.ax.figure

    def save(self, path, name=None):
        """Save figure to given path
        :param path: Path to directory where figure has been saved
        :param name: (optional) updated name of figure file
        :return: None
        Result: updated properties path, name
        """
        if name is None:
            name = self.name
        path.mkdir(parents=True, exist_ok=True)
        f = (path / name).with_suffix('.' + FMT['figure_format'])
        self.fig.savefig(str(f))
        self.path = path
        self.name = f.name


class TableRef():
    """Reference to a single table instance,
    formatted in LaTeX OR plain tabulated txt versions
    """
    def __init__(self, text=None, path=None, name=None):
        """
        :param text: single string with all table text
        :param path: (optional) Path to directory where tables are saved
        :param name: (optional) updated file name, with or without suffix
            suffix is determined by FMT['table_format'] anyway
        """
        # store table parts instead *****???
        self.text = text
        self.path = path
        self.name = name

    def __repr__(self):
        return (f'TableRef(text= text, ' +    # fmt= {repr(self.fmt)}, ' +
                f'path= {repr(self.path)}, name= {repr(self.name)})')

    def save(self, path, name=None):
        """Save table to file.
        :param path: Path to directory where tables are saved
        :param name: (optional) updated file name, with or without suffix
            suffix is determined by FMT['table_format'] anyway
        :return: None
        Result: updated properties path, name
        """
        if name is None:
            name = self.name
        path.mkdir(parents=True, exist_ok=True)   # just in case
        f = (path / name).with_suffix(TABLE_FILE_SUFFIX[FMT['table_format']])
        if self.text is not None and len(self.text) > 0:
            f.write_text(self.text, encoding='utf-8')
        self.path = path
        self.name = f.name


# ---------------------------------------- Formatting functions:
def fig_percentiles(perc_0,
                    y_label,
                    s_labels,
                    y_unit='',
                    cat_limits=None,
                    perc_1=None,
                    case_tuple=None,    # case_head, case_labels like tab_percentiles_3d  ???
                    x_label=None,
                    x_offset=0.1,
                    x_space=0.5, **kwargs):
    """create a figure with quality percentile results
    :param perc_0: primary percentile data,
        2D or 3D array with three (min, median, max) quality percentiles, arranged as
        perc_0[i, c, s] = i-th percentile for s_labels[..., s] result, c-th case variant, OR
        perc_0[i, s] if no case variants are included
    :param y_label: string for y-axis label
    :param y_unit: (optional) additional string for unit of y_label
    :param s_labels: list of strings with labels for x_ticks, one for each value in rows perc_0[..., :]
        len(s_labels) == perc_0.shape[-1]
    :param cat_limits: 1D array with response-interval limits (medians)
    :param perc_1: (optional) 2D or 3D array with quantiles for population mean
    :param x_label: (optional) string for x-axis label
    :param case_tuple: (optional) tuple (case_head, case_labels) for case variants
        len(case_labels) == perc_0.shape[-2] if perc_0.ndim == 3 else case_labels not used
    :param x_offset: (optional) space between case-variants of plots for each x_tick
    :param x_space: (optional) min space outside min and max x_tick values
    :param kwargs: (optional) dict with any additional keyword arguments for plot commands.

    :return: fig object with single plot axis with all results

    2018-04-19, allow perc_1 input
    2018-10-08, new cat_limits parameter
    """
    if x_label is None:
        x_label = FMT['tested_objects']
    if perc_1 is None:
        pop_y = perc_0 + 0.  # must have a copy for easier code
    else:
        pop_y = perc_1
    fig, ax = plt.subplots()
    if perc_0.ndim == 2:
        perc_0 = perc_0[np.newaxis, ...]
        pop_y = pop_y[np.newaxis, ...]
    else:
        perc_0 = perc_0.transpose((1, 0, 2))
        pop_y = pop_y.transpose((1, 0, 2))
    # now indexed as perc_0[case, quantile, system]
    if case_tuple is None:
        case_tuple = ('', [''])
    (case_head, case_labels) = case_tuple
    assert perc_0.shape[2] == len(s_labels), 'mismatching system labels'
    assert perc_0.shape[0] == len(case_labels), 'mismatching case labels'
    x = np.arange(0., len(s_labels)) - x_offset * (len(case_labels) - 1) / 2
    for (y, y_p, c_label, c, m) in zip(perc_0, pop_y, case_labels,
                                       cycle(FMT['colors']), cycle(FMT['markers'])):
        ax.plot(np.tile(x, (2, 1)),
                y[[0, 2], :],
                linestyle='solid', color=c, **kwargs)
        ax.plot(x, y[1,:], linestyle='',
                marker=m, markeredgecolor=c, markerfacecolor='w',
                label=c_label, **kwargs)
        if perc_1 is not None:
            # ax.plot(np.tile(x, (2, 1)),  # *** population range with thicker line
            #         y_p[[0, 2], :],
            #         linestyle='solid', linewidth=2, color=c, **kwargs)
            ax.plot(np.tile(x, (2, 1)),  # *** only markers for population credible range
                    y_p[[0, 2], :],
                    linestyle='',
                    marker='_', markeredgecolor=c, markerfacecolor='w', markersize=20,
                    # *** or marker = m ???
                    **kwargs)
        x += x_offset
    (x_min, x_max) = ax.get_xlim()
    x_min = min(x_min, -x_space)
    x_max = max(x_max, len(s_labels) - 1 + x_space)
    ax.set_xlim(x_min, x_max)
    if cat_limits is not None:
        _plot_response_intervals(ax, cat_limits)
    ax.set_xticks(np.arange(len(s_labels)))
    ax.set_xticklabels(s_labels)
    ax.set_ylabel(y_label + ' (' + y_unit + ')')
    ax.set_xlabel(x_label)
    if np.any([len(l) > 0 for l in case_labels]):
        ax.legend(loc='best')
    # if SHOW_FIGURE:
    #     plt.show()
    # if case_labels is None or case_labels == '':
    #     f_name = y_label
    # else:
    #     f_name = y_label + '_' + '_'.join(tc[0] for tc in case_labels)
    f_name = y_label + ('_' + case_head if len(case_head) > 0 else '')
    return FigureRef(ax, name=f_name)


def fig_indiv_boxplot(q,
                      y_label,
                      s_labels,
                      y_unit='',
                      cat_limits=None,
                      case_tuple=None,
                      x_label=None,
                      x_space=0.5,
                      **kwargs):
    """create a figure with boxplot of individual results
    :param q: 2D array or list of 2D arrays,
        with individual quality estimates, arranged as
        q[c][i, s] = i-th individual result for s_labels[s], in c-th case variant, OR
        q[i, s] if no case variants
    :param y_label: string for y-axis label
    :param s_labels: list of strings with labels for x_ticks, one for each value in rows q[..., :]
        len(s_labels) == q.shape[-1]
    :param y_unit: (optional) additional string for unit of y_label
    :param cat_limits: (optional) 1D array with response-interval limits (medians)
    :param case_tuple: (optional) tuple (case_head, case_labels) for case variants
        len(case_labels) == perc_0.shape[-2] if perc_0.ndim == 3 else case_labels not used
    :param x_label: (optional) string for x-axis label
    :param x_space: (optional) min space outside min and max x_tick values
    :param kwargs: (optional) dict with any additional keyword arguments for boxplot command.

    :return: FigureRef object with single plot axis with all results

    2018-10-08, new cat_limits parameter
   """
    if len(q) <= 1:
        return None  # boxplot does not work
    if x_label is None:
        x_label = FMT['tested_objects']
    fig, ax = plt.subplots()
    if case_tuple is None:
        assert q.ndim == 2, 'Input must be 2D if no case variants'
        case_tuple = ('', [''])
        q = [q]
        # make it a list of 2D arrays
    (case_head, case_labels) = case_tuple
    x_offset = min(0.2, 0.8 / len(case_labels))
    if len(case_labels) > 1:
        box_width = 0.8 * x_offset
    else:
        box_width = 0.5
    x_pos = np.arange(len(s_labels)) - x_offset * (len(case_labels) - 1) / 2
    for (y, c_label, c, m) in zip(q, case_labels, cycle(FMT['colors']), cycle(FMT['markers'])):
        boxprops = dict(linestyle='-', color=c)
        # flierprops = dict(marker=m, markeredgecolor=c, markerfacecolor='w', # *** markersize=12,
        #                   linestyle='none')
        whiskerprops = dict(marker='', linestyle='-', color=c)
        capprops = dict(marker='', linestyle='-', color=c)
        medianprops = dict(linestyle='-', color=c)
        ax.boxplot(y, positions=x_pos,
                   widths=box_width,
                   sym='',  # ******** no fliers
                   boxprops=boxprops,
                   medianprops=medianprops,
                   whiskerprops=whiskerprops,
                   capprops=capprops,
                   **kwargs)
        median = np.median(y, axis=0)
        ax.plot(x_pos, median, linestyle='',
                marker=m, markeredgecolor=c, markerfacecolor='w',
                label=c_label)
        x_pos += x_offset

    (x_min, x_max) = ax.get_xlim()
    x_min = min(x_min, -x_space)
    x_max = max(x_max, len(s_labels) -1 + x_space)
    ax.set_xlim(x_min, x_max)
    if cat_limits is not None:
        _plot_response_intervals(ax, cat_limits)
    ax.set_xticks(np.arange(len(s_labels)))
    ax.set_xticklabels(s_labels)
    ax.set_ylabel(y_label + ' (' + y_unit + ')')
    ax.set_xlabel(x_label)
    if np.any([len(l) > 0 for l in case_labels]):
        ax.legend(loc='best')
    # if SHOW_FIGURE:
    #     plt.show()
    f_name = y_label + '-box' + ('_' + case_head if len(case_head) > 0 else '')
    return FigureRef(ax, name=f_name)


def _plot_response_intervals(ax, c_lim):
    """plot horizontal lines to indicate response-category intervals
    :param ax: axis object
    :param c_lim: 1D array with scalar interval limits
    :return: None
    """
    (x_min, x_max) = ax.get_xlim()
    y = list(c_lim) + list(-c_lim)
    return ax.hlines(y, x_min, x_max, linestyle='solid', linewidth=0.2)


# ----------------------------------------- table displays:

def tab_percentiles(q, cdf, perc, y_label, s_labels, s_head):
    """create table with quality percentile results,
    in LaTeX tabular and in simple tab-separated text format
    :param q: 2D array with three (min, median, max) quality percentiles, arranged as
        q[p, s] = p-th percentile for s_label[i]
    :param cdf: 1D array with cumulative distribution value at zero,
        cdf[i] = probability quality <= 0 for s_label[i]
    :param perc: list of three (min, median, max) percentage values in range 0-100.
    :param y_label: string with label of tabulated percentile
    :param s_labels: list of strings with labels corresponding to q[..., :]
        len(s_labels) == q.shape[-1]
    :param s_head: single string printed over column with s_labels

    :return: TableRef object with header lines + one line for each s_labels element,

    2019-03-27, include columns with probabilities <=0 and >0, from given cdf
    """
    align = ['l', 'r', 'r', 'r', 'r', 'r']
    h = [s_head] + [f'{p:.0f}' + _percent() for p in perc] + ['<=0', '>0']
    rows = [[s] + [f'{p:.2f}' for p in p_s] +
            [f'{p_0*100:.0f}' + _percent(), f'{(1.-p_0)*100:.0f}' + _percent()]
            for (s, p_s, p_0) in zip(s_labels, q.T, cdf)]
    return TableRef(_make_table(h, rows, align), name=y_label)


def tab_percentiles_3d(q,
                       cdf,
                       perc,
                       y_label,
                       s_head,
                       s_labels,
                       case_head,
                       case_labels):
    """create table with quality percentile results,
    in LaTeX tabular and in simple tab-separated text format
    :param q: 3D array with three (min, median, max) quality percentiles, arranged as
        q[p, c, s] = p-th percentile for s_label[s] in c-th case condition
    :param cdf: 2D array with cumulative distribution values at zero,
        cdf[c, s] = probability that quality <= 0 for s_label[s] in c-th case condition
    :param perc: list of three (min, max, median) percentage values in range 0-100.
    :param y_label: single string with label of tabulated percentiles
    :param s_head: single string printed over column with s_labels
    :param s_labels: list of strings with labels corresponding to q[..., :]
        len(s_labels) == q.shape[2]
    :param case_labels: list of dicts with elements (case_head, case_label)
        corresponding to q[p, :, s], each yielding one table row
        len(case_labels) == q.shape[1]
        case_head are the same for each list element
    :param case_head: list of case factors, one for each column
        len(case_head) == len(case_labels[i]) for each i
    :return: TableRef object, with header + one line for each case_labels element
    2018-10-05, cleanup, case_head, case_labels as dict, one column per case_head
    2018-10-07, s_head mandatory argument
    2019-03-27, include columns with probabilities <=0 and >0, from given cdf
    """
    def make_row(s, c, q, p_0):
        """make cells for one table row
        :param s: system label
        :param c: case tuple
        :param q: percentile values
        :param p_0: scalar probability q <= 0
        :return: row = list with cells
            len(row) == 1 + len(c) + len(q) + 2
        """
        c_dict = dict(c)
        return ([s] + [c_dict[c_head]
                      for c_head in case_head] + [f'{p:.2f}' for p in q] +
                [f'{p_0*100:.0f}' + _percent(), f'{(1.-p_0)*100:.0f}' + _percent()])
    # --------------------------------------------------------------------
    align = ['l', len(case_head) * 'l', len(perc) * 'r', 2 * 'r']
    h = [s_head, *case_head] + [f'{p:.0f}' + _percent() for p in perc] + ['<=0', '>0']
    q = q[:,:,1:].transpose((1, 2, 0))
    # indexed as q[case, object, percentile], excluding system[0]
    # skipping 0-th object
    rows = []
    for (c, q_c, cdf_c) in zip(case_labels, q, cdf[:, 1:]):
        for (s, q_s, p_s) in zip(s_labels[1:], q_c, cdf_c):
            rows.append(make_row(s, c, q_s, p_s))
    f_name = y_label + '_' + '_'.join(case_head)
    return TableRef(_make_table(h, rows, align), name=f_name)


def tab_credible_diff(diff,
                      y_label,
                      diff_labels,
                      diff_head):
    """create table with credible differences among quality results
    :param diff: list of tuples ((i,j), p) defining jointly credible differences, indicating that
        prob{ quality of s_labels[i] > quality of s_labels[j] } AND all previous pairs } == p
    :param y_label: string with label of tabulated quality attribute
    :param diff_head: single string printed over column with pairs of s_labels
    :param diff_labels: list of strings with labels of compared random-vector elements,
        len(s_labels) == diff.shape[-1]

    :return: TableRef object with header lines + one line for each credible difference,
    """
    if len(diff) == 0:
        return None
    align = ['l', 'l', 'c', 'l', 'r']
    h = ['', diff_head, '>', diff_head, FMT['credibility']]
    rows = []
    col_0 = ''
    # ((i,j), p) = diff[0]  # separate format for first line
    for ((i, j), p) in diff:
        rows.append([col_0, diff_labels[i], '>', diff_labels[j], f'{100*p:.1f}'])
        col_0 = 'AND' # for all except first row
    f_name = y_label + '-diff'
    return TableRef(_make_table(h, rows, align), name=f_name)


def tab_credible_diff_3d(diff,
                         y_label,
                         diff_head,
                         diff_labels,
                         case_head,
                         case_labels):
    """create table with credible differences among quality results
    in LaTeX tabular and in simple tab-separated text format
    :param diff: list of tuples ((i, j, c), p) defining jointly credible differences, indicating that
        prob{ quality of diff_labels[i] > quality of diff_labels[j]  in case_label[c]
            AND same for all previous tuples in the lise } = p
    :param y_label: string with label of tabulated quality attribute
    :param diff_head: list of column headings for factors compared
    :param diff_labels: list of dicts, one for each credible difference (each table row)
        each with elements (diff_head, diff_label) with categories
    :param case_head: list of case_key strings, for column headings of background factors
    :param case_labels: list of dicts, one for each credible difference (each table row)
        each with elements (case_key, case_label) with categories
        for which the credible difference was found.

    :return: TableRef object with header lines + one line for each credible difference,
    """
    def make_cells(i, j, c):
        row = ([diff_labels[i][s_head]
                for s_head in diff_head] + ['>'] +
               [diff_labels[j][s_head]
                for s_head in diff_head] +
               [case_labels[c][c_head]
                for c_head in case_head])
        return row
    # --------------------------------------------------------------------------------

    if len(diff) == 0:
        return None
    align = ('l' + len(diff_head) * 'l' + 'c' + len(diff_head) * 'l' +
             len(case_head) * 'l' + 'r')
    h = ['', *diff_head, '>', *diff_head, *case_head, FMT['credibility']]
    rows = []
    col_0 = ''
    for ((i, j, c), p) in diff:
        rows.append([col_0, *make_cells(i, j, c), f'{100*p:.1f}'])
        col_0 = 'AND'  # for all except first row
    f_name = y_label + '-diff_' + '_'.join(diff_head)
    return TableRef(_make_table(h, rows, align), name=f_name)


def tab_credible_corr(c, a_labels):
    """create table of credible correlations
    :param c: list of tuple((i, j), p, md_corr), where
        (i, j) are indices into a_labels,
        p is joint credibility,
        md_corr = median conditional correlation value, given all previous
    :param a_labels: list with string labels for correlated attributes
    :return: TableRef object with header + one row for each credible correlation
    """
    if len(c) == 0:
        return None
    align = ['l', 'l', 'c', 'l', 'r', 'r']
    h = [_make_cell(FMT['attribute'], 4, FMT['table_format']),
         FMT['correlation'], FMT['credibility']]
    rows = []
    col_0 = ''
    for ((i, j), p, mdc) in c:
        rows.append([col_0, a_labels[i], '*', a_labels[j], f'{mdc:.2f}', f'{100*p:.1f}'])
        col_0 = 'AND'
    return TableRef(_make_table(h, rows, align), name='Correlation')


def tab_lr_test(lr_result):
    """Create TableRef with all likelihood ratio test results
    :param lr_result: nested dict with elements
        lr_result[group][attr] = pc_lr_test.LikelihoodRatioResult
    :return: TableRef instance
    """
    align = 'llrrrr'
    h = [FMT['group'], FMT['attribute'], 'Chi-2', 'df', 'p', FMT['significance']]
    rows = []
    for (g, g_result) in lr_result.items():
        for (a, lr) in g_result.items():
            p = f'{100*lr.pvalue:.1f}' + _percent()
            if lr.pvalue < 0.001:
                p = f'{lr.pvalue:.2g}'
                s = '***'
            elif lr.pvalue < 0.01:
                s = '**'
            elif lr.pvalue < 0.05:
                s = '*'
            else:
                s = '-'
            ga = f'Group {repr(g)}, Attribute {a}: '
            logger.info(ga + f'chi2(df={lr.df}) = {lr.statistic:.3f}: p= {p}. Signif.: {s}')
            rows.append([g, a, f'{lr.statistic:.2f}', f'{lr.df}', p, s])
    return TableRef(_make_table(h, rows, align), name='LR_significance_test')


# ------------------------------------------ internal help functions:
# more variants may be added for other table formats

table_begin = {'latex': lambda align: '\\begin{tabular}{' + ' '.join(c for c in align) + '}\n',
               'tab': lambda align: ''}
table_head_sep = {'latex':'\hline\n',
                  'tab':''}
table_cell_sep = {'latex': ' & ',
                  'tab':' \t '}
table_row_sep = {'latex': '\\\\ \n',
                 'tab': '\n'}
table_end = {'latex':'\hline\n\end{tabular}',
             'tab': ''}


def _make_cell(text, col_span, fmt):
    """Format multi-column table cell, usually only for header line
    :param text: cell contents
    :param col_span: number of columns to span
    :param fmt: str key for table format
    :return: string with latex or plain cell contents
    """
    if fmt == 'latex' and col_span > 1:
        return '\multicolumn{' + f'{col_span}' + '}{c}' + '{' + text + '}'
    else:
        return text


def _make_table(header, rows, col_alignment):
    """Generate a string with table text.
    Input:
    :param header: list with one string for each table column
    :param rows: list of rows, ehere
        each row is a list of string objects for each column in this row
    :param col_alignment: list of alignment symbols, l, r, or c
        len(col_alignment) == len(header) == len(row), for every row in rows

    :return: single string with complete table
    """
    def make_row(cells, fmt):
        return table_cell_sep[fmt].join(f'{c}' for c in cells) + table_row_sep[fmt]
    # ------------------------------------------------------------------------

    fmt = FMT['table_format']  # module global constant
    t = table_begin[fmt](col_alignment)
    t += table_head_sep[fmt]
    t += make_row(header, fmt)
    t += table_head_sep[fmt]
    t += ''.join((make_row(r, fmt) for r in rows))
    t += table_end[fmt]
    return t