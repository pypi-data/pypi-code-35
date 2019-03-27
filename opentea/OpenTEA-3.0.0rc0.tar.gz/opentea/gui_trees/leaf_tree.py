"""Module for leaf widgets."""

from tkinter import ttk
from tkinter import Variable as Tk_Variable
from tkinter import Label as Tk_Label
from tkinter import filedialog as Tk_filedlg

from opentea.gui_forms.constants import (
    WIDTH_UNIT,
    LINE_HEIGHT,
    BG_COLOR,
    load_icons,
    GetException,
    SetException)


class LeafWidget():
    """Factory for OpenTea Widgets."""

    def __init__(self, schema, root_frame):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        holder_nlines : integer
            custom number of lines for holder
        """
        self.tree = dict()
        self._tkvar = Tk_Variable()
        if "default" in schema:
            self._tkvar.set(schema['default'])

        self._holder = ttk.Frame(root_frame,
                                 name=schema["name"],
                                 width=WIDTH_UNIT,
                                 height=LINE_HEIGHT)
        self._holder.pack(side="top", fill="x")

        self._title = schema['name']
        if "title" in schema:
            self._title = schema['title']

        self._label = Tk_Label(self._holder,
                               text=self._title,
                               background=BG_COLOR,
                               justify="right",
                               wraplength=int(0.5*WIDTH_UNIT))
        self._label.place(relx=0.5, rely=0.5, anchor="se")


class _OTEntry(LeafWidget):
    """Factory for OpenTea Entries."""

    def __init__(self, schema, root_frame):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame)

        self._inits_entry()

    def _inits_entry(self):
        """Initialise entry."""
        self._status = Tk_Label(self._holder,
                                text="no status yet",
                                background=BG_COLOR,
                                foreground="red",
                                justify="left",
                                compound="left",
                                wraplength=WIDTH_UNIT,
                                width=WIDTH_UNIT)
        self._entry = ttk.Entry(self._holder, textvariable=self._tkvar)
        self._entry.place(relwidth=0.5, relx=0.5, rely=0.5, anchor="sw")
        self._status.place(relx=0.5, rely=0.5, anchor="n")

        self._holder.config(height=2 * LINE_HEIGHT)

        self._tkvar.trace('w', self._update_status_callback)

    def _update_status_callback(self, *args):
        """Redirect upon status callback."""
        try:
            self.get()
            self._status.config(text='', image='')
        except GetException:
            icons = load_icons()
            txt = 'Invalid input "%s"' % (self._entry.get())
            self._status.config(text=txt, fg='red', image=icons['invalid'])


class OTInteger(_OTEntry):
    """OTinteger variable."""

    def get(self):
        """Return python integer."""
        try:
            out = int(self._tkvar.get())
        except ValueError:
            raise GetException()
        return out

    def set(self, value):
        """Set integer to widget."""
        try:
            int_val = int(value)
            self._tkvar.set(int_val)
        except ValueError:
            raise SetException()


class OTNumber(_OTEntry):
    """OTNumber floats."""

    def get(self):
        """Return python float."""
        try:
            out = float(self._tkvar.get())
        except ValueError:
            raise GetException()
        return out

    def set(self, value):
        """Set float to widget."""
        try:
            float_val = float(value)
            self._tkvar.set(float_val)
        except ValueError:
            raise SetException()


class OTBoolean(LeafWidget):
    """OT booleans."""

    def __init__(self, schema, root_frame):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame)
        self._label.place(relx=0.5, rely=0.5, anchor="e")
        self._cbutt = ttk.Checkbutton(self._holder, variable=self._tkvar)
        self._cbutt.place(relx=0.5, rely=0.5, anchor="w")

    def get(self):
        """Returns python boolean."""
        try:
            out = bool(self._tkvar.get())
        except ValueError:
            raise GetException()
        return out

    def set(self, value):
        """Set boolean to widget."""
        try:
            bool_val = bool(value)
            self._tkvar.set(bool_val)
        except ValueError:
            raise SetException()


class OTChoice(LeafWidget):
    """OT choices widget."""

    def __init__(self, schema, root_frame):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame)
        n_lines = max(len(schema["enum"]), 1)
        self._holder.config(height=n_lines * LINE_HEIGHT)
        rel_step = 1./n_lines
        current_rely = 1*rel_step

        self._label.place(relx=0.5, rely=current_rely, anchor="se")

        titles = schema["enum"]
        if "enum_titles" in schema:
            titles = schema["enum_titles"]

        for value, title in zip(schema["enum"], titles):
            rad_btn = ttk.Radiobutton(self._holder,
                                      text=title,
                                      value=value,
                                      variable=self._tkvar)
            rad_btn.place(relx=0.5, rely=current_rely, anchor="sw")
            current_rely += rel_step

    def get(self):
        """Return python string."""
        out = self._tkvar.get()
        return out

    def set(self, value):
        """Set choice to widget."""
        self._tkvar.set(value)


class OTFileBrowser(LeafWidget):
    """OT file/folder browser widget."""

    def __init__(self, schema, root_frame):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame)

        self._filter = []
        self._isdirectory = False
        if 'ot_filter' in schema:
            filters = schema['ot_filter']
            if 'directory' in filters:
                self._isdirectory = True
            else:
                for ext in filters:
                    filetype = ("%s files" % ext, "*.%s" % (ext))
                    self._filter.append(filetype)

        self._label.place(relx=0.5, rely=0.5, anchor="e")

        self._path = ttk.Entry(self._holder,
                               textvariable=self._tkvar,
                               state='disabled',
                               foreground='black')
        self._path.place(relx=0.5, rely=0.5, relwidth=0.4, anchor="w")

        self._btn = ttk.Button(self._holder,
                               text="...",
                               # image=load_icons['load'],
                               width=0.1*WIDTH_UNIT,
                               compound='left',
                               command=self._browse)
        self._btn.place(relx=0.9, rely=0.5, anchor="w")

    def _browse(self, event=None):
        """Browse directory or files."""
        if self._isdirectory:
            path = Tk_filedlg.askdirectory(title=self._title)
        else:
            path = Tk_filedlg.askopenfilename(title=self._title,
                                              filetypes=self._filter)
        self._tkvar.set(path)

    def get(self):
        """Return data."""
        return self._tkvar.get()

    def set(self, value):
        """Set content."""
        self._tkvar.set(value)


class OTDescription(LeafWidget):
    """OT descriptin field."""

    def __init__(self, schema, root_frame):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame)
        del self._tkvar
        self._holder.pack_configure(side="bottom", fill="x")

        title = schema['name']
        if "title" in schema:
            title = schema['title']

        self._label = Tk_Label(self._holder,
                               text=title,
                               background=BG_COLOR,
                               justify="right",
                               wraplength=int(0.5*WIDTH_UNIT))

        self._label.config(justify="left",
                           text=schema["default"],
                           wraplength=WIDTH_UNIT*0.8)
        self._label.pack(side="bottom", fill="x")

    def get(self):
        """Return data."""
        return None

    def set(self, value):
        """Set content."""


class OTEmpty(LeafWidget):
    """OT widget for unimplemented types."""

    def __init__(self, schema, root_frame):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame)
        title = schema['name']
        if "title" in schema:
            title = schema['title']

        self._label = Tk_Label(self._holder,
                               text=title,
                               background=BG_COLOR,
                               justify="right",
                               wraplength=int(0.5*WIDTH_UNIT))

        del self._tkvar
        del self._holder
        info = []
        for item in ["name", "title", "type", "ot_type"]:
            if item in schema:
                info.append(item + " = " + schema[item])
        self._label.configure(text="\n".join(info))
        self._label.pack(side="top", padx=2, pady=2)

    def get(self):
        """Return data."""
        return None

    def set(self, value):
        """Set content."""
