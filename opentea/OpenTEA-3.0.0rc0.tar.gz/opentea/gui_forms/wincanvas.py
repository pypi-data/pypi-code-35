"""Opentea module for wincanvas."""

def redirect_canvas_items(schema, root_frame, name):
    """Redirect to wincanvas widgets.

    The schema attributes trigger which string widget will be in use.

    Inputs :
    --------
    schema :  a schema object
    root_frame :  a Tk object were the widget will be grafted
    name : name of the element

    Outputs :
    --------
    none
    """
    if "ot_canvas_type" not in schema:
        raise RuntimeError("ot_canvas_type attribute is compulsory")

    if schema["ot_canvas_type"] == "image":
        out = WinCanvasImage(schema, root_frame, name)
    else:
        raise NotImplementedError(schema["ot_canvas_type"] + " not implemented")

class WinCanvasImage():
    """Class for Image handling in dynamic canvases"""

    def __init__(self):
        """Startup class"""
        pass
