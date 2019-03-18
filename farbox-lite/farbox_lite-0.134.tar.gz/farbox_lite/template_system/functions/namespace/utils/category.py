# coding: utf8
from __future__ import absolute_import

from farbox_lite.utils import smart_unicode
from farbox_lite.utils.functional import curry, cached_property
from farbox_lite.utils.lazy import get_value_from_data
from farbox_lite.render.apis.data import get_data, get_paginator, get_doc
from farbox_lite.template_system.utils import SafeUndefined

# category 相关的很难单独出来，所以放在 utils 里调用


def get_doc_category(doc):
    if isinstance(doc, dict) and doc.get('type') and doc.get('path'):
        doc_path = doc.get('path') or ''
        if '/' in doc_path:
            parent_path = doc_path.rsplit('/', 1)[0]
            return Category(parent_path)




class Category(object):
    def __init__(self, path_or_doc):
        if isinstance(path_or_doc, dict):
            self.raw = path_or_doc
            self.path = self.raw.get('path')
        else:
            path = path_or_doc
            path = smart_unicode(path).strip()
            folder = {}
            doc = get_doc(path=path)
            if doc and doc.get('type') == 'folder':
                folder = doc
            self.raw = folder
            self.path = path

    def __nonzero__(self):
        return bool(self.raw)


    def __getattr__(self, item):
        if item in self.raw:
            return self.raw.get(item)
        return self.__dict__.get(item, SafeUndefined())


    def __getitem__(self, item):
        return self.__getattr__(item)


    @cached_property
    def parents(self):
        # 得到所有的上级目录
        ps = []
        if not self.raw:
            return ps
        path_parts = self.path.split('/')[:-1][:50] # 最多50个层级
        parent_paths = []
        for i in range(len(path_parts)):
            parent_paths.append('/'.join(path_parts[:i+1]))
        parent_paths.reverse() # just reverse it for human
        parent_categories = []
        for parent_path in parent_paths:
            parent_category = Category(parent_path)
            if parent_category:
                parent_categories.append(parent_category)
        return parent_categories


    @cached_property
    def url(self):
        return u'/category/%s' % self.path



    @cached_property
    def posts(self):
        # 仅仅当前
        pager_name = '%s_child_posts' % self.path
        return get_data(type='post', path=self.path, pager_name=pager_name, level=1)

    @cached_property
    def posts_pager(self):
        pager_name = '%s_child_posts' % self.path
        return get_paginator(pager_name)


    @cached_property
    def all_posts(self):
        # 遍历所有
        pager_name = '%s_all_posts' % self.path
        return get_data(type='post', path=self.path, pager_name=pager_name)


    @cached_property
    def all_posts_pager(self):
        pager_name = '%s_all_posts' % self.path
        return get_paginator(pager_name)


    @cached_property
    def cover_url(self):
        return self.raw.get('cover') or ''
        
    @cached_property
    def cover(self):
        return self.cover_url

    @cached_property
    def images(self):
        # 仅仅当前
        pager_name = '%s_child_images' % self.path
        return get_data(type='image', path=self.path, pager_name=pager_name, level=1)


    @cached_property
    def images_pager(self):
        pager_name = '%s_child_images' % self.path
        return get_paginator(pager_name)


    @cached_property
    def all_images(self):
        # 遍历所有
        pager_name = '%s_all_images' % self.path
        return get_data(type='image', path=self.path, pager_name=pager_name)


    @cached_property
    def all_images_pager(self):
        pager_name = '%s_all_images' % self.path
        return get_paginator(pager_name)


