#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2019/4/6'
Info:
        
"""

import os, sys

sys.path.insert(0, '..')
# import start


# import end
version = sys.version_info.major
if version == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    import importlib

    importlib.reload(sys)