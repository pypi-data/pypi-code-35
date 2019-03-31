import tkinter as tk


class MyListbox:
    def __init__(self, master, *, values, background, foreground, selectbackground, selectforeground, **kwargs):
        assert len(values) > 0

        self._background = background
        self._foreground = foreground
        self._selectbackground = selectbackground
        self._selectforeground = selectforeground

        self.listbox = tk.Listbox(master, selectmode=tk.BROWSE, activestyle=tk.NONE,
                                  background=background, foreground=foreground,
                                  selectbackground=background, selectforeground=foreground, **kwargs)

        self._values = values
        self._values_current = []

        self._replace_values(values)

        self._selected_idx = -1

        self.listbox.bind('<<ListboxSelect>>', lambda _: self._onselect(), add=True)

    def _replace_values(self, values):
        if self.listbox.size() > 0:
            self.listbox.delete(0, tk.END)

        for _ in values:
            self.listbox.insert(tk.END, _)

        self._values_current = values

    def _select(self, idx):
        self._unselect()

        self.listbox.itemconfigure(idx, background=self._selectbackground, foreground=self._selectforeground,
                                   selectbackground=self._selectbackground, selectforeground=self._selectforeground)

        self._selected_idx = idx

    def _unselect(self):
        if self._selected_idx == -1:
            return

        self.listbox.itemconfigure(self._selected_idx, background=self._background, foreground=self._foreground,
                                   selectbackground=self._background, selectforeground=self._foreground)

        self._selected_idx = -1

    def _onselect(self):
        _ = self.listbox.curselection()
        if len(_) == 0:
            return
        idx = _[0]

        self._select(idx)

    def set(self, value, *, only=False):
        assert value in self._values

        self._unselect()

        if only:
            self._replace_values([value])
            self._select(0)
        else:
            if self._values_current is not self._values:
                self._replace_values(self._values)
            self._select(self._values.index(value))
            self.listbox.yview_moveto(self._selected_idx / len(self._values))

    def get(self):
        if self._selected_idx == -1:
            return None

        return self._values_current[self._selected_idx]
