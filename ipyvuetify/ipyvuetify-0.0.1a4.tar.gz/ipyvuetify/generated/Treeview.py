from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class Treeview(VuetifyWidget):

    _model_name = Unicode('TreeviewModel').tag(sync=True)

    activatable = Bool(None, allow_none=True).tag(sync=True)

    active = List(None, allow_none=True).tag(sync=True)

    active_class = Unicode(None, allow_none=True).tag(sync=True)

    dark = Bool(None, allow_none=True).tag(sync=True)

    expand_icon = Unicode(None, allow_none=True).tag(sync=True)

    hoverable = Bool(None, allow_none=True).tag(sync=True)

    indeterminate_icon = Unicode(None, allow_none=True).tag(sync=True)

    item_children = Unicode(None, allow_none=True).tag(sync=True)

    item_key = Unicode(None, allow_none=True).tag(sync=True)

    item_text = Unicode(None, allow_none=True).tag(sync=True)

    items = List(None, allow_none=True).tag(sync=True)

    light = Bool(None, allow_none=True).tag(sync=True)

    loading_icon = Unicode(None, allow_none=True).tag(sync=True)

    multiple_active = Bool(None, allow_none=True).tag(sync=True)

    off_icon = Unicode(None, allow_none=True).tag(sync=True)

    on_icon = Unicode(None, allow_none=True).tag(sync=True)

    open = List(None, allow_none=True).tag(sync=True)

    open_all = Bool(None, allow_none=True).tag(sync=True)

    open_on_click = Bool(None, allow_none=True).tag(sync=True)

    return_object = Bool(None, allow_none=True).tag(sync=True)

    search = Unicode(None, allow_none=True).tag(sync=True)

    selectable = Bool(None, allow_none=True).tag(sync=True)

    selected_color = Unicode(None, allow_none=True).tag(sync=True)

    transition = Bool(None, allow_none=True).tag(sync=True)

    value = List(None, allow_none=True).tag(sync=True)


Treeview.active.default_value=None
Treeview.items.default_value=None
Treeview.open.default_value=None
Treeview.value.default_value=None



__all__ = ['Treeview']
