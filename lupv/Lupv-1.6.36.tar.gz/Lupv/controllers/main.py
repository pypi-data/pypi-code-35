import os
import pendulum
from os.path import join

from PyQt5.QtCore import QObject, pyqtSlot

from Lupv.models.main import StudentRecords


class MainController(QObject):
    def __init__(self, main_model):
        super().__init__()
        self._record_path = ""
        self._main_model = main_model

        self._main_model.record_path_changed.connect(self.on_record_path_changed)

    def change_record_path(self, record_path):
        self._main_model.record_path = record_path

    @pyqtSlot(str)
    def on_record_path_changed(self, record_path):
        self._record_path = record_path

    def validate(self, path):
        """Check if path contain valid student directory.

        This is necessary because invalid directory will break `read_records` and
        make application crash.
        """
        dirs = os.listdir(path)
        invalid_student_dirs = []
        for d in dirs:
            if d != "lupv-notes":
                if not os.path.isdir(join(path, d, ".git")):
                    invalid_student_dirs.append(d)

        return invalid_student_dirs

    def relativize_datetime(self, datetime):
        """Convert datetime into its relative version."""
        dt = pendulum.instance(datetime)
        relative_time = dt.diff_for_humans()
        return relative_time

    def get_first_record_time(self, first_record_dt):
        """Take the first record time."""
        first_record_time = "{:%a, %d %b %Y, %H:%M:%S}".format(first_record_dt)
        first_record_relativetime = self.relativize_datetime(first_record_dt)
        return first_record_time, first_record_relativetime

    def get_last_record_time(self, last_record_dt):
        """Take the last record time."""
        last_record_time = "{:%a, %d %b %Y, %H:%M:%S}".format(last_record_dt)
        last_record_relativetime = self.relativize_datetime(last_record_dt)
        return last_record_time, last_record_relativetime

    def calc_work_duration(self, first_record_dt, last_record_dt):
        """Calculate duration between last and first record time."""
        work_duration = str(last_record_dt - first_record_dt)
        last_dt, first_dt = [
            pendulum.instance(x) for x in [last_record_dt, first_record_dt]
        ]
        work_relative_duration = (last_dt - first_dt).in_words(locale="en")
        return work_duration, work_relative_duration

    def populate_students_records(self):
        """Return list of student records."""
        students_records = self._main_model.students_records

        for student in students_records:
            name = student.name
            student_id = student.student_id
            total_records = len(student.records)

            first_record_dt, last_record_dt = [
                student.records[x].committed_datetime for x in [-1, 0]
            ]
            first_record_time, first_record_relativetime = self.get_first_record_time(
                first_record_dt
            )
            last_record_time, last_record_relativetime = self.get_last_record_time(
                last_record_dt
            )
            work_duration, work_relative_duration = self.calc_work_duration(
                first_record_dt, last_record_dt
            )

            student_records = StudentRecords(
                name,
                student_id,
                total_records,
                first_record_time,
                first_record_relativetime,
                last_record_time,
                last_record_relativetime,
                work_duration,
                work_relative_duration,
            )
            yield student_records
