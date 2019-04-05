# Copyright (c) 2016-2017, System Engineering Software Society
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the System Engineering Software Society nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.
# IN NO EVENT SHALL SYSTEM ENGINEERING SOFTWARE SOCIETY BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import numpy as np

from sympathy import api
from sympathy.api import node as synode
from sympathy.api import qt2 as qt_compat
from sympathy.api import node_helper
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags, adjust

from sympathy.utils import preview

from sylib.figure import drawing, gui, mpl_utils

QtCore = qt_compat.QtCore
QtGui = qt_compat.QtGui
qt_compat.backend.use_matplotlib_qt()


class FigureCompressor(synode.Node):
    """
    Compress a list of Figures into one Figure.

    :Ref. nodes: :ref:`Figure`
    """

    author = 'Benedikt Ziegler'
    version = '0.3'
    icon = 'figurecompressor.svg'
    name = 'Figure Compressor'
    description = 'Compress a list of Figures to a single Figure'
    nodeid = 'org.sysess.sympathy.visualize.figurecompressorgui'
    tags = Tags(Tag.Visual.Figure)

    parameters = synode.parameters()
    parameters.set_list(
        'parent_figure', label='Parent figure:',
        description='Specify the figure from which axes parameters '
                    'and legend position are copied.',
        editor=synode.Util.combo_editor())
    parameters.set_boolean(
        'join_legends', value=True, label='Join legends',
        description='Set if legends from different axes should be '
                    'joined into one legend.')
    parameters.set_list(
        'legend_location', value=[0], label='Legend position:',
        plist=list(mpl_utils.LEGEND_LOC.keys()) + mpl_utils.OUTSIDE_LEGEND_LOC,
        description='Defines the position of the joined legend.',
        editor=synode.Util.combo_editor())
    parameters.set_boolean(
        'join_colorbars', value=False, label='Make first colorbar global',
        description='If checked, the colorbar from the first figure becomes '
                    'a global colorbar in the output figure.')
    parameters.set_boolean(
        'auto_recolor', value=False, label='Auto recolor',
        description='Automatically recolor all artists to avoid using a color '
                    'multiple times, if possible.')
    parameters.set_boolean(
        'auto_rescale', value=True, label='Auto rescale axes',
        description='Automatically rescale all axes to fit the visible data.')

    controllers = (
        synode.controller(
            when=synode.field('join_legends', 'checked'),
            action=synode.field('legend_location', 'enabled')))

    inputs = Ports([Port.Figures('List of Figures', name='input')])
    outputs = Ports([Port.Figure(
        'A Figure with the configured axes, lines, labels, etc',
        name='figure')])

    def adjust_parameters(self, node_context):
        adjust(node_context.parameters['parent_figure'],
               node_context.input['input'],
               lists='index')

    def execute(self, node_context):
        input_figures = node_context.input['input']
        output_figure = node_context.output['figure']
        parameters = node_context.parameters

        try:
            parent_figure_number = parameters['parent_figure'].value[0]
        except IndexError:
            parent_figure_number = 0

        input_axes = [figure.get_mpl_figure().axes for figure in input_figures]
        default_output_axes = output_figure.first_subplot().get_mpl_axes()

        axes_colorbars = drawing.compress_axes(
            input_axes, default_output_axes,
            parameters['join_legends'].value,
            parameters['legend_location'].selected,
            int(parent_figure_number),
            auto_recolor=parameters['auto_recolor'].value,
            auto_rescale=parameters['auto_rescale'].value,
            add_colorbars=not parameters['join_colorbars'].value)

        if parameters['join_colorbars'].value:
            drawing.add_global_colorbar(axes_colorbars, output_figure)


