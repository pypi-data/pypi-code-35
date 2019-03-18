import os
import sys
from PyQt5 import QtWidgets

def launch_gui():

    app = QtWidgets.QApplication(sys.argv)

    from picviewer.controller.main_controller import ControlCenter

    maincontrol = ControlCenter()


    sys.exit(app.exec_())

if __name__ == '__main__':
    launch_gui()
