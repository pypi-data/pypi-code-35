"""Module for containers widgets."""

from tkinter import ttk
from tkinter import Canvas as Tk_Canvas
from tkinter import Menu as Tk_Menu

from opentea.gui_forms.constants import (
    WIDTH_UNIT,
    BG_COLOR,
    GetException,
    SetException,
    SwitchForm)

from opentea.gui_forms.leaf_widgets import (OTInteger,
                                            OTNumber,
                                            OTEmpty,
                                            OTChoice,
                                            OTBoolean,
                                            OTFileBrowser,
                                            OTDescription)


def redirect_widgets(schema, root_frame):
    """Redirect to widgets.

    The schema attributes trigger which widget will be in use.

    Inputs :
    --------
    schema :  a schema object
    root_frame :  a Tk object were the widget will be grafted

    Outputs :
    --------
    none
    """
    out = OTEmpty(schema, root_frame)
    if "properties" in schema:
        out = OTContainerWidget(schema, root_frame)
    elif "oneOf"in schema:
        out = OTXorWidget(schema, root_frame)
    elif "enum" in schema:
        out = OTChoice(schema, root_frame)
    elif "type" in schema:
        if schema['type'] == 'integer':
            out = OTInteger(schema, root_frame)
        elif schema['type'] == 'number':
            out = OTNumber(schema, root_frame)
        elif schema['type'] == 'boolean':
            out = OTBoolean(schema, root_frame)
        elif schema["type"] == "string":
            if "ot_type" in schema:
                if schema["ot_type"] == "desc":
                    out = OTDescription(schema, root_frame)
                elif schema["ot_type"] == "docu":
                    out = OTEmpty(schema, root_frame)
                elif schema["ot_type"] == "file":
                    out = OTFileBrowser(schema, root_frame)
        elif schema["type"] == "array":
            out = OTMultipleWidget(schema, root_frame)
    return out


class OTNodeWidget():
    """Factory for OpenTea Widgets Containers."""

    def __init__(self, schema):
        """Startup class."""
        self.tree = dict()
        self.properties = schema["properties"]

    def get(self):
        """Get the data of children widgets.

        Returns :
        ---------
        a dictionnary with the get result of childrens
        """
        out = {}
        for child in self.properties:
            try:
                found = self.tree[child].get()
                if found is not None:
                    out[child] = found
            except GetException:
                pass
        if out == {}:
            out = None
        return out

    def set(self, dict_):
        """Get the data of children widgets.

        Input :
        -------
        a dictionnary with the value of the childrens"""
        for child in self.properties:
            if child in dict_:
                try:
                    self.tree[child].set(dict_[child])
                except SetException:
                    pass


