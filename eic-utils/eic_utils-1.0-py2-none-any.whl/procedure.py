import time, datetime
from .colorful_print import cp

class procedure(object):# {{{
    def __init__(self, msg, same_line=True):
        self.msg = msg
        self.time = time.time()
        self.finish = False
        cp.log(msg, end='\r'if same_line else '\n')

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.finish: return
        self.finish = True
        (cp.suc if traceback is None else cp.err)\
                 (self.msg, cp.done, 'time:(#b)',\
                    datetime.timedelta(seconds=time.time() - self.time))

    def __del__(self):
        if self.finish: return
        self.finish = True
        cp.suc(self.msg, cp.done, 'time:(#b)',\
                datetime.timedelta(seconds=time.time() - self.time))
# }}}
