'''
policies
========

.. warning:: This module is flagged as "beta", and may change.

The following methods allow for interaction into the Tenable.sc 
`Scan Policies <https://docs.tenable.com/sccv/api/Scan-Policy.html>`_ API.  
These items are typically seen under the **Scan Policies** section of Tenable.sc.

Methods available on ``sc.policies``:

.. rst-class:: hide-signature
.. autoclass:: ScanResultAPI

    .. automethod:: copy
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: export_policy
    .. automethod:: import_policy
    .. automethod:: list
    .. automethod:: share
    .. automethod:: template_details
    .. automethod:: template_list
'''
from .base import SCEndpoint
from io import BytesIO
import json