class OTContainerWidget(OTNodeWidget):
    """OT container widget."""

    def __init__(self, schema, root_frame, n_width=1):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        n_width : float
             relative size of the widget

        """
        super().__init__(schema)
        title = ""
        if "title" in schema:
            title = schema["title"]
        name = "dummy"
        if "name" in schema:
            name = schema["name"]
        self._holder = ttk.LabelFrame(root_frame,
                                      text=title,
                                      name=name,
                                      relief="sunken",
                                      width=n_width*WIDTH_UNIT)
        """Forcing the widget size"""
        self._forceps = ttk.Frame(self._holder,
                                  width=n_width*WIDTH_UNIT,
                                  height=1)
        self._holder.pack(side="top", fill="x",
                          padx=2, pady=2, expand=False)
        self._forceps = ttk.Frame(self._holder,
                                  width=WIDTH_UNIT,
                                  height=1)
        self._forceps.pack(side="top")
        # CHILDREN
        for name_child in self.properties:
            schm_child = self.properties[name_child]
            self.tree[name_child] = redirect_widgets(schm_child, self._holder)


class OTTabWidget(OTNodeWidget):
    """OT Tab widget container.

    Called for the 1st layer of nodes in the global schema
    """

    def __init__(self, schema, notebook):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        notebook :  a Tk notebook object were the widget will be grafted
        """
        super().__init__(schema)
        self._notebook = notebook
        self._tab = ttk.Frame(self._notebook, name=schema["name"])
        self._notebook.add(self._tab, text=schema["title"])
        # SCROLL FORM
        _scroll_f = ttk.Frame(self._tab)
        _scroll_f.pack(side="top", fill="both", expand=True)
        _scroll_f.columnconfigure(0, weight=1)
        _scroll_f.columnconfigure(1, weight=0)
        _scroll_f.rowconfigure(0, weight=1)
        _scroll_f.rowconfigure(1, weight=0)
        self._can_scroll = Tk_Canvas(_scroll_f,
                                     background=BG_COLOR,
                                     highlightbackground=BG_COLOR,
                                     highlightcolor=BG_COLOR)

        self._can_scroll.configure(width=1000, height=300)
        _scroll_vert = ttk.Scrollbar(_scroll_f,
                                     orient="vertical",
                                     command=self._can_scroll.yview)
        self._can_scroll.configure(yscrollcommand=_scroll_vert.set)
        _scroll_horz = ttk.Scrollbar(_scroll_f, orient="horizontal",
                                     command=self._can_scroll.xview)
        self._can_scroll.configure(xscrollcommand=_scroll_horz.set)
        self._can_scroll.grid(row=0, column=0, sticky="news")
        _scroll_vert.grid(row=0, column=1, sticky="ns")
        _scroll_horz.grid(row=1, column=0, sticky="we")

        self._out_frame = ttk.Frame(self._can_scroll)

        self._can_scroll.create_window((0, 0),
                                       window=self._out_frame,
                                       anchor='nw')
        # FOOTER
        _footer_f = ttk.Frame(self._tab)
        _footer_f.pack(side="top", fill="both", padx=2, pady=3)

        # button_var = StringVar(value="dummy info")
        _button_lb = ttk.Label(_footer_f, text="button_var")
        _button_bt = ttk.Button(_footer_f, text="Process")
        _button_bt.pack(side="right", padx=2, pady=2)
        _button_lb.pack(side="right", padx=2, pady=2)

        # CHILDREN
        for name in schema["properties"]:
            self.tree[name] = redirect_widgets(
                schema["properties"][name],
                self._out_frame)

        self._out_frame.bind("<Configure>",
                             self._update_canvas_bbox_from_inside)

    def _update_canvas_bbox_from_inside(self, event=None):
        """Smart grid upon widget size.

        Regrid the object according to the width of the window
        """
        self._can_scroll.configure(scrollregion=self._can_scroll.bbox("all"))
        ncols = max(int(self._notebook.winfo_width()/WIDTH_UNIT + 0.5), 1)
        height = 0
        for children in self._out_frame.winfo_children():
            height += children.winfo_height()
        limit_depth = height / ncols
        max_depth = 0
        x_pos = 10 + 0*WIDTH_UNIT
        y_pos = 10
        for children in self._out_frame.winfo_children():
            children.place(x=x_pos,
                           y=y_pos,
                           anchor="nw")
            y_pos += children.winfo_height() + 2

            if y_pos > limit_depth and ncols > 1:
                max_depth = y_pos
                x_pos += WIDTH_UNIT + 20
                y_pos = 10
            else:
                max_depth = height
        self._out_frame.configure(height=max_depth+40,
                                  width=ncols*(WIDTH_UNIT+20)+20)


class OTMultipleWidget():
    """OT multiple widget."""

    def __init__(self, schema, root_frame):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        n_width : float
             relative size of the widget
        """
        self.tree = list()
        self.item_schema = schema["items"]
        title = ""
        if "title" in schema:
            title = schema["title"]
        holder = ttk.LabelFrame(
            root_frame,
            text=title,
            name=schema["name"],
            relief="sunken",
            width=2*WIDTH_UNIT)

        holder.pack(side="top", fill="x", padx=2, pady=2, expand=False)
        forceps = ttk.Frame(holder, width=2*WIDTH_UNIT, height=1)
        self.tvw = ttk.Treeview(
            holder,
            selectmode="browse",
            height=15)
        scroll_vert = ttk.Scrollbar(
            holder,
            orient="vertical",
            command=self.tvw.yview)
        self.tvw.configure(yscrollcommand=scroll_vert.set)
        self.switchform = SwitchForm(
            holder,
            width=WIDTH_UNIT,
            name='tab_holder')
        forceps.grid(column=0, row=1, columnspan=3)
        scroll_vert.grid(column=1, row=1, sticky="news")
        self.tvw.grid(column=0, row=1, sticky="news")
        self.switchform.grid(column=2, row=1, rowspan=2, sticky="news")
        self.switchform.grid_propagate(0)
        item_props = self.item_schema["properties"]
        self.tvw["columns"] = tuple(item_props.keys())
        col_width = int(WIDTH_UNIT/(len(self.tvw["columns"])+1))
        self.tvw.column("#0", width=col_width)
        for key in item_props:
            title = key
            if "title" in item_props[key]:
                title = item_props[key]["title"]
            self.tvw.column(key, width=col_width)
            self.tvw.heading(key, text=title)

        dummy = []
        for i in range(2):
            lbl = "line_"+str(i)
            dummy.append({"name": lbl})
        self.set(dummy)

        def tv_simple_click(event):
            """Handle a simple click on treeview."""
            # col = self.tvw.identify_column(event.x)
            row = self.tvw.identify_row(event.y)
            self.switchform.sf_raise(row)

        self.tvw.bind("<Button-1>", tv_simple_click)

    def get(self):
        """Get the data of children widgets.

        Returns :
        ---------
        a dictionnary with the get result of childrens
        """
        out = list()
        for child in self.tree:
            try:
                found = child.get()
                if found is not None:
                    out.append(found)
            except GetException:
                pass
        if not out:
            out = None
        return out

    def set(self, list_):
        """Get the data of children widgets.

        Input :
        -------
        a list with the value of the childrens"""
        ingoing_childs = [item["name"] for item in list_]
        remaining_childs = ingoing_childs.copy()

        itemids_to_delete = []
        for item_id in self.tree:
            item_name = self.tree[item_id]["name"]
            if item_name not in ingoing_childs:
                itemids_to_delete.append(item_id)
            else:
                data_in = list_[ingoing_childs.index(item_name)]
                self.tree[item_id].set(data_in)
                remaining_childs.remove(item_name)

        for item_id in itemids_to_delete:
            del(self.tree[item_id])

        for item_name in remaining_childs:
            data_in = list_[ingoing_childs.index(item_name)]
            self.tree.insert(-1, OTMultipleItem(self, item_name))
            self.tree[-1].set(data_in)

    def _reorder_items(self, ingoing_childs):
        """Reorder the items upon a list.

        Must chanque the order in self.tree,
        and show it on the self.tvw"""


class OTMultipleItem(OTContainerWidget):
    """OT  multiple widget."""

    def __init__(self, mutiple, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        mutiple :  a Tk object were the widget will be grafted
        """
        self.tab = mutiple.switchform.add(name, title=name)
        super().__init__(mutiple.item_schema, self.tab)
        mutiple.tvw.insert("", "end", iid=name, text=name)


