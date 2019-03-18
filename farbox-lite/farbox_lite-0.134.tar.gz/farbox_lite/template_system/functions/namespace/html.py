# coding: utf8
from __future__ import absolute_import
import os
import uuid
from flask import g

from farbox_lite.utils import smart_unicode, get_md5
from farbox_lite.utils.functional import cached_property
from farbox_lite.utils.lazy import get_value_from_data
from farbox_lite.utils.url import join_url
from farbox_lite.utils.html import html_escape, re_html_dom, linebreaks as _linebreaks

from farbox_lite.utils.web.url import get_url_with_prefix
from farbox_lite.utils.web.cache_for_function import cache_result
from farbox_lite.utils.web.request import get_language

from farbox_lite.render.apis.data import get_paginator
from farbox_lite.render.utils.render import render_api_template



class Html(object):
    def __getattr__(self, item):
        # 一些同名的隐射
        if item in ['mobile_headers', 'mobile_header', 'mobile_meta']:
            return self.mobile_metas
        elif item in ['header']:
            return self.headers
        elif item in ['no_inject']:
            return self.set_no_html_inject


    @property
    def a_color(self):
        return self.get_a_color()

    @cached_property
    def prefix_url(self):
        prefix = getattr(g, 'prefix', '')
        if prefix and isinstance(prefix, (str, unicode)):
            prefix = prefix.strip('/')
        return prefix


    @cached_property
    def mobile_metas(self):
        return """
        <meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0" name="viewport"/>
        <meta content="yes" name="apple-mobile-web-app-capable"/>
        <meta content="black" name="apple-mobile-web-app-status-bar-style"/>
        <meta content="telephone=no" name="format-detection"/>
        <meta name="renderer" content="webkit">\n"""


    def seo(self, keywords=None, description=None):
        if getattr(g, 'seo_header_set', False):
            # 在一个页面内，仅仅能运行一次, 会被 h.headers 调用，如果要使用seo，确保 seo 在之前运行
            return ''
        keywords = keywords or get_value_from_data(g, 'doc.metadata.keywords') or get_value_from_data(g, 'site.configs.keywords')
        if isinstance(keywords, (list, tuple)): # keywords 是一个list
            keywords = [smart_unicode(k) for k in keywords]
            keywords = ', '.join(keywords)
        description = description or get_value_from_data(g, 'doc.metadata.description') or get_value_from_data(g, 'site.configs.description')
        html_content = self.set_metas(keywords=keywords, description=description)
        g.seo_header_set = True
        return html_content


    @cached_property
    def headers(self):
        return self.mobile_metas + self.seo()


    def set_meta(self, key, value):
        # 生成 HTML 的 head_meta
        if not key or not value:
            return ''
        key = smart_unicode(key).replace('"', "'")
        value = html_escape(smart_unicode(value).replace('"', "'"))
        meta_content = '<meta name="%s" content="%s">\n' % (key, value)
        return meta_content

    def set_metas(self, **kwargs):
        html_content = ''
        for k, v in kwargs.items():
            html_content += self.set_meta(k, v)
        return html_content


    @staticmethod
    def set_no_html_inject(status=True):
        # utils.render 的insert_into_header/footer 将会失效
        g.no_html_inject = status
        return ''


    def disable_load(self):
        # 禁用 load 这个函数
        g.disable_load_func = True
        return ''


    @classmethod
    def load(cls, *resource, **kwargs):
        if getattr(g, 'disable_load_func', False): # load函数被禁用了
            return ''

        force_load = kwargs.pop('force', False)

        if not resource:
            return ''


        if len(resource) == 1:
            resource = resource[0]
            if ' ' in resource: # load('a b c')的处理
                resource = resource.split(' ')

        # resource 可以是一个 list，也可以是字符串
        # 预先进行类型判断
        if isinstance(resource, (list, tuple)):
            result = ''
            for child_resource in resource:
                if isinstance(child_resource, (str, unicode)):
                    result += cls.load(child_resource)
            return result
        elif not isinstance(resource, (str, unicode)):
            return ''

        # 确保进入以下流程的都是单个 resource，这样才能达到去重的效果

        #相同的 resource，一个页面内，仅允许载入一次
        loads_in_page = getattr(g, 'loads_in_page', [])
        if not isinstance(loads_in_page, list):
            loads_in_page = []
        if resource in loads_in_page and not force_load:
             #ignore, 页面内已经载入过一次了
            return ''
        else:
            loads_in_page.append(resource)
            g.loads_in_page = loads_in_page

        if not isinstance(resource, (str, unicode)):
            return resource


        resource_path = resource
        if '?' in resource:
            resource_path = resource.split('?')[0]
        ext = os.path.splitext(resource_path)[1].lower()
        if not ext:
            ext = '.%s' % (resource.split('?')[0].split('/')[-1]) # 比如http://fonts.useso.com/css?family=Lato:300

        if ext == '.js' or ext.startswith('.js?') or resource.split('?')[0].endswith('js'):
            content = '<script type="text/javascript" src="%s"></script>' % resource
        elif ext in ['.css', '.less', '.scss', '.sass'] or ext.startswith('.css?') or ext.endswith('?format=css'):
            content = '<link href="%s" type="text/css" rel="stylesheet"/>' % resource
        else:
            content = ''

        return content



    def show_notification(self, message, timeout=0, status=None, position='top'):
        if status in ['no', 'fail', 'failed', 'false', False, 0]:
            status = 'error'
        elif status in ['yes', 'done', True, 1]:
            status = 'success'
        if status not in ['error', 'success']:
            status = 'normal'
        if position not in ['top', 'bottom']:
            position = 'top'
        message = message.replace("'", '')
        script = self.load('essage')+ "<script>var essage_message={message: '%s', status: '%s', placement: '%s'}; if(Essage){Essage.show(essage_message, %s)}</script>" %\
                                       (message, status, position, timeout)
        return script


    def show_note(self, *args, **kwargs):
        return self.show_notification(*args, **kwargs)


    def re_dom(self, html_content, rules):
        # 重新渲染 html 的某些 dom 结构
        # 一般用不到，但是在一些特定的或者封闭性的平台中或许有用，比如微信的公众号
        html_content = re_html_dom(html_content, rules)
        return html_content


    def linebreaks(self, content):
        content = smart_unicode(content)[:50000]
        return _linebreaks(content)

    @property
    def random_dom_id(self):
        # 返回一个随机的dom_id
        return 'd_%s' % uuid.uuid4().hex


    def get_dom_id(self, v=None):
        # 将一个value转为dom_id的格式
        return 'dd_%s' % get_md5(v)

    @staticmethod
    def join_url(url, *args, **kwargs):
        new_url = join_url(url, **kwargs)
        return new_url

    @staticmethod
    def get_url(url):
        return get_url_with_prefix(url)

    @staticmethod
    def url(url):
        # 同 get_url
        return get_url_with_prefix(url)


    @staticmethod
    def i18n(key, *args):
        key = smart_unicode(key)
        if not args:
            # 获取
            if key.startswith('_'): # 以_开头的，摘1后，返回原值
                return key[1:]
            lang = get_language()
            key1 = '%s-%s' % (key, lang)
            i18n_data = getattr(g, 'i18n', {})
            matched_value = i18n_data.get(key1) or i18n_data.get(key)
            return matched_value or key
        elif len(args)<=2:
            if not getattr(g, 'i18n', None):
                g.i18n = {}
            if len(args) == 2: # 指定了 lang 的
                value, lang = args
                lang = smart_unicode(lang).strip().lower()
                key = '%s-%s' % (key, lang)
            else: # 没有指定lang，设定默认值
                value = args[0]
            g.i18n[key] = value
            # 设置的
        # at last
        return ''


    @staticmethod
    def paginator(paginator=None, style='simple', **kwargs):
        # todo 页码分页的问题还要继续对应
        if 'simple' in kwargs and not kwargs.get('simple'):
            # 对旧的兼容，最开始的时候，auto 风格的调用是 simple=False
            style = 'auto'
        # 构建上下页的label，当然本身也是可以传入 HTML 片段的
        if 'pre_label' not in kwargs:
            if style == 'mini':
                pre_label = '<'
            else:
                pre_label = '&laquo; Prev'
            kwargs['pre_label'] = pre_label
        if 'next_label' not in kwargs:
            if style == 'mini':
                next_label = '>'
            else:
                next_label = 'Next &raquo;'
            kwargs['next_label'] = next_label

        paginator = paginator or get_paginator()
        if not paginator:
            return '' # ignore

        return render_api_template('paginator',
                                    paginator=paginator, paginator_style=style, return_html=True, **kwargs)



@cache_result
def h():
    return Html()

@cache_result
def html():
    return Html()