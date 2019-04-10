from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class Content(VuetifyWidget):

    _model_name = Unicode('ContentModel').tag(sync=True)

    tag = Unicode(None, allow_none=True).tag(sync=True)





__all__ = ['Content']
