"""OT Schema Viewer
"""
from tkinter import filedialog as Tk_filedialog,  \
                    Variable   as Tk_Variable,  \
                    Label      as Tk_Label,  \
                    Menu       as Tk_Menu,  \
                    Button     as Tk_Button

from tkinter import ttk, Tk
import inspect
from glob import glob
import json
import os
from PIL import ImageTk, Image


WD_WIDTH = 1000
WD_HEIGHT = 900
BASE_DIR = inspect.getfile(inspect.currentframe())
BASE_DIR = os.path.dirname(os.path.abspath(BASE_DIR))


def load_json_schema(json_file):
    """ Loading json schema into a dictionnary"""
    with open(json_file, "r") as fin:
        schema = json.load(fin)
    return schema

def _load_icons():
    """Load icons from a specified directory

    """
    icons_dir = os.path.join(BASE_DIR, 'otinker_images')
    icons_pattern = '_icon.gif'
    icons_files = glob('%s/*%s'%(icons_dir, icons_pattern))
    icons = dict()
    for k in icons_files:
        key = os.path.basename(k).replace(icons_pattern, '')
        icons[key] = ImageTk.PhotoImage(Image.open(k))

    return icons

class OTBrowser():
    """ GUI for browsing Otinker schema files"""
    def __init__(self, schema=None):
        self._root = Tk()
        self._root.title('Otinker Browser')
        self._root.geometry("%dx%d" %(WD_WIDTH, WD_HEIGHT))
        self._init_paned_windows()
        self._init_file_menu()
        self._root.mainloop()

    def _init_paned_windows(self):
        """ Creating paned window that holds all elements

        Creating holder for tree view and tree view

        Creating. holder for properties and Table

        of propeties
        """

        self._pw = ttk.PanedWindow(orient="horizontal")
        self._pw.pack(fill="both", expand=True)
        self._tv_holder = ttk.LabelFrame(self._pw,
                                         text='Viewer',
                                         relief='sunken')


        self._pw.add(self._tv_holder)

        self._tree = ttk.Treeview(self._tv_holder,
                                  selectmode="browse",
                                  height=20)
        self._tree.pack(side="top", fill='both', expand=1)



        self._props_holder = ttk.LabelFrame(self._pw,
                                            text='Item properties',
                                            relief='sunken')

        self._props = ttk.Treeview(self._props_holder, height=20)
        self._props['columns'] = ('value')
        self._props.heading("#0", text='Name', anchor='w')
        self._props.heading('value', text='Value')
        self._props.column("#0", anchor="w")
        self._props.column('value', anchor='center', width=100)
        self._props.pack(side="top", fill='both', expand=1)

        self._pw.add(self._props_holder)

    def _init_file_menu(self):
        icons = _load_icons()
        self._menubar = Tk_Menu(self._root)
        self._filemenu = Tk_Menu(self._menubar, tearoff=0)


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
        self._root.bind('<Control-w>', self._menu_quit_command)

        self._root.config(menu=self._menubar)

    def _menu_quit_command(self, event=None):
        self._root.quit()


    def _menu_load_command(self, event=None):

        schema = Tk_filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select file",
            filetypes=(("OpenTea json files", "*.otsv"),
                       ("json schema files", "*.json"),
                       ("All files", "*.*")))

    def _menu_save_command(self, event=None):
        print('save')

    def _menu_about_command(self):
        print('about')

if __name__ == '__main__':
    OTBrowser()
