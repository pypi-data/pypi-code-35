from CalcModel import calculate
from gui import calculator
from PyQt5 import QtWidgets, QtCore
import sys


class MyWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = calculator.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Btn_Go.clicked.connect(self.btn_onclick)
        self.show()

    @QtCore.pyqtSlot()
    def btn_onclick(self):
        input_1 = self.ui.In_Num1.text()
        input_2 = self.ui.In_Num_2.text()
        input_op = self.ui.In_Select_Op.currentText()
        result = calculate.run(float(input_1), float(input_2), input_op)
        print(result)
        self.ui.Out_Result.setText(str(result))
        self.ui.Out_Result.setStyleSheet("color: rgb(28, 43, 255);")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    application = MyWindow()
    sys.exit(app.exec())

