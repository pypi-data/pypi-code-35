import sys
from PySide2.QtCore import Qt
from PySide2.QtCore import QResource
from PySide2.QtCore import QCoreApplication
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

from gitannexgui.gitannex import GitAnnex


def main():
    
    # prepare gui
    QResource.registerResource("qml.rcc")
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine("main.qml")

    # setup gitannex handler and make available in QML
    git_annex = GitAnnex()
    engine.rootContext().setContextProperty("gitannex", git_annex)

    # start the app
    sys.exit(app.exec_())
