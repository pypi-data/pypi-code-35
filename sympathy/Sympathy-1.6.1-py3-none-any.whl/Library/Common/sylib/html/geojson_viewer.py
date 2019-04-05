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

import os

from PySide2 import QtWidgets, QtCore
from PySide2.QtWebEngineWidgets import QWebEngineView

from sympathy.api.typeutil import ViewerBase
from sympathy.utils.prim import localuri

from sylib.html.webengine import GeoJSONWebPageView


class GeoJSONWidget(QtWidgets.QWidget):
    def __init__(self, json_dict, parent=None):
        super().__init__(parent)
        self.json_dict = json_dict

        self._init_gui()
        self.center_and_resize(QtWidgets.QApplication.instance())

    def center_and_resize(self, qapp):
        available_size = qapp.desktop().availableGeometry().size()
        width = available_size.width()
        height = available_size.height()
        new_size = QtCore.QSize(width*0.8, height*0.9)

        style = QtWidgets.QStyle.alignedRect(
            QtCore.Qt.LeftToRight,
            QtCore.Qt.AlignCenter,
            new_size,
            qapp.desktop().availableGeometry()
        )
        self.setGeometry(style)

    def _init_gui(self):
        self.preview = QWebEngineView()
        self.preview_page = GeoJSONWebPageView()
        self.preview_page.data = self.json_dict
        self.preview_page.profile().clearHttpCache()
        self.preview.setPage(self.preview_page)

        self.error_textedit = QtWidgets.QTextEdit()

        leaflet_html_filepath = os.path.join(
            os.path.dirname(__file__), 'leaflet', 'index.html')

        #print(leaflet_html_filepath)

        self.preview.setUrl(QtCore.QUrl(localuri(leaflet_html_filepath)))
        progressbar = QtWidgets.QProgressBar()
        self.preview_page.loadProgress.connect(progressbar.setValue)

        self.lineedit = QtWidgets.QLineEdit()

        vlayout = QtWidgets.QVBoxLayout()

        policy = QtWidgets.QSizePolicy()
        policy.setHorizontalStretch(0)
        policy.setVerticalStretch(0)
        policy.setHorizontalPolicy(QtWidgets.QSizePolicy.Expanding)
        policy.setVerticalPolicy(QtWidgets.QSizePolicy.Expanding)

        self.preview.setSizePolicy(policy)
        vlayout.addWidget(self.preview)
        vlayout.addWidget(progressbar)

        self.setLayout(vlayout)


class GeoJSONViewer(ViewerBase):
    def __init__(self, data=None, console=None, parent=None):
        super(GeoJSONViewer, self).__init__(parent)
        self._data = data

        self.view = GeoJSONWidget(self._data.get())
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)

        self.setLayout(layout)

    def data(self):
        return self._data

    def update_data(self, data):
        if data is not None:
            self.view.preview_page.data = data.get()
