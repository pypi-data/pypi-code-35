#coding: utf8
from __future__ import absolute_import
from math import ceil
import flask
import urllib
from flask import request
from farbox_lite.utils.functional import cached_property
from farbox_lite.utils.lazy import to_int
from farbox_lite.utils import smart_unicode


def compute_auto_pages(pages, current_page=1, max_count=10):
    # 1 ...... n
    if max_count < 6:
        max_count = 6
    if pages <= max_count:
        return range(1, pages+1)

    just_head = range(1, max_count-1) + [0, pages]
    just_foot = [1, 0] + range(pages-max_count+1, pages+1)

    if current_page in just_head and current_page!=pages:
        if current_page < max_count/2:
            return just_head
    if current_page in just_foot and current_page!=1:
        if current_page > pages-max_count/2:
            return just_foot

    auto_fix_count = (max_count - 2*2)/2
    head = [1, 2]
    foot = [pages-1, pages]
    _middle_list = range(current_page-auto_fix_count+1, current_page+auto_fix_count)
    middle_list = []
    for i in _middle_list:
        if 1<i<pages and i not in head and i not in foot:
            middle_list.append(i)
    result =  head
    if result[-1]+1 not in middle_list:
        result.append(0) # head fill
    result += middle_list
    if result[-1] and result[-1]+1 not in foot:
        result.append(0)
    result += foot
    return result



class Paginator(object):
    def __init__(self, query, per_page=3, page=1, is_safe=False):
        # query is like db.entry.find({'something': 'something'})
        page = to_int(page, 1, 10000) # 最多不超过10k页
        per_page = to_int(per_page, 3, 1000) # 单页不超过1k条记录
        if page * per_page > 100000: # 数据总数不能超过10w条
            flask.abort(404)

        self.query = query
        self.per_page = per_page
        self.total_pages = int(ceil(float(self.total_count) / per_page))
        self.pages = self.total_pages # 总页码数
        self.page = page
        self.next_page = page + 1
        self.previous_page = page - 1
        self.is_safe = is_safe # 如果为真的，则不对输出结果进行关键字hidden

        self.default_max_page_numbers = 10

    def __getitem__(self, item):
        # 主要是做 for 循环用的
        if hasattr(self.list_object, '__getitem__'):
            return self.list_object.__getitem__(item)

    @cached_property
    def pre_page(self):
        return self.previous_page

    @cached_property
    def total_count(self):
        if isinstance(self.query, (list, tuple)):
            return len(self.query)
        if hasattr(self.query, 'count') and hasattr(self.query.count, '__call__'):
            return self.query.count()
        else:
            return len(self.query)

    @cached_property
    def has_previous(self):
        return self.page > 1

    @cached_property
    def has_pre(self):
        return self.has_previous

    @cached_property
    def has_next(self):
        return self.page < self.total_pages


    @staticmethod
    def get_page_url(page_number):
        if '/page/' in request.url:
            base = request.path.split('/page/',1)[0]
        else:
            base = request.path
        if page_number != 1:
            url = ('%s/page/%s'%(base, page_number)).replace('//','/')
        else:
            url = base.replace('//','/') or '/'
        if request.query_string:
            query_string = request.query_string
            if '%' in query_string:
                query_string = urllib.unquote(query_string)
            url += '?%s'%smart_unicode(query_string)
        url = url.replace('"', '%22').replace("'", '%27') # 避免被跨站
        return url

    @cached_property
    def previous_page_url(self):
        if self.has_previous:
            return self.get_page_url(self.previous_page)
        else:
            return '#'

    @cached_property
    def pre_page_url(self):
        return self.previous_page_url

    @cached_property
    def pre_url(self):
        return self.pre_page_url

    @cached_property
    def next_page_url(self):
        if self.has_next:
            return self.get_page_url(self.next_page)
        else:
            return '#'

    @cached_property
    def next_url(self):
        return self.next_page_url

    @cached_property
    def list_object(self):
        if self.page > self.total_pages or self.page < 1:
            return []
        start_at = (self.page-1) * self.per_page
        data = self.query[start_at: start_at+self.per_page]
        return list(data)

    @cached_property
    def page_numbers(self):
        return self.get_page_numbers()

    def set_default_max_page_numbers(self, numbers):
        # 设定 auto_pages 计算时，最大的长度跨度
        numbers = to_int(numbers)
        if isinstance(numbers, int) and 50>numbers>3:
            self.default_max_page_numbers = numbers
        return ''


    def get_page_numbers(self, max_count=None):
        if not max_count:
            max_count = self.default_max_page_numbers
        return compute_auto_pages(self.total_pages, current_page=self.page, max_count=max_count)
