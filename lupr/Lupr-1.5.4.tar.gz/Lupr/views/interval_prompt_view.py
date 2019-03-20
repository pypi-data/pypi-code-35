from PyQt5.QtWidgets import QDialog
from Lupr.views.interval_prompt_ui import Ui_Dialog


class IntervalPrompt(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.cancel_btn.clicked.connect(self.close)
        self.apply_btn.clicked.connect(self.accept)
