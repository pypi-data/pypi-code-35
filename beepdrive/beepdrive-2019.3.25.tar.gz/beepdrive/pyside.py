import os
import sys
import time
import platform
import threading
from queue import Queue

import qdarkstyle
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import beepdrive.snake as snake
from beepdrive.utils import is_frozen, frozen_temp_path

windowWidth = 450
windowHeight = 525

if is_frozen:
    base_dir = frozen_temp_path
elif platform.system() == "Linux":
    base_dir = os.path.join(os.path.expanduser("~"), ".local")
else:
    base_dir = sys.prefix

class Error:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.error_dialog = QErrorMessage()
        self.error_dialog.showMessage("Dependencies not satisfied. Please see https://github.com/amecava/beepdrive/blob/master/README.md for details.")
        self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        self.app.exec_()

class GUI():
    th = None
    th2 = None

    def __init__(self, beepdrive):
        self.beepdrive = beepdrive
        self.app = QApplication(sys.argv)
        self.app.setWindowIcon(QIcon(os.path.join(base_dir, "lib/Bd.png")))
        self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.app.aboutToQuit.connect(self.quit)
        self.login_window = None
        self.selection_window = None
        self.folder_window = None
        self.download_window = None
        self.main_window = None

    def run(self):
        GUI.main_window = GUI.MainWindow()
        GUI.login_window = GUI.LoginWindow(self.beepdrive)
        GUI.folder_window = GUI.FolderWindow(self.beepdrive)
        GUI.selection_window = GUI.SelectionWindow(self.beepdrive, '')
        GUI.download_window = GUI.DownloadWindow(self.beepdrive, '', None)
        GUI.main_window.setCentralWidget(GUI.login_window)
        GUI.main_window.show()
        GUI.th = threading.Thread(name="createDriver", target=self.beepdrive.create_driver)
        GUI.th.setDaemon(True)
        GUI.th.start()

        self.app.exec_()

        self.beepdrive.quit()
        sys.exit(0)

    def quit(self):
        self.beepdrive.quit()

        sys.exit(0)
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setFixedSize(windowWidth, windowHeight)

    class LoginWindow(QWidget):
        def __init__(self, beepdrive):
            super().__init__()
            self.beepdrive = beepdrive
            self.setFixedSize(windowWidth, windowHeight)
            self.setWindowTitle("BeepDrive")
            self.image = QLabel(self)
            self.logo = QPixmap(os.path.join(base_dir, "lib/Bd.png"))
            self.image.setPixmap(self.logo.scaled(100, 100))
            self.image.move((windowWidth - 100) / 2, 100)
            self.cod_text = QLineEdit(self)
            self.cod_text.setPlaceholderText("Person code")
            self.cod_text.setFixedWidth(200)
            self.cod_text.move((windowWidth - 200) / 2, 300)
            self.pw_text = QLineEdit(self)
            self.pw_text.setPlaceholderText("Password")
            self.pw_text.setEchoMode(QLineEdit.Password)
            self.pw_text.setFixedWidth(200)
            self.pw_text.move((windowWidth - 200) / 2, 350)
            self.enterbutton = QPushButton("Login", self)
            self.enterbutton.clicked.connect(self.log_in)
            self.enterbutton.setFixedWidth(200)
            self.enterbutton.move((windowWidth - 200) / 2, 400)
            self.cod_text.returnPressed.connect(self.enterbutton.click)
            self.pw_text.returnPressed.connect(self.enterbutton.click)
            self.auth_text = QLabel('', self)
            self.auth_text.hide()
            self.auth_text.setFixedWidth(windowWidth)
            self.auth_text.move(0, 450)
            self.auth_text.setAlignment(Qt.AlignCenter)
            self.enterbutton.setEnabled(True)

        def log_in(self):
            GUI.th.join()
            self.log_th = threading.Thread(target=self.logging)
            self.log_th.setDaemon(True)
            self.log_th.start()

        def logging(self):
            auth_errors = {
                1: "person code not valid.",
                7: "wrong password.",
                14: "person code not valid.",
                24: "empty password.",
                129: "person code not valid."
            }
            self.auth_text.setText("Logging in...")
            self.auth_text.setStyleSheet("color: white")
            self.auth_text.setAlignment(Qt.AlignCenter)
            self.auth_text.show()
            self.enterbutton.setEnabled(False)

            if self.cod_text.text() == '':
                self.auth_result = 14
            elif self.pw_text.text() == '':
                self.auth_result = 24
            else:
                self.queue = Queue()
                self.th = threading.Thread(name="login_thread", target=self.beepdrive.aunica_login, args=(self.queue, self.cod_text.text(), self.pw_text.text(),))
                self.th.setDaemon(True)
                self.th.start()
                self.th.join()
                self.auth_result = self.queue.get()

            if self.auth_result == 0:
                GUI.th = threading.Thread(name="getCoursesThread", target=self.beepdrive.get_courses)
                GUI.th.setDaemon(True)
                GUI.th.start()
                GUI.main_window.setCentralWidget(GUI.folder_window)
            else:
                self.auth_text.setText("Authentication failed: " + auth_errors[self.auth_result])
                self.auth_text.setStyleSheet("color: red")
                self.auth_text.setAlignment(Qt.AlignCenter)
                self.auth_text.show()
                self.enterbutton.setEnabled(True)

    class FolderWindow(QWidget):
        def __init__(self, beepdrive):
            super().__init__()
            self.beepdrive = beepdrive
            self.setFixedSize(windowWidth, windowHeight)
            self.setWindowTitle("BeepDrive")
            self.image = QLabel(self)
            self.logo = QPixmap(os.path.join(base_dir, "lib/Bd.png"))
            self.image.setPixmap(self.logo.scaled(100, 100))
            self.image.move((windowWidth - 100) / 2, 100)
            self.lbBroswer = QLabel("Choose a directory:", self)
            self.lbBroswer.setFixedWidth(200)
            self.lbBroswer.move((windowWidth - 200) / 2, 300)
            self.etBrowser = QLineEdit('', self)
            self.etBrowser.setFixedWidth(165)
            self.etBrowser.move((windowWidth - 200) / 2, 350)
            self.btnBrowse = QPushButton("...", self)
            self.btnBrowse.setToolTip("Select directory...")
            self.btnBrowse.resize(30, 24)
            self.btnBrowse.move((windowWidth - 200) / 2 + 170, 350)
            self.btnBrowse.clicked.connect(self.selectDirectory)
            self.button = QPushButton("Select", self)
            self.button.setFixedWidth(200)
            self.button.move((windowWidth - 200) / 2, 400)
            self.button.clicked.connect(self.choose_path)
            self.folder_error = QLabel("The selected folder is invalid.", self)
            self.folder_error.setStyleSheet("color: red")
            self.folder_error.hide()
            self.folder_error.setFixedHeight(20)
            self.folder_error.setFixedWidth(200)
            self.folder_error.move((windowWidth - 200) / 2, 450)
            self.etBrowser.returnPressed.connect(self.button.click)

        def selectDirectory(self):
            self.etBrowser.setText(QFileDialog.getExistingDirectory())

        def choose_path(self, courses_dict):
            self.folder_error.hide()
            self.folder = self.etBrowser.text()
            if self.folder == "":
                self.folder_error.show()
            else:
                if self.folder[-1] != '/':
                    self.folder = self.folder + "/"
                GUI.th.join()
                GUI.selection_window = GUI.SelectionWindow(self.beepdrive, self.folder)
                GUI.main_window.setCentralWidget(GUI.selection_window)

    class SelectionWindow(QWidget):
        def __init__(self, beepdrive, folder):
            super().__init__()
            self.beepdrive = beepdrive
            self.folder = folder
            self.setFixedSize(windowWidth, windowHeight)
            self.setWindowTitle("BeepDrive")
            self.image = QLabel(self)
            self.logo = QPixmap(os.path.join(base_dir, "lib/Bd.png"))
            self.image.setPixmap(self.logo.scaled(100, 100))
            self.image.move((windowWidth - 100) / 2, 100)
            self.courses = self.beepdrive.courses.copy()
            self.checkboxes = []
            self.position = 300
            self.select_button = QPushButton("Confirm", self)
            self.select_button.setFixedWidth(100)
            self.select_button.clicked.connect(self.get_courses_to_download)
            self.select_button.move((windowWidth - 100) / 2, windowHeight - 50)
            self.select_all = QCheckBox("Deselect all", self)
            self.select_all.setTristate(True)
            self.select_all.setCheckState(Qt.Checked)
            self.select_all.clicked.connect(self.tristate)
            self.select_all.move(30, windowHeight - 50)
            self.select_all.setChecked(True)
            self.scroll_area = QScrollArea(self)
            self.scroll_area.setFixedSize(400, 150)
            self.scroll_area.move((windowWidth - 400) / 2, 300)
            self.scroll_area.setWidgetResizable(True)
            self.widget = QWidget()
            self.widget.setFixedWidth(350)
            self.layout = QVBoxLayout(self.widget)
            self.layout.setSpacing(3)
            self.scroll_area.setWidget(self.widget)
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.layout.setAlignment(Qt.AlignTop)
            self.layout.setAlignment(Qt.AlignCenter)
            for course in self.courses.keys():
                self.checkboxes.append(QCheckBox(course, self))
                self.checkboxes[-1].setChecked(True)
                self.checkboxes[-1].setStyleSheet("font: 10pt")
                self.checkboxes[-1].stateChanged.connect(self.change_tristate)
                self.layout.addWidget(self.checkboxes[-1])
            self.layout.addStretch(1)

        def get_courses_to_download(self):
            for check in self.checkboxes:
                self.courses[check.text()] = check.isChecked()
            GUI.download_window = GUI.DownloadWindow(self.beepdrive, self.folder, self.courses)
            GUI.main_window.setCentralWidget(GUI.download_window)
            GUI.download_window.download()

        def tristate(self):
            if self.select_all.checkState() == Qt.Unchecked:
                self.uncheck_all()
                self.select_all.setText("Select all")
            elif self.select_all.checkState() == Qt.Checked:
                self.check_all()
                self.select_all.setText("Deselect all")
            else:
                self.select_all.setCheckState(Qt.Checked)
                self.check_all()
                self.select_all.setText("Deselect all")

        def change_tristate(self):
            self.true = 0
            self.false = 0
            for check in self.checkboxes:
                if check.isChecked():
                    self.true += 1
                else:
                    self.false += 1
            if self.true == 0:
                self.select_all.setCheckState(Qt.Unchecked)
                self.select_all.setText("Select all")
            elif self.false == 0:
                self.select_all.setCheckState(Qt.Checked)
                self.select_all.setText("Deselect all")
            else:
                self.select_all.setCheckState(Qt.PartiallyChecked)
                self.select_all.setText("Select all")

        def check_all(self):
            for check in self.checkboxes:
                check.setChecked(True)

        def uncheck_all(self):
            for check in self.checkboxes:
                check.setChecked(False)

    class DownloadWindow(QWidget):
        def __init__(self, beepdrive, folder, courses_dict):
            super().__init__()
            self.beepdrive = beepdrive
            self.folder = folder
            self.courses = courses_dict
            self.setFixedSize(windowWidth, windowHeight)
            self.setWindowTitle("BeepDrive")
            self.image = QLabel('', self)
            self.logo = QPixmap(os.path.join(base_dir, "lib/Bd.png"))
            self.image.setPixmap(self.logo.scaled(100, 100))
            self.image.move((windowWidth - 100) / 2, 100)
            self.progress = QProgressBar(self)
            self.progress.setFixedWidth(300)
            self.progress.setFixedHeight(20)
            self.progress.move((windowWidth - 300) / 2, 300)
            self.progress.setValue(0)
            self.label = QLabel("Waiting for download to start...", self)
            self.label.setFixedWidth(300)
            self.label.setFixedHeight(100)
            self.label.setAlignment(Qt.AlignTop)
            self.label.move((windowWidth - 300) / 2, 325)
            self.label.hide()
            self.finish_button = QPushButton("Close", self)
            self.finish_button.hide()
            self.finish_button.setFixedWidth(200)
            self.finish_button.move((windowWidth - 200) / 2, 300)
            self.finish_button.clicked.connect(self.close_app)
            self.sboard = snake.Board(self, windowWidth - 20, windowHeight - 340)
            self.sboard.resize(windowWidth - 20, windowHeight - 340)
            self.sboard.move(10, 330)
            self.sboard.start()
            self.n_courses = 0

        def download(self):
            for check in self.courses.values():
                if check:
                    self.n_courses += 1
            self.th = threading.Thread(name="beepDriveThread", target=self.beepdrive.start_download, args=(self.folder, self.courses,))
            self.th.setDaemon(True)
            self.th.start()
            self.main_th = threading.Thread(name="goThread", target=self.go)
            self.main_th.setDaemon(True)
            self.main_th.start()

        def go(self):
            self.stop = False
            while not self.stop:
                self.th2 = threading.Thread(name="changeLabelThread", target=self.change_label, args=(self.beepdrive.downloaded, self.n_courses,))
                self.th2.setDaemon(True)
                self.th2.start()
                self.th2.join()
            self.finish_button.show()
            self.progress.hide()

        def change_label(self, downloading, courses):
            if courses == 0:
                self.stop = True
            elif not self.th.isAlive():
                self.progress.setValue(100)
                self.progress.setFormat("Download complete - 100%")
                time.sleep(3)
                self.stop = True
            else:
                self.status = downloading * 100 / courses
                self.progress.setValue(self.status)
                self.progress.setFormat(("%.2f" % self.status) + " %")
            return

        def close_app(self):
            self.beepdrive.quit()

            sys.exit(0)
