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
import json

from PySide2.QtWebEngineWidgets import QWebEngineView

from PySide2 import QtCore, QtWidgets, QtWebEngineWidgets, QtWebChannel


class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loadFinished.connect(self.onLoadFinished)

    @QtCore.Slot(bool)
    def onLoadFinished(self, ok):
        if ok:
            self.load_qwebchannel()
            self.run_scripts_on_load()

    def load_qwebchannel(self):
        file = QtCore.QFile(":/qtwebchannel/qwebchannel.js")
        if file.open(QtCore.QIODevice.ReadOnly):
            content = file.readAll()
            file.close()
            self.runJavaScript(content.data().decode())
        if self.webChannel() is None:
            channel = QtWebChannel.QWebChannel(self)
            self.setWebChannel(channel)

    def add_objects(self, objects, signals=''):
        if self.webChannel() is not None:
            initial_script = ""
            end_script = ""
            self.webChannel().registerObjects(objects)
            for name, obj in objects.items():
                initial_script += "var {helper};".format(helper=name)
                end_script += "{helper} = channel.objects.{helper};".format(helper=name)
            js = initial_script + \
                 "new QWebChannel(qt.webChannelTransport, function (channel) {" + \
                 end_script + \
                 signals + \
                 "} );"
            self.runJavaScript(js)

    def run_scripts_on_load(self):
        pass


class GeoJSONWebPageView(WebEnginePage):
    export = QtCore.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {}

    def run_scripts_on_load(self):
        api_key = os.environ.get('MAPBOX_API_KEY', '')
        js = f'var token = "{api_key}";'
        js += '''
            var map = L.map('mapid').setView([0, 0], 2);

            L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                maxZoom: 18,
                id: 'mapbox.streets',
                accessToken: token
            }).addTo(map);
        '''

        for d in self.data.values():
            js += '''
                  var geojsonFeature = ''' + json.dumps(d) + ''';

                  L.geoJSON(geojsonFeature).addTo(map);
                  '''
        self.runJavaScript(js)

    @QtCore.Slot(str)
    def on_clicked(self, html):
        self.export.emit(html)
        #print("clicked on startButton", html)


class GraphJSWebPageView(WebEnginePage):
    export = QtCore.Signal(str)

    def __init__(self, *args, **kwargs):
        super(GraphJSWebPageView, self).__init__(*args, **kwargs)

    def run_scripts_on_load(self):
        pass
        #self.add_objects({"jshelper": self})
        # js = '''
        #     var button = document.getElementById("startButton");
        #     button.addEventListener("click", function(){ jshelper.on_clicked(editor.getHtml()) });
        # '''
        # self.runJavaScript(js)

    @QtCore.Slot(str)
    def on_clicked(self, html):
        self.export.emit(html)
        #print("clicked on startButton", html)


class UpdatableWebPageView(WebEnginePage):
    updateHtml = QtCore.Signal(str)

    def __init__(self, *args, **kwargs):
        super(UpdatableWebPageView, self).__init__(*args, **kwargs)

    def run_scripts_on_load(self):
        signals = '''
            channel.objects.jshelper.updateHtml.connect(function(html) {
                document.getElementById("preview").innerHTML = html;
            });
        '''
        self.add_objects({"jshelper": self}, signals)
        js = '''
            var button = document.getElementById("startButton");
            button.addEventListener("click", function(){ jshelper.on_clicked(editor.getHtml()) });
        '''
        self.runJavaScript(js)

    @QtCore.Slot(str)
    def update_html(self, html):
        self.updateHtml.emit(html)
