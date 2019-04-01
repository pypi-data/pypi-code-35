from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import biseau as bs

from .optionswidget import OptionsWidget


class ScriptEditor(QWidget):
    def __init__(self, script, parent=None):
        super().__init__(parent)

        v_layout = QVBoxLayout()

        self.tab_widget = QTabWidget()

        # First tab = editor
        self.edit_widget = QPlainTextEdit()
        self.tab_widget.addTab(self.edit_widget, "editor")

        # Second Tab = options
        self.option_widget = OptionsWidget()
        self.tab_widget.addTab(self.option_widget, "options")

        v_layout.addWidget(self.tab_widget)
        v_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(v_layout)

        self.set_script(script)

        self.setStyleSheet("QFrame:focus {  border: 2px solid red; }")

    def __del__(self):
        print("destructor")

    def set_script(self, script: bs.Script):
        """ set script reference for this editor """
        self.script = script
        self.edit_widget.setPlainText(self.script.source_code)
        self.option_widget.set_script(script)

    def update_script(self):
        self.script.source_code = self.edit_widget.toPlainText()
        print("options", self.option_widget.model.get_option_values())
        self.script.options_values.update(self.option_widget.model.get_option_values())
