"""Root widget."""


import json
from tkinter import ttk
from tkinter import filedialog as Tk_filedlg
from tkinter import Menu as Tk_Menu

from opentea.gui_tree.constants import BG_COLOR, WIDTH_UNIT, load_icons

from opentea.gui_tree.node_widgets import OTNodeWidget
from opentea.fastref import nob_pprint


class OTRoot(OTNodeWidget):
    """OT root widget."""

    def __init__(self, schema, tksession):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        """
        self._root = tksession
        super().__init__(schema)

        self._root.title(schema["name"])
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

        self._main_frame = ttk.Frame(self._root, padding="3 3 12 12")
        self._main_frame.grid(column=0, row=0, sticky="news")
        self._notebook = ttk.Notebook(self._main_frame, name='tab_holder')
        self._notebook.pack(fill="both", padx=2, pady=3, expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        self._init_gui()
        self._init_file_menu()
        self._root.mainloop()

    def _init_file_menu(self):
        """Create the top menu dialog."""
        self._menubar = Tk_Menu(self._root)
        self._filemenu = Tk_Menu(self._menubar, tearoff=0)
        icons = load_icons()
        self._filemenu.add_command(label="New  (Ctrl+N)",
                                   image=icons['new'],
                                   compound='left',
                                   command=self._menu_new_command)

        self._filemenu.add_command(label="Load  (Ctrl+O)",
                                   image=icons['load'],
                                   compound='left',
                                   command=self._menu_load_command)

        self._filemenu.add_command(label="Save  (Ctrl+S)",
                                   image=icons['save'],
                                   compound='left',
                                   command=self._menu_save_command)

        self._filemenu.add_separator()

        self._filemenu.add_command(label="Quit   (Ctrl+W)",
                                   image=icons['quit'],
                                   compound='left',
                                   command=self._menu_quit_command)

        self._menubar.add_cascade(label="File", menu=self._filemenu)

        self._helpmenu = Tk_Menu(self._menubar, tearoff=0)

        self._helpmenu.add_command(label="About",
                                   image=icons['about'],
                                   compound='left',
                                   command=self._menu_about_command)

        self._menubar.add_cascade(label="Help", menu=self._helpmenu)

        self._root.bind('<Control-o>', self._menu_load_command)
        self._root.bind('<Control-s>', self._menu_save_command)
        self._root.bind('<Control-n>', self._menu_new_command)
        self._root.bind('<Control-w>', self._menu_quit_command)
        self._root.bind('<Control-h>', self._dump_tree_data)
        self._root.config(menu=self._menubar)

    def _init_gui(self):
        """Start the recursive spawning of widgets."""
        for child in self.properties:
            self.tree[child] = OTTabWidget(
                self.properties[child],
                self._notebook)

    def _menu_quit_command(self, event=None):
        """Quit full application."""
        self._root.quit()

    def _dump_tree_data(self, event=None):
        """Quit full application."""
        print(nob_pprint(self.get()))

    def _menu_new_command(self, event=None):
        """Start new application."""
        self._init_gui()

    def _menu_load_command(self, event=None):
        """Load data in current application."""
        state_file = Tk_filedlg.askopenfilename(
            title="Select file")
        state = load_json_schema(state_file)
        self.set(state)

    def _menu_save_command(self, event=None):
        """Save data in current application."""
        output = Tk_filedlg.asksaveasfilename(
            title="Select file",
            defaultextension='.otsv')

        if output != '':
            dump = json.dumps(self.get(), indent=4)
            with open(output, 'w') as fout:
                fout.writelines(dump)

    def _menu_about_command(self):
        """Splashscreen about openTEA."""
        print('about')


def load_json_schema(schema_file):
    """Load schema file.

    limited to JSON storage

    Inputs :
    --------
    schema_file :  string
        path to a schema file

    Returns :
    ---------
    schema :
        a nest object with the schema
    """
    with open(schema_file, "r") as fin:
        schema = json.load(fin)
    return schema


# class TkinterObjectEncoder(json.JSONEncoder):
#     """Adapt JSON encoder to Tkinter types."""

#     def default(self, obj):
#         """Overide the default encoder."""
#         if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
#             out = json.JSONEncoder.default(self, obj)
#         elif isinstance(obj, (OTInteger, OTNumber, OTBoolean,
#                               OTChoice, OTContainerWidget,
#                               OTXorWidget,
#                               OTTabWidget, OTFileBrowser)):
#             try:
#                 out = obj.get()
#             except GetException:
#                 out = None
#         elif isinstance(obj, (OTDescription)):
#             out = None
#         else:
#             raise NotImplementedError()
#         return out
