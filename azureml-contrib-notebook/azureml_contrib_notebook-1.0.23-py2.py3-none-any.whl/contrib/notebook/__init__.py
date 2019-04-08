# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Include notebook extension to capture notebooks on runs."""
from azureml.contrib.notebook.extension import Extension, load_ipython_extension

__all__ = [
    "Extension",
    "load_ipython_extension"
]


def _jupyter_server_extension_paths():
    return [{
        "module": "notebook"
    }]


# Jupyter Extension points
def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        src="_scripts",
        dest="azureml",
        require="azureml/kernel")]
