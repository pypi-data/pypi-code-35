import tkinter as tk

from .lib.Dialog import Dialog
from .lib.MyListbox import MyListbox
from .lib.misc import lorem, duration2hms, hms2duration


def _func_1(li):
    return ['%02d' % _ for _ in li]


class TimerDialog(Dialog):
    def __init__(self, master):
        super().__init__(master)

        def new_label(text):
            return tk.Label(self.toplevel, text=text, font=('Courier', 12, 'bold'), anchor=tk.W, borderwidth=0, padx=1)

        label0 = new_label('Name')
        label0.grid(row=0, column=0, columnspan=6, sticky=tk.EW)

        v1 = tk.StringVar(); self._v1 = v1
        entry1 = tk.Entry(self.toplevel, font=('Courier', 12), borderwidth=0, insertborderwidth=0,
                          highlightthickness=1, insertwidth=1, justify=tk.CENTER, textvariable=v1); self._entry1 = entry1
        entry1.grid(row=1, column=0, columnspan=6, sticky=tk.EW)

        label20 = new_label('Hours')
        label20.grid(row=2, column=0, columnspan=2, sticky=tk.EW)

        label21 = new_label('Minutes')
        label21.grid(row=2, column=2, columnspan=2, sticky=tk.EW)

        label22 = new_label('Seconds')
        label22.grid(row=2, column=4, columnspan=2, sticky=tk.EW)

        def new_listbox(values):
            return MyListbox(self.toplevel, values=values, height=10, width=12, font=('Courier', 12),
                             borderwidth=0, highlightthickness=1, background='#FFF', foreground='#000',
                             selectbackground='#2981CC', selectforeground='#FFF')

        def new_scrollbar(listbox):
            scrollbar = tk.Scrollbar(self.toplevel, orient=tk.VERTICAL)

            listbox['yscrollcommand'] = scrollbar.set
            scrollbar['command'] = listbox.yview

            return scrollbar

        listbox30 = new_listbox(_func_1(range(100))); self._listbox30 = listbox30
        listbox30.listbox.grid(row=3, column=0)

        scrollbar31 = new_scrollbar(listbox30.listbox)
        scrollbar31.grid(row=3, column=1, sticky=tk.NS)

        listbox32 = new_listbox(_func_1(range(60))); self._listbox32 = listbox32
        listbox32.listbox.grid(row=3, column=2)

        scrollbar33 = new_scrollbar(listbox32.listbox)
        scrollbar33.grid(row=3, column=3, sticky=tk.NS)

        listbox34 = new_listbox(_func_1(range(60))); self._listbox34 = listbox34
        listbox34.listbox.grid(row=3, column=4)

        scrollbar35 = new_scrollbar(listbox34.listbox)
        scrollbar35.grid(row=3, column=5, sticky=tk.NS)

        def new_button(text):
            return tk.Button(self.toplevel, text=text, font=('Courier', 12, 'bold'), borderwidth=1)

        button_cancel = new_button('Cancel')
        button_cancel['command'] = self._oncancel
        button_cancel.grid(row=4, column=2, sticky=tk.EW)

        button_ok = new_button('Ok')
        button_ok['command'] = self._onok
        button_ok.grid(row=4, column=4, sticky=tk.EW)

        self._result = None

    def _onok(self):
        self._result = self._v1.get(), hms2duration(*[int(_.get()) for _ in [self._listbox30, self._listbox32, self._listbox34]])
        self._hide()

    def _oncancel(self):
        self._ondelete()

    def _ondelete(self):
        self._result = None
        self._hide()

    def set(self, *, name=None, duration=0, can_edit_duration=True):
        if name is None:
            name = lorem(6)
        self._v1.set(name)

        for listbox, value in zip([self._listbox30, self._listbox32, self._listbox34], _func_1(duration2hms(duration))):
            listbox.set(value, only=(not can_edit_duration))

        self._entry1.focus_set()
        self._entry1.icursor(tk.END)
        self._entry1.select_range(0, tk.END)

    def _get(self):
        return self._result
