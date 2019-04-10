from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class Container(VuetifyWidget):

    _model_name = Unicode('ContainerModel').tag(sync=True)

    align_baseline = Bool(None, allow_none=True).tag(sync=True)

    align_center = Bool(None, allow_none=True).tag(sync=True)

    align_content_center = Bool(None, allow_none=True).tag(sync=True)

    align_content_end = Bool(None, allow_none=True).tag(sync=True)

    align_content_space_around = Bool(None, allow_none=True).tag(sync=True)

    align_content_space_between = Bool(None, allow_none=True).tag(sync=True)

    align_content_start = Bool(None, allow_none=True).tag(sync=True)

    align_end = Bool(None, allow_none=True).tag(sync=True)

    align_start = Bool(None, allow_none=True).tag(sync=True)

    fill_height = Bool(None, allow_none=True).tag(sync=True)

    fluid = Bool(None, allow_none=True).tag(sync=True)

    id = Unicode(None, allow_none=True).tag(sync=True)

    justify_center = Bool(None, allow_none=True).tag(sync=True)

    justify_end = Bool(None, allow_none=True).tag(sync=True)

    justify_space_around = Bool(None, allow_none=True).tag(sync=True)

    justify_space_between = Bool(None, allow_none=True).tag(sync=True)

    justify_start = Bool(None, allow_none=True).tag(sync=True)

    tag = Unicode(None, allow_none=True).tag(sync=True)

    d_inline = Bool(None, allow_none=True).tag(sync=True)

    d_block = Bool(None, allow_none=True).tag(sync=True)

    d_contents = Bool(None, allow_none=True).tag(sync=True)

    d_flex = Bool(None, allow_none=True).tag(sync=True)

    d_grid = Bool(None, allow_none=True).tag(sync=True)

    d_inline_block = Bool(None, allow_none=True).tag(sync=True)

    d_inline_flex = Bool(None, allow_none=True).tag(sync=True)

    d_inline_grid = Bool(None, allow_none=True).tag(sync=True)

    d_inline_table = Bool(None, allow_none=True).tag(sync=True)

    d_list_item = Bool(None, allow_none=True).tag(sync=True)

    d_run_in = Bool(None, allow_none=True).tag(sync=True)

    d_table = Bool(None, allow_none=True).tag(sync=True)

    d_table_caption = Bool(None, allow_none=True).tag(sync=True)

    d_table_column_group = Bool(None, allow_none=True).tag(sync=True)

    d_table_header_group = Bool(None, allow_none=True).tag(sync=True)

    d_table_footer_group = Bool(None, allow_none=True).tag(sync=True)

    d_table_row_group = Bool(None, allow_none=True).tag(sync=True)

    d_table_cell = Bool(None, allow_none=True).tag(sync=True)

    d_table_column = Bool(None, allow_none=True).tag(sync=True)

    d_table_row = Bool(None, allow_none=True).tag(sync=True)

    d_none = Bool(None, allow_none=True).tag(sync=True)

    d_initial = Bool(None, allow_none=True).tag(sync=True)

    d_inherit = Bool(None, allow_none=True).tag(sync=True)

    grid_list_xs = Bool(None, allow_none=True).tag(sync=True)

    grid_list_sm = Bool(None, allow_none=True).tag(sync=True)

    grid_list_md = Bool(None, allow_none=True).tag(sync=True)

    grid_list_lg = Bool(None, allow_none=True).tag(sync=True)

    grid_list_xl = Bool(None, allow_none=True).tag(sync=True)





__all__ = ['Container']
