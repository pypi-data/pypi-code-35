import pathlib
import git
import os
from os.path import join
from datetime import datetime

from PyQt5.QtCore import QObject


class Model(QObject):
    def __init__(self):
        super().__init__()
        self._record_path = ""
        self._record_interval = 3

    @property
    def record_path(self):
        """Return the value of record_path."""
        return self._record_path

    @record_path.setter
    def record_path(self, record_path):
        """Set the value of record_path."""
        self._record_path = record_path

    @property
    def record_interval(self):
        return self._record_interval

    @record_interval.setter
    def record_interval(self, interval):
        self._record_interval = interval

    def get_dotlup_path(self):
        """Return the value of watchers."""
        return join(self._record_path, ".lup")

    def create_dotlup_dir(self):
        """Create watchers directory."""
        pathlib.Path(join(self._record_path, ".lup")).mkdir(parents=True, exist_ok=True)

    def write_auth_info(self, auth_info):
        """Write auth information to file."""
        auth_file_path = join(self.get_dotlup_path(), "auth_info")
        auth_file = open(auth_file_path, "w+")
        auth_file.write(auth_info)
        auth_file.close()

    def write_all_windows(self, all_windows):
        """Write all windows title to file."""
        all_windows_path = join(self.get_dotlup_path(), "all_windows")
        all_windows_file = open(all_windows_path, "w+")
        all_windows_file.write(all_windows)
        all_windows_file.close()

    def write_focused_window(self, active_window):
        """Write focused window title to file."""
        focused_window_path = join(self.get_dotlup_path(), "focused_window")
        focused_window_file = open(focused_window_path, "w+")
        focused_window_file.write(active_window)
        focused_window_file.close()

    def is_repo(self):
        if os.path.isdir(join(self._record_path, ".git")):
            return True

    def initialize_student_repo(self):
        student_repo = git.Repo.init(self._record_path)
        # real name and email useless cause lup already record login
        # and machine name
        student_repo.config_writer().set_value("user", "name", "student").release()
        student_repo.config_writer().set_value("user", "email", "s@student").release()
        return student_repo

    def get_student_repo(self):
        if self.is_repo():
            student_repo = git.Repo(self._record_path)
        else:
            student_repo = self.initialize_student_repo()
        return student_repo

    def create_record(self):
        student_repo = self.get_student_repo()
        # commit only when changed file present
        if "nothing to commit" not in str(student_repo.git.status()):
            student_repo.git.add(".")
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            student_repo.git.commit(m=now)
