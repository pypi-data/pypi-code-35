"""Empty docstring"""

import sys
import biseau as bs
import clyngor
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


from .imageviewer import ImageViewer
from .dotviewer import DotViewer
from .logwidget import LogWidget
from .scriptlistwidget import ScriptListWidget, ScriptRole
from .scripteditor import ScriptEditor


import time


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.tab_widget = QTabWidget()
        self.log_widget = LogWidget()
        self.script_list_widget = ScriptListWidget()

        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.tab_widget)
        self.splitter.addWidget(self.log_widget)
        self.splitter.setStretchFactor(0, 9)
        self.splitter.setStretchFactor(1, 1)
        self.setCentralWidget(self.splitter)

        self.image_viewer = ImageViewer()

        self.add_central_view(self.image_viewer)
        # TODO : add more central view

        # Build left script list view
        scripts_dock = QDockWidget()
        scripts_dock.setWindowTitle("Scripts")
        scripts_dock.setWidget(self.script_list_widget)
        scripts_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, scripts_dock)

        # setup toolbar and menubar
        self.setup_action()

        #  give focus on script editor
        self.script_list_widget.view.itemClicked.connect(
            lambda item: self.set_focus_on_editor(item.data(ScriptRole))
        )

        # (un)comment this to load working scripts
        self.add_script("scripts/raw_data.lp")
        self.add_script("scripts/compute_score.py")
        self.add_script("scripts/render_interactions.json")

    def setup_action(self):
        # Setup menu bar
        self.tool_bar = self.addToolBar("main")
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        add_action = self.tool_bar.addAction(
            QIcon.fromTheme("list-add"), "Add script", self.open_script
        )
        run_action = self.tool_bar.addAction(
            QIcon.fromTheme("media-playback-start"), "Run", self.run
        )
        stop_action = self.tool_bar.addAction(
            QIcon.fromTheme("media-playback-stop"), "stop", self.stop
        )
        clean_action = self.tool_bar.addAction(
            QIcon.fromTheme("edit-clear"), "clean cache", self.clean_cache
        )
        auto_compile_action = self.tool_bar.addAction(
            QIcon.fromTheme("view-refresh"), "auto_compile"
        )

        add_action.setShortcut(QKeySequence.Open)
        run_action.setShortcut(Qt.CTRL + Qt.Key_R)
        auto_compile_action.setCheckable(True)
        auto_compile_action.triggered.connect(self.set_auto_compile)

        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(add_action)
        file_menu.addSeparator()
        file_menu.addAction("&Quit", self.close)
        # used to store dock
        # TODO : move dock view elsewhere
        self.view_menu = self.menuBar().addMenu("&View")

        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addAction("About Qt", qApp.aboutQt)

    def add_central_view(self, widget: QWidget):

        self.tab_widget.addTab(widget, widget.windowTitle())

    def open_script(self):
        "Prompt user about a file, try to load a script from it"
        filename = QFileDialog.getOpenFileName(self, QDir.currentPath())[0]
        if not filename:  return
        assert isinstance(filename, str), filename
        relative_filename = QDir.current().relativeFilePath(filename)
        print("XOQYXL path", filename, relative_filename)
        self.add_script(filename)

    def add_script(self, filename):
        """add one script into the app. Create list item and dock"""
        # TODO: we should be able to load any script in the file, not only the first
        script = next(bs.module_loader.build_scripts_from_file(filename), None)
        if not script:  return
        self.script_list_widget.add_script(script)
        # create dock script editor
        editor = ScriptEditor(script)
        dock = QDockWidget()
        dock.setWindowTitle(script.name)
        dock.setWidget(editor)
        dock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.view_menu.addAction(dock.toggleViewAction())

    def update_scripts_from_editors(self):
        """ call ScriptEditor.update() on each editor """
        dockWidgets = self.findChildren(QDockWidget)
        for dock in dockWidgets:
            if type(dock.widget()) == ScriptEditor:
                dock.widget().update_script()

    def dock_from_script(self, script: bs.Script):
        """ TODO : dict should be better """
        dockWidgets = self.findChildren(QDockWidget)
        for dock in dockWidgets:
            if type(dock.widget()) == ScriptEditor:
                if dock.widget().script == script:
                    return dock

    def set_focus_on_editor(self, script: bs.Script):
        dock = self.dock_from_script(script)
        if dock:
            # dock.widget().edit_widget.activateWindow()
            dock.widget().edit_widget.setFocus()
            # dock.widget().edit_widget.setFocusPolicy(Qt.StrongFocus)
            # dock.widget().edit_widget.raise_()

    def run(self):
        """ Run biseau and display the dot file """

        # freeze gui
        self.script_list_widget.setDisabled(True)

        # Update script from editors
        self.update_scripts_from_editors()

        # Run main loop
        try:
            context = ""
            scripts = self.script_list_widget.get_scripts()
            for index, (context, duration) in enumerate(bs.core.yield_run(scripts)):
                self.script_list_widget.set_item_duration(index, duration)
                self.script_list_widget.set_current_script(scripts[index])
                qApp.processEvents()
            self.set_dot(bs.compile_context_to_dot(context))
        except clyngor.utils.ASPSyntaxError as e:
            self.log_widget.add_message(str(e))
        self.script_list_widget.setEnabled(True)

    def stop(self):
        print("STOP")
        # TODO: kill action_run thread

    def clean_cache(self):
        print("CLEAN_CACHE:")
        # TODO : self.scripting_widget.clear_cache()

    def set_auto_compile(self, active: bool):
        print("AUTO_COMPILE:", active)
        # TODO: toggle auto-compilation
        # TODO: change button style

    def set_dot(self, source):
        """ set dot file """
        self.image_viewer.set_dot(source)

    @staticmethod
    def start_gui():
        app = QApplication(sys.argv)
        w = MainWindow()
        w.showMaximized()
        return app.exec_()
