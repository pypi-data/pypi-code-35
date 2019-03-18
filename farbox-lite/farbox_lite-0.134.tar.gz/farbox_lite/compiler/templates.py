#coding: utf8
from __future__ import absolute_import
from farbox_lite.compiler.utils import get_file_list
from farbox_lite.utils import get_relative_path, same_slash, smart_unicode
from farbox_lite.utils.functional import curry
import os



template_resources_cache = {}



def is_allowed_template_resource(root, filepath):
    if not os.path.exists(filepath):
        return False
    relative_path = get_relative_path(filepath, root=root)
    relative_path = relative_path.lower()
    if relative_path in ['data']:
        return False
    elif relative_path.startswith('data/'):
        return False
    if os.path.isfile(filepath):
        ext = os.path.splitext(filepath)[-1].lower().strip('.')
        if ext not in ['html', 'js', 'css', 'otf', 'eot', 'ttf', 'woff', 'woff2', 'png', 'jpg', 'gif']:
            return False
        else:
            return True
    elif os.path.isdir(filepath):
        return True
    else:
        return False


def raw_get_template_resources(root):
    root = same_slash(root)
    root = os.path.join(root, 'template') # templates' folder
    if not os.path.isdir(root):
        return {}
    template_resources = {}
    template_resource_mtimes = {}
    allowed_func = curry(is_allowed_template_resource, root)
    template_resource_filepaths = get_file_list(root, filter_func=allowed_func)
    for filepath in template_resource_filepaths:
        mtime = os.path.getmtime(filepath)
        relative_path = get_relative_path(filepath, root=root).strip().lower()
        if not os.path.isfile(filepath):
            continue
        with open(filepath, 'rb') as f:
            file_content = f.read()
        template_resources[relative_path] = file_content
        template_resource_mtimes[relative_path] = (filepath, mtime)

        # +号衍生的路由
        relative_parent, filename = os.path.split(relative_path)
        just_name, ext = os.path.splitext(filename)
        if '+' in just_name:
            for sub_name in just_name.strip().split('+'):
                sub_name = sub_name.strip()
                if not sub_name:
                    continue
                sub_path = '%s/%s%s' % (relative_parent, sub_name, ext)
                sub_path = sub_path.lstrip('/')
                template_resources[sub_path] = file_content
                template_resource_mtimes[sub_path] = (filepath, mtime)

    template_resources['_'] = template_resource_mtimes

    return template_resources


def get_template_resources(root):
    root = same_slash(root)
    if not os.path.isdir(root):
        return {}
    if root in template_resources_cache:
        template_resources = template_resources_cache.get(root)
        return template_resources
    template_resources = raw_get_template_resources(root)
    template_resources_cache[root] = template_resources
    return template_resources



def update_template_resources(root):
    template_resources = raw_get_template_resources(root)
    template_resources_cache[root] = template_resources
    return template_resources

