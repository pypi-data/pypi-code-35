# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Back compat shim for remote runs."""
# TODO: Remove this file once remote runs have fully migrated to use SDK's remote script.
from ._azureautomlsettings import AzureAutoMLSettings as _AutoMLSettings
