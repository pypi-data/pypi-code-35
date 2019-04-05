# Copyright (c) 2016, System Engineering Software Society
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
from matplotlib import colors as mpl_colors

from sylib.figure import colors
from sylib.util import base_eval


REPLACE_AXIS_TYPE = {'x': 'bottom',
                     'x1': 'bottom',
                     'x2': 'top',
                     'y': 'left',
                     'y1': 'left',
                     'y2': 'right'}


def parse_value(value_text, data_table, extra_vars=None):
    """
    Evaluate expression in a limited python environment.

    Parameters
    ----------
    value_text : str
        The string that should be evaluated to produce the value.
    data_table : sympathy data type (e.g. sympathy.api.table.File)
        The input port that should be available during eval under the name arg.
    extra_vars : dict, optional
        Extra variables that will be available during eval.

    Returns
    -------
    Returns the evaluated text, or None if there was an error.
    """
    context = {'arg': data_table}
    if extra_vars:
        context.update(extra_vars)
    try:
        parsed_value = base_eval(str(value_text), context)
    except Exception:
        parsed_value = None
    return parsed_value


def verify_options(value, options):
    """Check if value is within the options."""
    if value in options:
        return value
    return None


def parse_type(value, t, options=None):
    if t == 'colortype':
        if (colors.get_color_dev(value) in ['rgb', 'rgba', 'rgbF', 'rgbaF'] or
                mpl_colors.is_color_like(value)):
            return value
        else:
            # TODO: add some validation for python expressions
            return value
    elif t == 'options':
        return verify_options(str(value), options)
    elif t == 'axesposition':
        if value in REPLACE_AXIS_TYPE.keys():
            value = REPLACE_AXIS_TYPE[value]
        return verify_options(value, options)
    elif t == bool:
        return value == 'True'
    else:
        return t(value)