class SubplotFigures(synode.Node):
    """
    Layout the Figures in a list of Figures into subplots.

    The number of rows and columns is automatically adjusted to an approximate
    square. Empty axes in a non-empty row will be not shown.

    :Ref. nodes: :ref:`Figure`
    """

    author = 'Benedikt Ziegler'
    version = '0.2'
    icon = 'figuresubplots.svg'
    name = 'Layout Figures in Subplots'
    description = 'Layout a list of Figures in a Subplot'
    nodeid = 'org.sysess.sympathy.visualize.figuresubplot'
    tags = Tags(Tag.Visual.Figure)

    inputs = Ports([Port.Figures('List of Figures', name='input')])
    outputs = Ports([Port.Figure(
        'A Figure with several subplot axes', name='figure')])

    parameters = synode.parameters()
    parameters.set_integer(
        'rows', value=0, label='Number of rows (0 = best):',
        description='Specify the number of rows. 0 optimizes to fit all '
                    'figures. If rows and columns are 0, the axes layout '
                    'will be approximately square.',
        editor=synode.Util.bounded_spinbox_editor(0, 100, 1))
    parameters.set_integer(
        'columns', value=0, label='Number of columns (0 = best):',
        description='Specify the number of columns. 0 optimizes to fit all '
                    'figures. If rows and columns are 0, the axes layout '
                    'will be approximately square.',
        editor=synode.Util.bounded_spinbox_editor(0, 100, 1))
    parameters.set_boolean(
        'recolor', value=False, label='Auto recolor',
        description='Specify if artists should be assigned new colors '
                    'automatically to prevent duplicate colors.')
    parameters.set_boolean(
        'remove_internal_ticks', value=False, label='Remove internal ticks',
        description='If checked, remove ticklabels from any axis between two '
                    'subplots.')
    parameters.set_boolean(
        'join_colorbars', value=False, label='Make first colorbar global',
        description='If checked, the colorbar from the first subplot is '
                    'treated as a global colorbar valid for all subplots.')
    parameters.set_boolean(
        'join_legends', value=False, label='Make first legend global',
        description='If checked, the legend(s) in the first subplot are '
                    'treated as global legends valid for all subplots.')

    def execute(self, node_context):
        input_figures = node_context.input['input']
        output_figure = node_context.output['figure']
        parameters = node_context.parameters
        rows = parameters['rows'].value
        cols = parameters['columns'].value
        auto_recolor = parameters['recolor'].value
        global_colorbar = parameters['join_colorbars'].value
        global_legend = parameters['join_legends'].value
        remove_internal_ticks = parameters['remove_internal_ticks'].value

        # calculate the number of rows and columns if any is =0
        nb_input_figures = len(input_figures)
        if rows == 0 and cols == 0:
            rows = int(np.ceil(np.sqrt(nb_input_figures)))
            cols = int(np.ceil(np.sqrt(nb_input_figures)))
            if rows * cols - cols >= nb_input_figures > 0:
                rows -= 1
        elif rows == 0 and cols > 0:
            rows = int(np.ceil(nb_input_figures / float(cols)))
        elif rows > 0 and cols == 0:
            cols = int(np.ceil(nb_input_figures / float(rows)))

        subplots = np.array(output_figure.subplots(rows, cols)).ravel()

        figure_colorbars = []

        for i, (subplot, input_figure) in enumerate(
                zip(subplots, input_figures)):
            default_axes = subplot.get_mpl_axes()
            input_axes = [axes.get_mpl_axes() for axes in input_figure.axes]

            if remove_internal_ticks:
                subplot_mpl = subplot.get_mpl_axes()
                remove_ticklabels = (
                    not subplot_mpl.is_first_row(),
                    not subplot_mpl.is_last_col(),
                    not subplot_mpl.is_last_row(),
                    not subplot_mpl.is_first_col())
            else:
                remove_ticklabels = None

            axes_colorbars = drawing.compress_axes(
                [input_axes], default_axes,
                legends_join=False,
                legend_location='best',
                copy_properties_from=0,
                auto_recolor=auto_recolor,
                auto_rescale=False,
                add_colorbars=not global_colorbar,
                add_legends=(i == 0 or not global_legend),
                remove_ticklabels=remove_ticklabels)

            if axes_colorbars:
                figure_colorbars.append(axes_colorbars)

        if global_colorbar and len(figure_colorbars):
            drawing.add_global_colorbar(
                figure_colorbars[0], output_figure)

        # don't show empty axes
        if len(subplots) > len(input_figures):
            for ax_to_blank in subplots[len(input_figures):]:
                ax_to_blank.set_axis(False)