class OTXorWidget():
    """OT  Or-exclusive / oneOf widget."""

    def __init__(self, schema, root_frame, n_width=1):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        n_width : float
             relative size of the widget
        """
        self.tree = dict()
        self.current_child = None
        self._schema = schema
        title = self._schema["name"]
        if "title" in self._schema:
            title = self._schema["title"]

        self._holder = ttk.LabelFrame(root_frame,
                                      text=title,
                                      name=self._schema["name"],
                                      relief="sunken",
                                      width=n_width*WIDTH_UNIT)

        self._forceps = ttk.Frame(self._holder,
                                  width=n_width*WIDTH_UNIT,
                                  height=1)
        self._menu_bt = ttk.Menubutton(self._holder,
                                       text="None")

        self._xor_holder = ttk.Frame(self._holder)

        self._holder.pack(side="top", fill="x",
                          padx=2, pady=2, expand=False)
        self._forceps.pack(side="top")
        self._menu_bt.pack(side="top")
        self._xor_holder.pack(side="top", fill="x",
                              padx=2, pady=2, expand=False)

        self._menu_bt.menu = Tk_Menu(self._menu_bt, tearoff=False)
        self._menu_bt["menu"] = self._menu_bt.menu

        for oneof_item in self._schema["oneOf"]:
            nam = oneof_item["required"][0]
            ch_s = oneof_item["properties"][nam]
            title = nam
            if "title" in ch_s:
                title = ch_s["title"]
            self._menu_bt.menu.add_command(
                label=title,
                command=lambda nam=nam: self._xor_callback(nam))

        self._xor_callback(self._schema["default"])

    def _xor_callback(self, name_child, data_in=None):
        """Reconfigure XOR button.

        Inputs :
        --------
        name_child : sting, naming the child object
        data_in : dictionary used to pre-fill the data
        """
        self.current_child = name_child
        child_schema = None
        for possible_childs in self._schema["oneOf"]:
            if possible_childs["required"][0] == name_child:
                child_schema = possible_childs["properties"][name_child]

        for child_widget in self._xor_holder.winfo_children():
            child_widget.destroy()

        self.tree = dict()
        self.tree[name_child] = OTContainerWidget(child_schema,
                                                  self._xor_holder)
        if data_in is None:
            self.tree[name_child].set(dict())
        else:
            self.tree[name_child].set(data_in)

        title = name_child
        if "title" in child_schema:
            title = child_schema["title"]
        self._menu_bt.configure(text=title)

    def get(self):
        """Get the data of children widgets.

        Returns :
        ---------
        a dictionnary with the get result of current children
        """
        out = dict()
        try:
            found = self.tree[self.current_child].get()
            if found is not None:
                out[self.current_child] = found
        except GetException:
            pass
        if out == {}:
            out = None
        return out

    def set(self, dict_):
        """Get the data of children widgets.

        Input :
        -------
        a dictionnary with the value of the childrens
        """
        given_keys = dict_.keys()
        if len(given_keys) > 1:
            raise SetException("Multiple matching option, skipping...")

        for child in self._schema["oneOf"]:
            if child in dict_:
                try:
                    self._xor_callback(child, dict_[child])
                except SetException:
                    pass
