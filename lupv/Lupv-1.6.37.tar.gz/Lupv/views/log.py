from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, qApp
from PyQt5.QtGui import QBrush, QColor

from Lupv.standard.standard import resize_column


class LogView:
    def __init__(self, Ui, student_ctrl, controller):
        super().__init__()
        self._ui = Ui
        self._log_ctrl = student_ctrl
        self._main_ctrl = controller

        self._ui.log_tree.itemSelectionChanged.connect(self.log_selection_changed)

        self._ui.stats_check.setToolTip("Show/hide insertions deletions lines")
        self._ui.stats_check.clicked.connect(
            lambda: self.log_appearance_changed("stats")
        )

        self._ui.log_realdate_rbtn.setToolTip("Use Real DateTime format")
        self._ui.log_realdate_rbtn.toggled.connect(
            lambda: self.log_appearance_changed("dateformat")
        )
        self._ui.log_reldate_rbtn.setToolTip("Use Relative DateTime format")
        self._ui.log_reldate_rbtn.toggled.connect(
            lambda: self.log_appearance_changed("dateformat")
        )

        self._ui.diff_mode_rbtn.clicked.connect(self.log_selection_changed)
        self._ui.diff_mode_rbtn.setToolTip("Use diff mode for file contents")
        self._ui.show_mode_rbtn.clicked.connect(self.log_selection_changed)
        self._ui.show_mode_rbtn.setToolTip("Use show mode for file contents")
        self._ui.filename_combo.setToolTip("Filename to track")

    def toggle_spinner(self, toggle):
        """Show spinner icon while app working."""
        if toggle == "work":
            self._ui.spinner_stack.setCurrentIndex(1)
        else:
            self._ui.spinner_stack.setCurrentIndex(0)

    def clear_widgets(self):
        """Clear all widget contents."""
        self._ui.file_content_widget.clear()
        self._ui.log_tree.clear()
        self._ui.filename_combo.clear()
        self._ui.windows_tree.clear()

    def get_selected_sha(self):
        """Get SHA value from log_QTreeWidget."""
        sha = 0
        items = self._ui.log_tree.selectedItems()
        if items:
            sha = items[0].text(2)
        return sha

    def display_logs(self, complete=False):
        """Display log to log_QTreeWidget."""
        self.toggle_spinner("work")
        qApp.processEvents()

        self._ui.log_tree.clear()

        selected_file = self.get_selected_file()

        if complete:  # can't show stats without selected_file
            self._ui.log_tree.clear()
            for l in self._log_ctrl.populate_logs(selected_file):
                QTreeWidgetItem(
                    self._ui.log_tree,
                    [
                        str(l.relative_datetime),
                        str(l.datetime),
                        str(l.sha),
                        "{line}".format(
                            line="No record"
                            if l.add_stats == 0
                            else "{} Lines".format(l.add_stats)
                        ),
                        "{line}".format(
                            line="No record"
                            if l.del_stats == 0
                            else "{} Lines".format(l.del_stats)
                        ),
                    ],
                )
        else:
            for l in self._log_ctrl.populate_logs(selected_file):
                QTreeWidgetItem(
                    self._ui.log_tree,
                    [str(l.relative_datetime), str(l.datetime), str(l.sha)],
                )

        resize_column(self._ui.log_tree)
        self.toggle_spinner("ready")

    def display_file_content(self, sha):
        """Display diff to diff_QPlainTextEdit."""
        self._ui.file_content_widget.clear()

        if self._ui.diff_mode_rbtn.isChecked():
            mode = "diff"
        else:
            mode = "show"

        selected_file = self.get_selected_file()
        no_file_selected_msg = "No file selected, Please select one"
        no_file_rec_msg = 'No availibale record for "{}" in this period'.format(
            selected_file
        )
        if not selected_file:
            self._ui.file_content_widget.setPlainText(no_file_selected_msg)
        else:
            file_content = self._log_ctrl.populate_file_content(
                selected_file, sha, mode
            )
            if file_content == "" or file_content is None:
                self._ui.file_content_widget.setPlainText(no_file_rec_msg)
            else:
                if mode == "show":
                    self._ui.file_content_widget.setPlainText(file_content)
                else:
                    self._ui.file_content_widget.appendHtml(file_content)

    def display_filename(self):
        """Display file to file_QTreeWidget."""
        files = self._log_ctrl.populate_files()

        self._ui.filename_combo.clear()
        files.insert(0, "No File Selected")
        self._ui.filename_combo.addItems(files)

    def get_selected_file(self):
        """Return selected file in file_QTreeWidget."""
        filename = str(self._ui.filename_combo.currentText())
        if filename != "No File Selected":
            return filename

    def display_windows(self, sha):
        """Display all windows and focused window from self._ui.records."""
        self._ui.windows_tree.clear()

        focused_window = self._log_ctrl.populate_focused_window(sha)
        focused_row = QTreeWidgetItem(self._ui.windows_tree, [focused_window])

        focused_row.setForeground(0, QBrush(QColor("#41CD52")))
        windows = self._log_ctrl.populate_all_windows(sha)
        for window in windows:
            if window != focused_window:
                QTreeWidgetItem(self._ui.windows_tree, [window])

    def display_auth_info(self, sha):
        """Display auth information from self._ui.records."""
        auth_info = self._log_ctrl.populate_auth_info(sha)
        if auth_info:
            self._ui.name_lbl.setText(auth_info[0])
            self._ui.machine_lbl.setText(auth_info[1])
            self._ui.ip_lbl.setText(auth_info[2])

    def log_selection_changed(self):
        """Actions invoked when selection in log_QTreeWidget changed."""
        sha = self.get_selected_sha()
        if sha:
            self.display_file_content(sha)
            self.display_windows(sha)
            self.display_auth_info(sha)

    def log_appearance_changed(self, btn_name):
        """Actions when appearance setting changed."""
        if btn_name == "stats":
            self.toggle_stats()
        else:
            self.toggle_dateformat()
        resize_column(self._ui.log_tree)

    def toggle_stats(self):
        """Togggle insertions deletions columns visibility."""
        if self._ui.stats_check.isChecked():
            selected_file = self.get_selected_file()
            if not selected_file:
                QMessageBox.warning(None, "", "please choose a file")
                self._ui.stats_check.setChecked(False)
                return None

            self.display_logs(complete=True)
            for col_num in [3, 4]:
                self._ui.log_tree.showColumn(col_num)
        else:
            for col_num in [3, 4]:
                self._ui.log_tree.hideColumn(col_num)

    def toggle_dateformat(self):
        """Togggle dateformat columns visibility."""
        if self._ui.log_realdate_rbtn.isChecked():
            self._ui.log_tree.showColumn(1)
            self._ui.log_tree.hideColumn(0)
        else:
            self._ui.log_tree.showColumn(0)
            self._ui.log_tree.hideColumn(1)
