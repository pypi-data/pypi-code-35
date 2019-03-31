import queue


class InvokeMixin:
    def _init(self):
        self._q = queue.Queue()

        def f():
            funcs = []
            while True:
                try:
                    funcs.append(self._q.get_nowait())
                except queue.Empty:
                    break

            for _ in funcs:
                _()

            self.tk.after(100, f)

        f()

    def invoke(self, func):
        if getattr(self, '_q', None) is None:
            self._init()

        self._q.put(func)
