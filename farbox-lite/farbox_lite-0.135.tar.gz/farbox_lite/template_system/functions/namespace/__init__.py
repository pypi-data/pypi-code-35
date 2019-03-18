# coding: utf8
from __future__ import absolute_import
from farbox_lite.template_system.func import get_functions_in_a_file_obj
default_variables = {}

sub_names = ['post', 'site', 'image', 'html', 'data',
             'request', 'response', 'shortcut', 'syntax_block'
             ]
for sub_name in sub_names:
    exec('from farbox_lite.template_system.functions.namespace import %s' % sub_name)
    exec('default_variables.update(get_functions_in_a_file_obj(%s))' % sub_name)

    try: # 非函数性质的
        exec('default_variables.update(%s.default_variables)' % sub_name)
    except:
        pass


# 实体的file class
parts = []
for part in parts:
    default_variables.update(get_functions_in_a_file_obj(part))



