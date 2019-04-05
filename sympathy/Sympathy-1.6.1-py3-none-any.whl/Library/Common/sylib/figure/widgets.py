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
from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import numpy as np
import six
from matplotlib import colors as mpl_colors

from sylib.figure import colors
from sylib.icons import utils as icon_utils
from sylib.tree_model import widgets as tree_widgets
from sympathy.api import qt2 as qt
from sympathy.platform import widget_library as sywidgets

QtCore = qt.QtCore
QtGui = qt.QtGui
QtWidgets = qt.QtWidgets


class SyColorEdit(tree_widgets.SyBaseTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        icon = icon_utils.create_icon(icon_utils.SvgIcon.color)
        self.toolbutton = sywidgets.LineEditDropDownMenuButton(
            icon, parent=self)
        self.toolbutton.setToolTip('Click to select a color.')
        self.add_widget(self.toolbutton)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.toolbutton.clicked.connect(self._on_color_pick)
        self.textChanged.connect(self._eval_color)

        self._keep_focus = False

    def allow_focus_out(self, reason):
        # Workaround to prevent the widget from losing focus if the color pick
        # dialog or drop down menu is used
        if reason == QtCore.Qt.ActiveWindowFocusReason and self._keep_focus:
            # Opening the color picker dialog will trigger one FocusOutEvent
            # with ActiveWindowFocusReason, but it will only reach the event
            # filter in SyStackedPythonEdit after _on_color_pick has returned
            # control to the event loop. Therefore we ignore the first such
            # event after each call to _on_color_pick until the timeout event
            # has triggered and reset self._keep_focus to False.
            return False
        return True

    def _eval_color(self):
        text = self.toPlainText()
        color = colors.parse_to_mpl_color(text)
        self._update_button_color(color)

    def _on_color_pick(self):
        # Don't open a new color picker if one has already been opened:
        if self._keep_focus:
            return

        self._keep_focus = True
        # store old value and type
        try:
            old_value = self.get_value()
            color = colors.get_color_as_rgba_f(old_value)
        except ValueError:
            color = [0, 0, 0]
        if color is None:
            color = [0, 0, 0]
        color = np.array(color) * 255
        qcolor = QtGui.QColor(*color.astype(int))
        # create dialog
        dialog = QtWidgets.QColorDialog(qcolor, parent=self)
        dialog.setOptions(QtWidgets.QColorDialog.ShowAlphaChannel)
        color = dialog.getColor()

        # Queue an event which will be handled after possible FocusOutEvents
        QtCore.QTimer.singleShot(0, self._end_color_pick)

        if not color.isValid():
            return
        new_value = mpl_colors.rgb2hex(color.getRgbF())
        self.set_value(new_value)

    def _end_color_pick(self):
        self._keep_focus = False

    def _update_button_color(self, value):
        if value is not None:
            icon = icon_utils.color_icon(six.text_type(value))
        else:
            icon = icon_utils.create_icon(icon_utils.SvgIcon.color)
        self.toolbutton.setIcon(icon)
