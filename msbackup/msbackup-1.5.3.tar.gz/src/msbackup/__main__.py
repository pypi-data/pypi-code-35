# -*- coding: utf-8 -*-
"""Точка входа в приложение."""

import sys

try:
    from msbackup.msbackup import main
except ImportError:
    from .msbackup import main


sys.exit(main())
