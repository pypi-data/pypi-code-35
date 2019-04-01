from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSvg import *

from graphviz import Source


class ImageView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene())

        self.setBackgroundBrush(QBrush(Qt.white))
        # It appears that Qt can handle gif:
        #  https://stackoverflow.com/questions/41709464/python-pyqt-add-background-gif
        # so is biseau.gif_from_filenames and derivatives

    def wheelEvent(self, event):
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Zoom
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.scale(zoomFactor, zoomFactor)

        # Get the new position
        newPos = self.mapToScene(event.pos())

        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())

    def set_dot(self, source):
        s = Source(source, format="svg")
        s.render("tmp")
        self.dot_item = QGraphicsSvgItem("tmp.svg")
        self.scene().clear()
        self.scene().addItem(self.dot_item)


class ImageViewer(QWidget):

    #  exemple signals
    dotReceived = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image viewer")
        self.tool_bar = QToolBar()
        self.view = ImageView()

        _layout = QVBoxLayout()
        _layout.addWidget(self.tool_bar)
        _layout.addWidget(self.view)
        _layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(_layout)

        #  example connection simple
        self.tool_bar.addAction("act_1", lambda: print("act_1"))
        self.tool_bar.addAction("act_2", self.act_2)

        #  example connection avec arguments
        self.combo = QComboBox()
        self.combo.addItems(["test1", "test2", "test3"])
        self.tool_bar.addWidget(self.combo)
        self.combo.currentTextChanged.connect(self.act_3)

        #  example de connection
        self.dotReceived.connect(self.act_4)

    def set_dot(self, source: str):
        self.view.set_dot(source)
        #  example envoie signals
        self.dotReceived.emit(True)

    def act_2(self):
        # example avec sender qui est l'envoyeur du signals
        print("act2", self.sender().text())
        print("act2 property", self.sender().property("text"))  # Property

    def act_3(self, value):
        print("act3", value)

    def act_4(self, status: bool):
        print("act_4", status)
