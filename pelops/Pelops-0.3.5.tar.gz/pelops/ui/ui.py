from cmd import Cmd
import threading


class UI(Cmd):
    intro = None
    prompt = None
    _stop_service_cmd = None
    _service_is_stopping = None
    _stopping = None

    def __init__(self, intro, prompt, stop_service_cmd, service_is_stopping):
        self.intro = intro
        self.prompt = prompt
        self._stopping = False

        Cmd.__init__(self)

        self._stop_service_cmd = stop_service_cmd
        self._service_is_stopping = service_is_stopping
        self._main_thread = threading.Thread(target=self._wrapper, name=__class__.__name__+".wrapper")

    def start(self):
        self._main_thread.start()

    def stop(self):
        if not self._stopping:
            self.onecmd("exit")
        self._main_thread.join()

    def _wrapper(self):
        self._stopping = False
        self.cmdloop()
        self._stopping = True
        if not self._service_is_stopping.is_set():
            stop_daemon = threading.Thread(target=self._stop_service_cmd, name=__class__.__name__+" stop command")
            stop_daemon.daemon = True
            stop_daemon.start()

    def do_exit(self, arg):
        """exit - stops the monitoring service: EXIT"""
        return True

    def do_e(self, arg):
        # """shortcut for 'exit'"""
        return True

    def do_q(self, arg):
        # """shortcut for 'exit'"""
        return True

    @classmethod
    def add_command(cls, name, function):
        cmd_name = "do_"+name

        try:
            getattr(cls, cmd_name)
            raise ValueError("command '{}' already defined".format(name))
        except AttributeError:
            pass  # expected behavior

        if not callable(function):
            raise AttributeError("parameter function must be callable")

        setattr(cls, cmd_name, function)
