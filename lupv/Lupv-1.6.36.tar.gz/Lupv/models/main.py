import git
import os
from os.path import join

from PyQt5.QtCore import QObject, pyqtSignal


class MainModel(QObject):
    record_path_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._record_path = ""
        self._students_records = None

        self.record_path_changed.connect(self.read_students_records)

    @property
    def record_path(self):
        """Return the value of record_path."""
        return self._record_path

    @record_path.setter
    def record_path(self, record_path):
        """Set the value of record_path."""
        self._record_path = record_path
        self.record_path_changed.emit(record_path)

    @property
    def students_records(self):
        """Return the value of record_path."""
        return self._students_records

    @students_records.setter
    def students_records(self, students_records):
        """Set the value of record_path."""
        self._students_records = students_records

    def get_student_dirs(self):
        "Return list of student directories"
        dirs = os.listdir(self._record_path)
        student_dirs = []
        for d in dirs:
            if d != "lupv-notes":
                if os.path.isdir(join(self._record_path, d, ".git")):
                    student_dirs.append(d)
        return student_dirs

    def get_records(self, student_path):
        """Return records from student directory."""
        student_repo = git.Repo(student_path)
        records = list(student_repo.iter_commits("master"))
        return records

    def read_students_records(self):
        """Read records from students directory."""
        student_dirs = self.get_student_dirs()
        students_records = []

        for student in student_dirs:
            student_path = join(self._record_path, student)
            records = self.get_records(student_path)

            name, student_id = [str(student).split("-")[x] for x in [0, 1]]

            student_records = StudentsRecords(name, student_id, records)
            students_records.append(student_records)

        self._students_records = students_records


class StudentsRecords(QObject):
    def __init__(self, name, student_id, records):
        super().__init__()
        self.name = name
        self.student_id = student_id
        self.records = records


class StudentRecords(QObject):
    def __init__(
        self,
        name,
        student_id,
        total_records,
        first_record_time,
        first_record_relativetime,
        last_record_time,
        last_record_relativetime,
        work_duration,
        work_relative_duration,
    ):
        super().__init__()
        self.name = name
        self.student_id = student_id
        self.total_records = total_records
        self.first_record_time = first_record_time
        self.first_record_relativetime = first_record_relativetime
        self.last_record_time = last_record_time
        self.last_record_relativetime = last_record_relativetime
        self.work_duration = work_duration
        self.work_relative_duration = work_relative_duration
