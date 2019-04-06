'''
Created on 2019年4月6日

@author: bkd
'''
import sys
import optparse
from os import walk,listdir
from os.path import expanduser,dirname,join,splitext,basename
from PyQt5.QtGui import QTextCursor, QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import  QWidget,QApplication,QFileDialog, QMessageBox
from PyQt5.uic.driver import Driver
from .fileutil import get_file_realpath
from .kdui2py_ui import Ui_Form

class kdui2py(QWidget,Ui_Form):

    def __init__ (self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(get_file_realpath("logo.jpg")))
        self.last_dir = None
    @pyqtSlot()
    def on_pb_convert_single_file_clicked(self):
        seleted_file,_ = QFileDialog.getOpenFileName(self, '转换单个文件', self.get_last_dir(), '*.ui', '')
        self.last_dir = dirname(seleted_file)
        output_file = self.convert_single_file(seleted_file)
        self.tb_result.append("转换成功，{} -> {}".format(basename(seleted_file), output_file))
        self.tb_result.moveCursor(QTextCursor.End)
        self.tb_result.append("\n")

    @pyqtSlot()
    def on_pb_single_dir_clicked(self):
        seleted_dir = QFileDialog.getExistingDirectory(self, '转换单个目录', self.get_last_dir())
        self.last_dir = seleted_dir
        
        files = listdir(seleted_dir)
        for file in files :
            if file.endswith(".ui"):
                absolute_path = join(seleted_dir,file)
                output_file = self.convert_single_file(absolute_path)
                self.tb_result.append("转换成功，{} -> {}".format(file, output_file))
                self.tb_result.moveCursor(QTextCursor.End)
        self.tb_result.append("\n")
    @pyqtSlot()
    def on_pb_dir_and_subdir_clicked(self):
        seleted_dir = QFileDialog.getExistingDirectory(self, '转换单个目录', self.get_last_dir())
        self.last_dir = seleted_dir
#         for dirpath,dirnames,filenames in walk(seleted_dir):
        for dirpath,_,filenames in walk(seleted_dir):
            for file in filenames:
                if file.endswith(".ui"):
                    absolute_path = join(dirpath,file)
                    output_file = self.convert_single_file(absolute_path)
                    self.tb_result.append("转换成功，{} -> {}".format(file, output_file))
                    self.tb_result.moveCursor(QTextCursor.End)
        self.tb_result.append("\n")
#     预览UI文件
    @pyqtSlot()
    def on_pb_preview_clicked(self):
        seleted_file,_ = QFileDialog.getOpenFileName(self, '转换单个文件', expanduser("~"), '*.ui', '')
        try:
            self.preview_widget = loadUi(seleted_file)
            self.preview_widget.show()
        except Exception as e:
            QMessageBox.warning(self, "预览文件失败", str(e), QMessageBox.Ok)

#             获取上一次打开的目录
    def get_last_dir(self):
        if self.last_dir :
            return self.last_dir
        else :
            return expanduser("~")
        
#         转换单个文件
    def convert_single_file(self,filename,preview = False):
        if filename :
            base_name = basename(filename)
            output_file = join(dirname(filename),splitext(base_name)[0]+self.le_suffix.text() +".py")
#             complete sample : opts: {'preview': False, 'output': '/tmp/r.oo', 'execute': False, 'debug': False, 'indent': 4, 'import_from': None, 'from_imports': False, 'resource_suffix': '_ui'}
            opts = optparse.Values()
            opts.ensure_value("preview", preview)
            opts.ensure_value("execute", False)
            opts.ensure_value("debug", False)
            opts.ensure_value("indent", 4)
            opts.ensure_value("from_imports", False)
            opts.ensure_value("import_from", None)
            opts.ensure_value("resource_suffix", "_rc")
            opts.ensure_value("output", output_file)
            args =filename
            driver = Driver(opts,args)
            try:
                driver.invoke()
#                 print(filename,output_file,exit_status)
#                 QMessageBox.information(self, "转换成功", str(exit_status), QMessageBox.Ok)
                return output_file
            except IOError as e:
                QMessageBox.warning(self, "转换异常", str(e), QMessageBox.Ok)
def main():
    app = QApplication(sys.argv)
    win = kdui2py()
    win.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
