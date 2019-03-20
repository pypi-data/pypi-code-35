import sys

from PyQt5.QtWidgets import (
    QMenu,
    QSystemTrayIcon,
    QMainWindow,
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtGui import QIcon

from Lupr.resources import images
from Lupr.worker.record_worker import RecordWorker
from Lupr.views.interval_prompt_view import IntervalPrompt


class MainView(QMainWindow):
    def __init__(self, model, controller):
        super().__init__()

        self._model = model
        self._controller = controller

        # UI
        icon = QIcon(":img/lup.svg")
        menu = QMenu()
        self.record_action = menu.addAction("Start Recording")
        self.set_interval_action = menu.addAction("Set Interval")
        self.quit_action = menu.addAction("Stop and Quit")
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(icon)
        self.tray.setContextMenu(menu)
        self.tray.show()
        self.tray.setToolTip("Lup")
        self.tray.showMessage("Lup", "Welcome to Lup", self.tray.Information, 1500)

        self.record_action.triggered.connect(self.record)
        self.set_interval_action.triggered.connect(self.set_interval)
        self.quit_action.triggered.connect(self.quit_app)

        self.recorderThread = RecordWorker(self._model, self._controller)

        # default
        self.set_interval_action.setEnabled(False)

    def choosedir_dialog(self, caption):
        """Prompts dialog to choose record directory."""
        options = QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        return QFileDialog.getExistingDirectory(self, caption=caption, options=options)

    def record(self):
        """Start recording with worker(recorder) thread."""
        path = self.choosedir_dialog("Select Directory...")
        if not path:
            return None

        self._controller.set_record_path(path)
        self.recorderThread.start()

        self.set_interval_action.setEnabled(True)
        self.record_action.setEnabled(False)
        self.tray.showMessage("Lup", "Lup is recording", self.tray.Information, 1500)

    def set_interval(self):
        "Change record interval."
        interval_prompt = IntervalPrompt()
        accepted = interval_prompt.exec_()

        if accepted:
            interval = interval_prompt.interval_spin.value()
            if interval:
                self._controller.change_interval(interval)
                self.tray.showMessage(
                    "Lup",
                    "Interval chaned to {}".format(interval),
                    self.tray.Information,
                    1500,
                )
            else:
                title = "Interval Warning"
                msg = "Interval must higher than 0"
                QMessageBox.warning(None, title, msg)
                self.set_interval()

    def quit_app(self):
        """Quit the app."""
        self.recorderThread.terminate()
        self.tray.showMessage("Lup", "See you")
        sys.exit()
