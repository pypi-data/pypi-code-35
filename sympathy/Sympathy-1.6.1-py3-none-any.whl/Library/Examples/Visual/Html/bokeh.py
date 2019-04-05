# Copyright (c) 2019, System Engineering Software Society
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

from itertools import cycle

import numpy as np

from bokeh.plotting import figure
from bokeh.models import Range1d
from bokeh.embed import components

from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap
from bokeh.models.widgets import Panel, Tabs

from sympathy.api import fx_wrapper


class GeneratePlots(fx_wrapper.FxWrapper):
    arg_types = ['(json, table)']

    def execute(self):
        table = self.arg[1]

        TOOLS='pan,wheel_zoom,box_zoom,reset,save'
        scatter_colors = ('red', 'blue', 'green')
        plots = {}

        # Price/year plot
        col = table['year']
        y = table['price']
        fig = figure(tools=TOOLS, plot_width=300, plot_height=300)
        fig.scatter(col, y, size=12, color='red', alpha=0.5)
        plots['price-per-year'] = fig

        # Manufacturer count
        manufacturers, counts = np.unique(table['name'], return_counts=True)

        source = ColumnDataSource(data=dict(manufacturers=manufacturers, counts=counts))

        p = figure(x_range=manufacturers, plot_height=600, toolbar_location=None, title="Manufacturer Counts")
        p.vbar(x='manufacturers', top='counts', width=0.9, source=source, legend="manufacturers",
               line_color='white', fill_color=factor_cmap('manufacturers', palette=Spectral6, factors=manufacturers))

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.y_range.end = max(counts)
        p.legend.orientation = "horizontal"
        p.legend.location = "top_center"

        plots['p'] = p

        script, div = components(plots)

        res = {'script': script,
               'div': div,}
        self.res[0].set(res)
