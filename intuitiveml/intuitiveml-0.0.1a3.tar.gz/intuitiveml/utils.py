from IPython.display import display, clear_output
from ipywidgets import Button

def gen_button(desc, obj, **kwargs):
    button = Button(description="Show {}".format(desc))
    def on_button_clicked(b):
        if button.description == "Show {}".format(desc):
            if callable(obj):
                display(obj(**kwargs))
            else:
                display(obj)
            button.description = "Hide {}".format(desc)
        else:
            button.description = "Show {}".format(desc)
            clear_output()
            display(button)
    button.on_click(on_button_clicked)
    return button