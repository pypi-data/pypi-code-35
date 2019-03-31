import tkinter as tk

from .ConfMixin import ConfMixin
from .misc import center_window, WindowingSystem


class Dialog(ConfMixin):
    def __init__(self, master):
        ConfMixin.__init__(self)

        self.toplevel = tk.Toplevel(master)
        self.toplevel.withdraw()

        self._register_conf(name='title', func_set=lambda _: self.toplevel.title(_))
        self._register_conf(name='iconphoto', func_set=lambda _: self.toplevel.iconphoto(_))

        self.toplevel.resizable(False, False)
        self.toplevel.protocol("WM_DELETE_WINDOW", self._ondelete)

        self._shown = False

    def show(self):
        if WindowingSystem.windowingsystem(self.toplevel) == WindowingSystem.X11:
            self.toplevel.transient(self.toplevel.master)
            self.toplevel.deiconify()

            if not self._shown:
                self.toplevel.update()
                center_window(self.toplevel)
                self._shown = True
        else:
            if not self._shown:
                center_window(self.toplevel)
                self._shown = True

            self.toplevel.transient(self.toplevel.master)
            self.toplevel.deiconify()

        self.toplevel.grab_set()

        self.toplevel.master.mainloop()

        return self._get()

    def _hide(self):
        self.toplevel.master.quit()
        self.toplevel.transient()
        self.toplevel.grab_release()
        self.toplevel.withdraw()
        self.toplevel.master.focus_set()

    def _get(self):
        pass

    def set(self, *args, **kwargs):
        pass

    def destroy(self):
        self.toplevel.destroy()

    def _ondelete(self):
        self._hide()
