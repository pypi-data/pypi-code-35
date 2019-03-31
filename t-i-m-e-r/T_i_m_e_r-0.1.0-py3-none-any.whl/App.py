import os
import tkinter as tk

from functools import partial
from collections import OrderedDict

from .resource import load_resource
from .TimerWidget import TimerWidget
from .TimerDialog import TimerDialog
from .AboutDialog import AboutDialog
from .lib.Settings import Settings
from .lib.misc import WindowingSystem

from . import APP


def _read_image(path, *, _li=[]):
    _ = tk.PhotoImage(data=load_resource(path), format='png')
    _li.append(_)  # keep a reference !!!
    return _


class App:
    def __init__(self):
        self._settings = Settings(os.path.expanduser(os.path.join('~', '.%s' % APP, 'Settings')))
        self._settings.load()

        root = tk.Tk(); self._root = root
        root.withdraw()
        root.title('Timer')
        root.iconphoto(True, _read_image('image/Timer.png'))

        menu = tk.Menu(root, tearoff=False); root['menu'] = menu

        menu_file = tk.Menu(menu, tearoff=False); menu.add_cascade(label='File', menu=menu_file)
        menu_file.add_command(label='New', accelerator='Ctrl+N', command=self._onnew); root.bind('<Control-KeyPress-n>', self._onnew)
        menu_file.add_separator()
        menu_file.add_command(label='Exit', command=self._onexit)

        menu_help = tk.Menu(menu, tearoff=False); menu.add_cascade(label='Help', menu=menu_help)
        menu_help.add_command(label='About', command=self._onabout)

        '''wrap a widget (like text, label, entry) to be able to specify its size in pixel
        '''

        frame_text = tk.Frame(root, borderwidth=0, highlightthickness=0)
        frame_text.grid(row=0, column=0, sticky=tk.NSEW)

        text = tk.Text(frame_text, state=tk.DISABLED, borderwidth=0, highlightthickness=0, background='#FFF', padx=0, pady=0, cursor=''); self._text = text
        text.pack(expand=True, fill=tk.BOTH)

        frame_text.pack_propagate(False)

        vs = tk.Scrollbar(root)
        vs.grid(row=0, column=1, sticky=tk.NS)

        text['yscrollcommand'] = vs.set
        vs['command'] = text.yview

        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

        TIMER_HEIGHT = 100
        TIMER_WIDTH = TimerWidget.min_width(TIMER_HEIGHT)

        text_width = self._settings.get('text/width', TIMER_WIDTH); self._settings.tosave('text/width', lambda : text_width)
        text_height = self._settings.get('text/height', TIMER_HEIGHT * 4); self._settings.tosave('text/height', lambda : text_height)

        def onresize(*_):
            nonlocal text_width, text_height

            text_width = frame_text.winfo_width()
            text_height = frame_text.winfo_height()

            _ = min(len(self._timers), text_width // TIMER_WIDTH)
            if _ == 0:
                return
            timer_width = text_width // _
            for timer in self._timers:
                timer.frame['width'] = timer_width

        frame_text.bind('<Configure>', onresize)
        frame_text['width'] = text_width
        frame_text['height'] = text_height

        root.update()

        self._timer_dialog = TimerDialog(root)
        self._about_dialog = AboutDialog(root)

        def post():
            status = active_timer.status()

            if status == TimerWidget.RUNNING:
                menu_edit.entryconfigure('Stop', state=tk.NORMAL)
                menu_edit.entryconfigure('Start', state=tk.DISABLED)
            else:
                menu_edit.entryconfigure('Stop', state=tk.DISABLED)
                menu_edit.entryconfigure('Start', state=tk.NORMAL)

            if status not in [TimerWidget.NEW, TimerWidget.EXPIRED]:
                menu_edit.entryconfigure('Restart', state=tk.NORMAL)
            else:
                menu_edit.entryconfigure('Restart', state=tk.DISABLED)

        def start():
            active_timer.start()

        def stop():
            active_timer.stop()

        def restart():
            active_timer.restart()

        def remove():
            self._remove_timer(active_timer)

        def configure():
            d = active_timer.configure()
            self._timer_dialog.configure(title='Configure')
            self._timer_dialog.set(name=d['name'], duration=d['duration'], can_edit_duration=False)
            _ = self._timer_dialog.show()
            if _ is None:
                return

            active_timer.configure(name=_[0])

        menu_edit = tk.Menu(text, tearoff=False, postcommand=post)
        menu_edit.add_command(label='Start', command=start)
        menu_edit.add_command(label='Stop', command=stop)
        menu_edit.add_command(label='Restart', command=restart)
        menu_edit.add_separator()
        menu_edit.add_command(label='Configure', command=configure)
        menu_edit.add_separator()
        menu_edit.add_command(label='Remove', command=remove)

        active_timer = None

        def onenter(_, *, timer):
            timer.configure(state=TimerWidget.ACTIVE)

        def onleave(_, *, timer):
            timer.configure(state=TimerWidget.NORMAL)

        def onrightclick(e, *, timer):
            nonlocal active_timer

            active_timer = timer
            menu_edit.tk_popup(e.x_root, e.y_root)

        self._timers = []; self._settings.tosave('timers', lambda : [_.save() for _ in self._timers])
        def add_timer(timer):
            timer.frame['width'] = 0
            timer.frame['height'] = TIMER_HEIGHT

            timer.frame.bind('<Enter>', partial(onenter, timer=timer))
            timer.frame.bind('<Leave>', partial(onleave, timer=timer))

            if WindowingSystem.windowingsystem(timer.frame) == WindowingSystem.AQUA:
                timer.bind('<ButtonRelease-2>', partial(onrightclick, timer=timer))
            else:
                timer.bind('<ButtonRelease-3>', partial(onrightclick, timer=timer))

            text['state'] = tk.NORMAL
            text.window_create('end', window=timer.frame)
            text['state'] = tk.DISABLED

            self._timers.append(timer)

            onresize()

        self._add_timer = add_timer

        for d in self._settings.get('timers', []):
            timer = TimerWidget(text)
            timer.restore(d)
            add_timer(timer)

        def remove_timer(timer):
            text['state'] = tk.NORMAL
            text.delete(timer.frame)
            text['state'] = tk.DISABLED

            self._timers.remove(timer)

            onresize()

        self._remove_timer = remove_timer

        def go():
            for _ in self._timers:
                _.tick()

            root.after(256, go)

        root.protocol('WM_DELETE_WINDOW', self._onexit)
        root.minsize(width=TIMER_WIDTH + vs.winfo_width(), height=TIMER_HEIGHT)
        root.deiconify()

        go()
        root.mainloop()

    def _onnew(self, *_):
        self._timer_dialog.configure(title='New')
        self._timer_dialog.set()
        _ = self._timer_dialog.show()
        if _ is None:
            return

        name, duration = _
        self._add_timer(TimerWidget(self._root, name=name, duration=duration))

    def _onexit(self):
        self._root.destroy()
        self._settings.save()

    def _onabout(self):
        self._about_dialog.show()


def main():
    App()
