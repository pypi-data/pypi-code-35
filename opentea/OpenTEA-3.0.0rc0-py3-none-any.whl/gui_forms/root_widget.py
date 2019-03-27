"""Root widget."""

import os
import yaml
import time

#from opentea.noob.validation import main_validate

import subprocess
from tkinter import ttk
from tkinter import filedialog as Tk_filedlg
from tkinter import Menu as Tk_Menu
from tkinter import Toplevel as Tk_Toplevel
from tkinter import Variable as Tk_Variable
from opentea.gui_forms.constants import BG_COLOR, load_icons, TextConsole
from opentea.gui_forms.node_widgets import (OTNodeWidget,
                                            OTTabWidget)
# from opentea.noob.noob import (nob_pprint,
#                                nob_get)

from opentea.noob.validation import (opentea_clean_data,
                                     opentea_resolve_require)
from opentea.noob.asciigraph import nob_asciigraph
from opentea.noob.inferdefault import nob_complete


class OTRoot(OTNodeWidget):
    """OT root widget."""

    def __init__(self, schema, data_start, tksession, calling_dir):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        data_start : nested object filled by default
        tksession : the main TKsession
        calling_dir : directory from which otinker was called
        """
        self._root = tksession
        self.icons = load_icons()
        self.schema = schema
        self.calling_dir = calling_dir
        super().__init__(schema)
        title = "untitled"
        if "title" in schema:
            title = schema["title"]

        self._root.title(title)
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

        self._main_frame = ttk.Frame(self._root, padding="3 3 12 12")
        self._main_frame.grid(column=0, row=0, sticky="news")

        self.main_nb = ttk.Notebook(self._main_frame, name='top_nb')
        self.main_nb.pack(fill="both", padx=2, pady=3, expand=True)

        self.toptabs = ttk.Frame(self.main_nb, name="forms")
        self.main_nb.add(self.toptabs, text="Forms")

        self.toptabs.nb = ttk.Notebook(self.toptabs, name='tab_nb')
        self.toptabs.nb.pack(fill="both", padx=2, pady=3, expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        ttk.Style().configure("TNotebook", background=BG_COLOR)
        self._init_gui()
        self._init_file_menu()
        self._root.mainloop()

    def _init_file_menu(self):
        """Create the top menu dialog."""
        self._menubar = Tk_Menu(self._root)
        self._filemenu = Tk_Menu(self._menubar, tearoff=0)
        self._filemenu.add_command(label="New  (Ctrl+N)",
                                   image=self.icons['new'],
                                   compound='left',
                                   command=self._menu_new_command)

        self._filemenu.add_command(label="Load  (Ctrl+O)",
                                   image=self.icons['load'],
                                   compound='left',
                                   command=self._menu_load_command)

        self._filemenu.add_command(label="Save  (Ctrl+S)",
                                   image=self.icons['save'],
                                   compound='left',
                                   command=self._menu_save_command)

        self._filemenu.add_separator()
        self._filemenu.add_command(label="Quit   (Ctrl+W)",
                                   image=self.icons['quit'],
                                   compound='left',
                                   command=self._menu_quit_command)
        self._menubar.add_cascade(label="File", menu=self._filemenu)

        self._treeviewmenu = Tk_Menu(self._menubar, tearoff=0)

        self._treeviewmenu.add_command(label="Show tree",
                                       image=self.icons['tree'],
                                       compound='left',
                                       command=self._dump_tree_data)

        self._menubar.add_cascade(label="Debug", menu=self._treeviewmenu)


        self._helpmenu = Tk_Menu(self._menubar, tearoff=0)

        self._helpmenu.add_command(label="About",
                                   image=self.icons['about'],
                                   compound='left',
                                   command=self._menu_about_command)

        self._menubar.add_cascade(label="Help", menu=self._helpmenu)

        self._root.bind('<Control-o>', self._menu_load_command)
        self._root.bind('<Control-s>', self._menu_save_command)
        self._root.bind('<Control-n>', self._menu_new_command)
        self._root.bind('<Control-w>', self._menu_quit_command)
        self._root.bind('<Control-h>', self._dump_tree_data)
        self._root.config(menu=self._menubar)
        self.toplevel = None
        self._root.bind_all('<<mem_check>>', self._mem_check, add="+")
        # DEBUG
        self._root.bind_all('<<mem_change>>', self._mem_change, add="+")

    def _mem_change(self, event):
        # print("Ping mem_change" + str(event.widget))
        pass

    def _mem_check(self, event):
        # print("Ping mem_check" + str(event.widget))
        checked_mem = opentea_resolve_require(self.get(), self.schema)
        self.set(checked_mem)
        self._root.event_generate('<<mem_change>>')

    def _init_gui(self):
        """Start the recursive spawning of widgets."""
        for child in self.properties:
            self.tree[child] = OTTabWidget(
                self.properties[child],
                self,
                child)

        compl1 = nob_complete(self.schema)
        compl2 = opentea_clean_data(compl1)
        compl3 = opentea_resolve_require(compl2, self.schema)
        self.set(compl3)

    def _menu_quit_command(self, event=None):
        """Quit full application."""
        self._root.quit()

    def _dump_tree_data(self, event=None):
        """Show memory """
        if self.toplevel is not None:
            self.toplevel.destroy()
        self.toplevel = Tk_Toplevel(self._root)
        self.toplevel.title('Tree View')
        self.toplevel.transient(self._root)
        memory = Tk_Variable(value=nob_asciigraph(self.get()))
        TextConsole(self.toplevel, memory)

    def _menu_new_command(self, event=None):
        """Start new application."""
        self._init_gui()

    def _menu_load_command(self, event=None):
        """Load data in current application."""
        state_file = Tk_filedlg.askopenfilename(
            title="Select file")
        with open(state_file, "r") as fin:
            state = yaml.load(fin)
        self.set(state)
        self._root.event_generate('<<mem_check>>')

    def _menu_save_command(self, event=None):
        """Save data in current application."""
        output = Tk_filedlg.asksaveasfilename(
            title="Select file",
            defaultextension='.yml')

        if output != '':
            dump = yaml.dumps(self.get(), default_flow_style=False)
            with open(output, 'w') as fout:
                fout.writelines(dump)

    def _menu_about_command(self):
        """Splashscreen about openTEA."""
        print('about')

    def execute(self, script):
        """execute a script"""
        full_script = os.path.join(self.calling_dir, script)
        print("Executing in subprocess ", full_script)
        start = time.time()
        dump = yaml.dump(self.get(), default_flow_style=False)
        try:
            os.remove("dataset_to_gui.yml")
        except FileNotFoundError:
            pass

        with open("dataset_from_gui.yml", 'w') as fout:
                fout.writelines(dump)
        subp = subprocess.Popen([
            "python",
            full_script, 
            "dataset_from_gui.yml"])
        subp.communicate()
        subp.wait()
        end = time.time()
        duration = str(round(end-start, 3)) + "s"
        
        success = True
        try:
            with open("dataset_to_gui.yml", 'r') as fin:
                data_in = yaml.load(fin)
                #main_validate(data_in, self.schema)
                self.set(data_in)
        except FileNotFoundError:
            success = False
            print("Process failed...")

        print("Process finished in "+duration)
        return success, duration


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
