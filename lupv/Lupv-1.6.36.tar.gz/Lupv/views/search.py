import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMessageBox,
    QTreeWidgetItem,
    QSizePolicy,
    qApp,
    QDialog,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QComboBox,
    QFileDialog,
)

from Lupv.standard.standard import MyComboBox, bold, resize_column, peek


class SearchView:
    def __init__(self, Ui, search_ctrl):
        super().__init__()
        self._ui = Ui
        self._search_ctrl = search_ctrl

        self._ui.analyze_suspects_btn.clicked.connect(self.display_suspects)

        self.suspect_filename_combo = MyComboBox()
        self.suspect_filename_combo.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.Preferred
        )
        self.suspect_filename_combo.popupAboutToBeShown.connect(
            self.display_suspect_filenames
        )
        self._ui.horizontalLayout_5.addWidget(self.suspect_filename_combo)

        self._ui.analyze_suspects_btn.setIcon(QIcon(":img/account-search.svg"))
        self._ui.analyze_suspects_btn.setIconSize(QSize(16, 16))
        self._ui.analyze_suspects_btn.setToolTip(
            "Search for Suspect.\nThis might take a while"
        )

        self._ui.windows_searchkey_widget.returnPressed.connect(
            self.display_student_windows
        )
        self._ui.windows_search_btn.clicked.connect(self.display_student_windows)
        self._ui.windows_search_btn.setIcon(QIcon(":img/account-search.svg"))
        self._ui.windows_search_btn.setIconSize(QSize(16, 16))
        self._ui.windows_search_btn.setToolTip(
            "Search window by name.\nThis might take a while"
        )

        self._ui.group_by_ip_btn.clicked.connect(self.display_student_ips)
        self._ui.group_by_ip_btn.setIcon(QIcon(":img/account-search.svg"))
        self._ui.group_by_ip_btn.setIconSize(QSize(16, 16))
        self._ui.group_by_ip_btn.setToolTip(
            "Group students by Ip Address.\nThis might take a while"
        )

        self._ui.load_editdistance_action.triggered.connect(self.load_editdistance_file)
        self._ui.export_editdistance_action.triggered.connect(
            self.show_ed_filename_dialog
        )
        self._ui.compare_editdistance_btn.clicked.connect(
            self.display_compared_editdistance
        )
        self._ui.compared_ed_savegraph_btn.clicked.connect(
            lambda: self.display_compared_editdistance(savep=True)
        )

        # editdistance page
        self.cur_student_name_combo = MyComboBox()
        self.cur_student_name_combo.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred
        )
        self.cur_filename_combo = MyComboBox()
        self.cur_filename_combo.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred
        )

        self.cur_student_name_combo.popupAboutToBeShown.connect(
            self.display_cur_students_name_ed
        )
        self.cur_filename_combo.popupAboutToBeShown.connect(
            self.display_cur_student_file_ed
        )
        self._ui.horizontalLayout_18.addWidget(self.cur_student_name_combo)
        self._ui.horizontalLayout_19.addWidget(self.cur_filename_combo)

        self.prev_student_name_combo = MyComboBox()
        self.prev_student_name_combo.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred
        )
        self.prev_filename_combo = MyComboBox()
        self.prev_filename_combo.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred
        )

        self.prev_student_name_combo.popupAboutToBeShown.connect(
            self.display_prev_students_name_ed
        )
        self.prev_filename_combo.popupAboutToBeShown.connect(
            self.display_prev_student_file_ed
        )

        self._ui.horizontalLayout_21.addWidget(self.prev_student_name_combo)
        self._ui.horizontalLayout_20.addWidget(self.prev_filename_combo)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self._ui.verticalLayout_22.addWidget(self.canvas)

    def toggle_spinner(self, toggle):
        """Show spinner icon while app working."""
        if toggle == "work":
            self._ui.spinner_stack.setCurrentIndex(1)
        else:
            self._ui.spinner_stack.setCurrentIndex(0)

    def display_suspect_filenames(self):
        "Suggest filename to display suspect fieleds."
        files = self._search_ctrl.populate_sample_filenames()
        files.insert(0, "No File Selected")
        self.suspect_filename_combo.clear()
        self.suspect_filename_combo.addItems(files)

    def display_suspects(self):
        """Display suspected students."""
        self._ui.suspects_tree.clear()
        insertions_limit = str(self._ui.insertions_limit_spin.value())
        filename = self.suspect_filename_combo.currentText()

        msg = "please set limit higer than {}\nAbove 10 is recommended"
        if int(insertions_limit) == 0:
            QMessageBox.warning(None, "", msg.format(insertions_limit))
            return None
        if filename == "No File Selected" or not filename:
            QMessageBox.warning(None, "", "please select a file")
            return None

        self.toggle_spinner("work")
        qApp.processEvents()

        suspects = self._search_ctrl.get_suspects(int(insertions_limit), str(filename))

        if len(suspects.keys()) > 0:
            for student_name_key in suspects.keys():
                parent = QTreeWidgetItem(
                    self._ui.suspects_tree,
                    [
                        "{} [{}]".format(
                            student_name_key, len(suspects[student_name_key])
                        )
                    ],
                )
                bold(parent)
                for suspect in suspects[student_name_key]:
                    QTreeWidgetItem(
                        parent,
                        [
                            suspect.name,
                            str(suspect.student_id),
                            suspect.filename,
                            str(suspect.insertions),
                            str(suspect.date),
                        ],
                    )
        else:
            for col in range(1, 5):
                self._ui.suspects_tree.hideColumn(col)
            self._ui.suspects_tree.headerItem().setText(0, "")
            msg = 'No suspect found, for "{}" insertion limit'
            QTreeWidgetItem(self._ui.suspects_tree, [msg.format(insertions_limit)])

        resize_column(self._ui.suspects_tree)
        self.toggle_spinner("ready")

    def display_student_ips(self):
        """Display grouped students ip address."""
        self.toggle_spinner("work")
        qApp.processEvents()

        self._ui.group_by_ip_tree.clear()
        ip_groups = self._search_ctrl.get_student_ip_groups()

        if len(ip_groups.keys()) > 0:
            for ip_key in ip_groups.keys():
                parent = QTreeWidgetItem(
                    self._ui.group_by_ip_tree,
                    ["{} [{}]".format(ip_key, len(ip_groups[ip_key]))],
                )
                bold(parent)
                for student_key in ip_groups[ip_key].keys():
                    child = QTreeWidgetItem(
                        parent,
                        [
                            "{} [{}]".format(
                                student_key, len(ip_groups[ip_key][student_key])
                            )
                        ],
                    )
                    for student in ip_groups[ip_key][student_key]:
                        QTreeWidgetItem(
                            child,
                            [
                                str(student.ip),
                                student.name,
                                str(student.student_id),
                                student.date,
                            ],
                        )
        else:
            for col in range(1, 4):
                self._ui.group_by_ip_tree.hideColumn(col)
            self._ui.group_by_ip_tree.headerItem().setText(0, "")
            QTreeWidgetItem(self.group_by_ip_tree, ["No IP address found"])

        resize_column(self._ui.group_by_ip_tree)
        self.toggle_spinner("ready")

    def display_student_windows(self):
        """Display student's opened windows name."""
        self._ui.windows_search_tree.clear()
        search_key = self._ui.windows_searchkey_widget.text()
        if not search_key:
            QMessageBox.warning(None, "", "please supply the window name")
            return None  # magic line `break` alias.

        self.toggle_spinner("work")
        qApp.processEvents()
        student_windows = self._search_ctrl.get_student_windows(search_key)

        if student_windows:
            for student_name_key in student_windows.keys():
                parent = QTreeWidgetItem(
                    self._ui.windows_search_tree,
                    [
                        "{} [{}]".format(
                            student_name_key, len(student_windows[student_name_key])
                        )
                    ],
                )
                bold(parent)
                for window in student_windows[student_name_key]:
                    QTreeWidgetItem(
                        parent,
                        [
                            window.window_name,
                            window.name,
                            str(window.student_id),
                            window.date,
                        ],
                    )
        else:
            for col in range(1, 5):
                self._ui.windows_search_tree.hideColumn(col)
            self._ui.windows_search_tree.headerItem().setText(0, "")
            msg = 'No windows name for "{}" found'
            QTreeWidgetItem(self._ui.windows_search_tree, [msg.format(search_key)])

        resize_column(self._ui.windows_search_tree)
        self.toggle_spinner("ready")

    #
    # Editdistance tab
    #

    def display_cur_students_name_ed(self):
        """Display current student name in editdistance page."""
        students = self._search_ctrl.populate_student_dirs()
        self.cur_student_name_combo.clear()
        students.insert(0, "No Student Selected")
        self.cur_student_name_combo.addItems(students)

    def display_cur_student_file_ed(self):
        """Display current student filename in editdistance page."""
        filenames = self._search_ctrl.populate_sample_filenames()
        self.cur_filename_combo.clear()
        filenames.insert(0, "No File Selected")
        self.cur_filename_combo.addItems(filenames)

    def choosefile_dialog(self, caption):
        """Prompts dialog to choose record directory."""
        return QFileDialog.getOpenFileName(None, caption=caption)

    def load_editdistance_file(self):
        """Load exported editdistance file."""
        filename = self.choosefile_dialog("Select File")
        if not filename[0]:
            return None
        self._search_ctrl.load_prev_editdistances(filename[0])

    def display_prev_students_name_ed(self):
        """Display previous student name in editdistance page."""
        try:
            prev_students = self._search_ctrl.get_prev_students()
        except Exception:
            msg = "Please load editdistances file first"
            QMessageBox.warning(None, "File Not Loaded", msg)
            return None
        self.prev_student_name_combo.clear()
        prev_students.insert(0, "No Student Selected")
        self.prev_student_name_combo.addItems(prev_students)

    def display_prev_student_file_ed(self):
        """Display previous student filename in editdistance page."""
        try:
            sample_filename = self._search_ctrl.get_prev_filename_sample()
        except Exception:
            msg = "Please load editdistances file first"
            QMessageBox.warning(None, "File Not Loaded", msg)
            return None
        self.prev_filename_combo.clear()
        self.prev_filename_combo.addItem(sample_filename)

    def calc_prev_editdistances(self, student_name):
        """Calculate previous editdistances values."""
        prev_editdistances = self._search_model.prev_editdistances
        prev_records_ax = prev_editdistances[student_name]["records_ax"]
        prev_editdistances_ax = prev_editdistances[student_name]["editdistances_ax"]
        return prev_records_ax, prev_editdistances_ax

    def export_editdistance(self, filename):
        """Export current editdistances value to file."""
        self.toggle_spinner("work")
        qApp.processEvents()

        self._search_ctrl.create_lupvnotes_dir()
        students_ed = self._search_ctrl.calc_all_editdistance(filename)
        ed_path = self._search_ctrl.construct_editdistance_path(filename)
        self._search_ctrl.export_editdistance(students_ed, ed_path)
        msg = "Editdistance exported to {}"
        QMessageBox.information(None, "", msg.format(ed_path))

        self.toggle_spinner("ready")

    def show_ed_filename_dialog(self):
        """Prompt dialog for suspect parameter."""
        ed_filename_dlg = EdFilenameDialog()
        files = self._search_ctrl.populate_sample_filenames()
        ed_filename_dlg.editdistance_filename_combo.clear()
        ed_filename_dlg.editdistance_filename_combo.addItems(files)

        accepted = ed_filename_dlg.exec_()
        if accepted:
            filename = ed_filename_dlg.editdistance_filename_combo.currentText()
            if filename:
                self.export_editdistance(filename)
            else:
                QMessageBox.warning(None, "", "Please Choose filename")
                self.prompt_editdistance_dialog()

    def is_pair_filled(self, field1, field2):
        """Check if both fields filled."""
        if (field1 != "" and field1 != "No Student Selected") and (
            field2 != "" and field2 != "No File Selected"
        ):
            return True

    def display_compared_editdistance(self, savep=None):
        """Display editdistance graph."""
        cur_student_name = self.cur_student_name_combo.currentText()
        cur_filename = self.cur_filename_combo.currentText()
        prev_student_name = self.prev_student_name_combo.currentText()
        prev_filename = self.prev_filename_combo.currentText()

        cur_pair = self.is_pair_filled(cur_student_name, cur_filename)
        prev_pair = self.is_pair_filled(prev_student_name, prev_filename)
        if (cur_pair is None) and (prev_pair is None):
            QMessageBox.warning(None, "", "Please fill one of the pairs")
            return None

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        cur_fmt = ""
        prev_fmt = ""
        bridge_fmt = ""

        if cur_pair is not None:
            cur_editdistances_ax, cur_records_ax = self._search_ctrl.calc_editdistances(
                cur_student_name, cur_filename
            )
            ax.plot(cur_records_ax, cur_editdistances_ax, label=cur_student_name)
            cur_fmt = "{}".format(cur_student_name)
            image_path = self._search_ctrl.construct_ed_graph_path(cur_student_name)

        if prev_pair is not None:
            prev_editdistances_ax, prev_records_ax = self._search_ctrl.calc_prev_editdistances(
                prev_student_name
            )
            ax.plot(prev_records_ax, prev_editdistances_ax, label=prev_student_name)
            prev_fmt = "{}".format(prev_student_name)
            image_path = self._search_ctrl.construct_ed_graph_path(prev_student_name)

        if (cur_pair and prev_pair) is not None:
            bridge_fmt = " .. "
            image_path = self._search_ctrl.construct_ed_graph_path(
                cur_student_name, prev_student_name
            )

        ax.legend()
        plt.title(
            "{cur}{bridge}{prev}".format(
                cur="" if cur_fmt is None else cur_fmt,
                bridge="" if bridge_fmt is None else bridge_fmt,
                prev="" if prev_fmt is None else prev_fmt,
            )
        )
        plt.xlabel("Records count")
        plt.ylabel("Editdistance from final sumbission")

        self.canvas.draw()

        if savep:
            plt.savefig(image_path)
            QMessageBox.information(None, "", "Graph saved to {}".format(image_path))


class EdFilenameDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.cancel_btn = QPushButton("Close")
        self.export_btn = QPushButton("Export")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.cancel_btn)

        self.editdistance_filename_combo = QComboBox()

        layout = QVBoxLayout()
        layout.addWidget(self.editdistance_filename_combo)
        layout.addLayout(btn_layout)
        self.resize(281, 82)

        self.cancel_btn.clicked.connect(self.close)
        self.export_btn.clicked.connect(self.accept)

        self.setLayout(layout)