class Figure(synode.Node):
    """
    The configuration for this node consists of a tree view containing all the
    parts of your figure. To add plots to the figure, you can either click on
    its corresponding button in the toolbar, or press on a plot button and
    dragging it to where in the tree view you want it (possible drop locations
    will be shown in green). The plot will be added with some basic properties
    depending on which plot type you added (e.g. *X Data* and *Y Data* for line
    plot). Almost all configuration items support more than the default
    properties. To add more, right-click on a configuration item and choose
    "Add...".

    Some common plots
    =================
    There are many types of plots available in the Figure node. Here follows a
    short word about some of more common ones.

    Scatter plots and line plots
    ----------------------------
    These plot types are mostly pretty self-explanatory. The main difference
    between these is while a *Line plot* can have marker, a *Scatter plot* can
    not have lines. The *Scatter plot* can on the other hand have a different
    size and color for each marker, whereas *Line plot* can only have a single
    color and size for all markers.

    Bar plots and histograms
    ------------------------
    Bar plots and histograms are pretty similar plots. The difference lies in
    how their x axis data is structured. The bar plot has distinct labels for
    each bin, whereas each bin in a histogram lies between two points on a
    continueous line. To get data on the correct format for a histogram plot
    you can use the node :ref:`org.sysess.sympathy.dataanalysis.histogramcalc`
    as a preprocessing node.

    Use a *Bar Container* if you want to combine multiple bar plots by grouping
    or stacking them. The bar plots should all have the same *Bar Labels*.
    Please note that stacked bar plots are only situationally useful since it's
    very difficult to gauge the heights of the individual bar parts.

    Use a *Histogram Container* if you want to combine multiple histograms by
    stacking them on top of each other. Please note that stacked histograms are
    only situationally useful since it can be very difficult to read the
    distributions of the individual histograms.

    Heatmaps
    --------
    Heatmaps are two-dimensional histograms. To get data on the correct format
    for a heatmap plot you can use the node
    :ref:`org.sysess.sympathy.dataanalysis.heatmapcalc` as a preprocessing
    node.

    Box plots
    ---------
    Box plots are a good plot for comparing different distributions of data.
    The box plot is special in that it expects a *list* of arrays as data. It
    can for example be specified as ``[arg['Column A'], arg['Column B']]`` or
    with a list comprehension
    ``[arg[col_name] for col_name in arg.column_names()]``.

    Pie charts
    ----------
    Pie charts can be used to show parts of a whole, but are generally
    considered inferior to e.g. bar plots. If you use a pie chart you will also
    want to set the *Aspect ratio* of the *Axes* to 'equal'. Otherwise your pie
    chart will be very hard to ready accurately.

    Multiple axes
    =============
    There is support in the node for having more than one pair of axes. This
    can for example be useful if you want to have two different y scales for
    two line plots. To get two y axes first add an extra *Axes* item to the
    configuration tree. In the new *Axes*, you should set the *position* of the
    *YAxis* to 'right'. Lastly add one line plot to each *Axes*.

    Legends
    =======
    To get a legend you must both set labels on all plots that you want to
    include in the legend and also add a *Legend* item. Note that some plot
    types have other configuration items called things like *Bin Labels* or
    *Bar Labels*, but those are not used for the legend. Instead, look for a
    property called simply *Label* or *Labels*.

    It is possible to place the legend outside of the axes, but you might need
    to tweak the *Distance from Axes* property to get it to look just right for
    your specific plot.

    To get a single legend which summarizes all signals across multiple *Axes*
    you need to add the *Legend* to the root of the configuration tree, i.e.
    next to the *Axes* items.

    Iterators
    =========
    An *Iterator* can be used to create a dynamic number of plots in a single
    figure. The iterator can only contain a single plot, but that plot will
    then be repeated depending on the *Iterable*. For example if the data is a
    Table and the *Iterable* is ``col_name = arg.column_names()`` then ``c``
    will take on all the column_names in the Table and can be used in e.g.
    *Y Data* as such: ``arg[col_name]``.

    Python expressions as values
    ============================
    To allow the user extra flexibility, many properties can be given either as
    a normal value or as a python expression which evaluates to a value for
    that configuration item. To swith to Python mode click the grayed out
    Python icon to the right of the normal input field. Note that some fields
    can only be entered as Python expressions (notably fields like *X Data* and
    *Y Data* for line plots).

    In the python evironment the input data port is available under the name
    ``arg``. For example one can refer to data columns in a connected Table by
    writing something like ``arg['My data column']``. Have a look at the
    :ref:`datatypeapis` to see all the available methods and attributes for the
    data type that you connect to the node.

    Related nodes
    =============
    This node can not create subplots, but by creating multiple figure objects
    you can use the node :ref:`org.sysess.sympathy.visualize.figuresubplot` to
    arrange them as subplots.

    Use the node :ref:`Export figures` to write the figures you produce to
    files.

    :ref:`org.sysess.sympathy.visualize.figurecompressorgui` can be used to
    combine multiple figures into a single figure.
    """

    author = 'Benedikt Ziegler & Magnus Sandén'
    version = '0.1'
    icon = 'figure.svg'
    name = 'Figure'
    description = 'Create a Figure from some data.'
    nodeid = 'org.sysess.sympathy.visualize.figure'
    tags = Tags(Tag.Visual.Figure)

    parameters = synode.parameters()
    parameters.set_json(
        'parameters', value={},
        description='The full configuration for this figure.')

    inputs = Ports([Port.Custom('<a>', 'Input', name='input')])
    outputs = Ports([
        Port.Figure('Output figure', name='figure', preview=True)])

    def _parameter_view(self, node_context, input_data):
        figure_widget = gui.FigureFromTableWidget(
            input_data, node_context.parameters['parameters'])
        preview_widget = preview.PreviewWidget(
            self, node_context, node_context.parameters)
        widget = preview.ParameterPreviewWidget(
            figure_widget, preview_widget)
        return widget

    def exec_parameter_view(self, node_context):
        input_data = node_context.input['input']
        if not input_data.is_valid():
            input_data = api.table.File()
        return self._parameter_view(node_context, input_data)

    def execute(self, node_context):
        data_table = node_context.input['input']
        figure = node_context.output['figure']

        config_table = node_context.output.group('config')
        if len(config_table) > 0:
            config_table = config_table[0]
        else:
            config_table = None

        parameters = node_context.parameters['parameters'].value
        figure_creator = drawing.CreateFigure(data_table, figure, parameters)
        figure_creator.create_figure()


@node_helper.list_node_decorator(['input'], ['figure'])
class Figures(Figure):
    name = 'Figures'
    nodeid = 'org.sysess.sympathy.visualize.figures'

    def _parameter_view_no_preview(self, node_context, input_data):
        figure_widget = gui.FigureFromTableWidget(
            input_data, node_context.parameters['parameters'])
        preview_widget = preview.NullPreviewWidget(
            '<b>Preview requires non-empty input list</b>')
        preview_widget.setWordWrap(True)
        preview_widget.setAlignment(
            QtCore.Qt.AlignTop)
        widget = preview.ParameterPreviewWidget(
            figure_widget, preview_widget)
        return widget

    def exec_parameter_view(self, node_context):
        input_data = node_context.input['input']
        if input_data.is_valid() and len(input_data):
            return self._parameter_view(node_context, input_data[0])
        else:
            input_data = api.table.File()
            return self._parameter_view_no_preview(node_context, input_data)
