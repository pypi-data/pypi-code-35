import os
import json
import time

from luigi import *
import luigi
from .formatted_target import get_formatted_class
from .config import daisy as conf

class Task(luigi.Task):
    ext = None

    def task_name(self):
        params = self.to_str_params(only_significant=True, only_public=True)
        param_str = ",".join("{}={}".format(k,v) for k, v in sorted(params.items()))

        return "{}({})".format(self.task_family, param_str.replace("/", "_"))

    def path(self):
        return os.path.join(conf().data_dir, self.get_task_family().replace('.', '/'), self.task_name())

    def output(self):
        if isinstance(self.ext, str):
            cls = get_formatted_class(self.ext)
            return cls(self.path() + "." + self.ext)

        elif isinstance(self.ext, dict):
            path = self.path()
            obj = {}
            for name, ext in self.ext.items():
               cls = get_formatted_class(ext)
               obj[name] = cls(os.path.join(path, name + "." + ext))
            return obj

        else:
            return None

    def iter_with_progress(self, iterable, length=None):
        if length is None:
            try:
                length = len(iterable)
            except AttributeError:
                length = None

        start_time = time.time()
        last_time = start_time

        def _set_status(stat, i):
            if length is not None:
                perc = i*100.0/length
                self.set_status_message("{}: {:,d} / {:,d} ({:0.1f}%)".format(stat, i, length, perc))
                self.set_progress_percentage(perc)
            else:
                self.set_status_message("{}: {:,d} / ???".format(stat, i))

        _set_status("starting", 0)
        update_span = conf().progress_update_span 

        for i, elm in enumerate(iter(iterable)):
            now = time.time()
            if now - last_time >= update_span:
                _set_status("running", i)
                last_time = now

            yield elm

        _set_status("finishing", i+1)


