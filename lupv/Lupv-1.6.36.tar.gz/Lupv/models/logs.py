import git
import os
from os.path import join

from PyQt5.QtCore import QObject, pyqtSignal


class LogModel(QObject):
    current_student_changed = pyqtSignal(str)
    record_path_changed = pyqtSignal(str)

    def __init__(self, main_model):
        super().__init__()
        self._record_path = ""
        self._current_student = ""
        self._student_path = ""
        self._student_repo = None
        self._student_records = None

        self._main_model = main_model
        self._record_path = self._main_model.record_path

        self.current_student_changed.connect(self.on_current_student_changed)

    @property
    def record_path(self):
        """Return the value of current student."""
        return self._record_path

    @record_path.setter
    def record_path(self, record_path):
        """Set the value of current student."""
        self._record_path = record_path
        self.record_path_changed.emit(record_path)

    @property
    def current_student(self):
        """Return the value of current student."""
        return self._current_student

    @current_student.setter
    def current_student(self, current_student):
        """Set the value of current student."""
        self._current_student = current_student
        self.current_student_changed.emit(current_student)

    @property
    def student_records(self):
        """Return the value of current student."""
        return self._student_records

    @student_records.setter
    def student_records(self, student_records):
        """Set the value of current student."""
        self._student_records = student_records

    @property
    def student_path(self):
        """Return the value of current student."""
        return self._student_path

    @student_path.setter
    def student_path(self, student_path):
        """Set the value of current student."""
        self._student_path = student_path

    @property
    def student_repo(self):
        """Return the value of current student."""
        return self._student_repo

    @student_repo.setter
    def student_repo(self, student_repo):
        """Set the value of current student."""
        self._student_repo = student_repo

    def on_current_student_changed(self):
        self.student_path = join(self._record_path, self._current_student)
        self.student_repo = git.Repo(self._student_path)
        self.student_records = self._main_model.get_records(self._student_path)

    def read_files(self):
        """Return files in student directory."""
        dirs = os.listdir(self._student_path)
        files = []
        for item in dirs:
            if os.path.isfile(join(self._student_path, item)):
                files.append(item)
        return files

    def read_focused_window(self, sha):
        """Read focused window from dotlup directory."""
        foc_win_path = join(".lup", "focused_window")
        focused_window = self._student_repo.git.show("{}:{}".format(sha, foc_win_path))
        return focused_window

    def read_auth_info(self, sha):
        """Read auth_info from dotlup directory."""
        auth_path = join(".lup", "auth_info")
        auth_file = self._student_repo.git.show("{}:{}".format(sha, auth_path))
        auth_info = auth_file.splitlines()
        return auth_info

    def read_all_windows(self, sha):
        """Read all windows from dotlup directories."""
        all_win_path = join(".lup", "all_windows")
        diff = self._student_repo.git.show("{}:{}".format(sha, all_win_path))
        windows = diff.splitlines()
        return windows

    def read_file(self, filename, sha):
        """Get content of current file state."""
        current_file = self._student_repo.git.show("{}:{}".format(sha, filename))
        return current_file

    def read_diff(self, filename, sha):
        """Get content of diff file."""
        diff = self._student_repo.git.show(sha, filename)
        return diff

    def is_exists(self, filename, sha):
        """Check if filename in current record exist."""
        files = self._student_repo.git.show("--pretty=" "", "--name-only", sha)
        if filename in files:
            return True


class Logs(QObject):
    def __init__(self, relative_datetime, datetime, sha, add_stats, del_stats):
        super().__init__()
        self.relative_datetime = relative_datetime
        self.datetime = datetime
        self.sha = sha
        self.add_stats = add_stats
        self.del_stats = del_stats
