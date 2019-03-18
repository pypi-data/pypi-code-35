# coding: utf8
from __future__ import absolute_import
from flask import request, g

from farbox_lite.utils.web.cache_for_function import cache_result

from farbox_lite.utils import get_md5, smart_unicode, get_random_html_dom_id
from farbox_lite.utils.layout.utils import get_grid_factor
from farbox_lite.utils.functional import curry

from farbox_lite.utils.web.response import force_response
from farbox_lite.utils.web.request import get_user_agent
from farbox_lite.template_system.functions.namespace.html import Html


import re





@cache_result
def browser():
    # 对浏览器的判断，符合条件的才显示对应的内容
    def _func(family, **kwargs):
        caller = kwargs.pop('caller', None)
        if not caller or not hasattr(caller, '__call__'):
            return ''
        user_agent = get_user_agent()
        if not user_agent:
            return ''

        family = smart_unicode(family)
        totally_matched = False
        if family.startswith('@'):
            totally_matched = True
            family = family[1:]
        if totally_matched:
            return_html = family==user_agent.browser.family.lower()
        else:
            # 如果family 传入为空，则以下条件始终为 True
            return_html = family.lower() in user_agent.browser.family.lower()

        version = kwargs.get('version', None)
        if version and return_html: # 指定了 version 的
            browser_version = user_agent.browser.version_string
            if version == browser_version:
                pass
            elif version.startswith('>=') and version[2:]>=browser_version:
                pass
            elif version.startswith('>') and version[1:]>browser_version:
                pass
            elif version.startswith('<=') and version[2:]<=browser_version:
                pass
            elif version.startswith('<') and version[1:]<browser_version:
                pass
            else:
                return_html = False
        if return_html:
            html = caller()
            return html
        else:
            return '' # at last
    return _func


@cache_result
def create_dom():
    # 由于 jade 语法的显示，不能产生动态类型的 dom，所以增加了这个函数进行补足
    def _func(tag='div', *args, **kwargs):
        # *args 实际上是忽略的，没有任何作用
        caller = kwargs.pop('caller', None)
        inner_html = kwargs.pop('content', None) # 内部的 html 可以由 content 这个参数传入，或者其为空的时候，调用 caller
        extra_kwargs = kwargs.pop('extra', None)
        if extra_kwargs and isinstance(extra_kwargs, dict):
            kwargs.update(extra_kwargs)
        if inner_html:
            inner_html = smart_unicode(inner_html)
        if (not caller or not hasattr(caller, '__call__')) and not inner_html:
            return ''
        if not isinstance(tag, (str, unicode)):
            return ''
        if len(tag) > 20:
            return ''
        href = kwargs.pop('href', None)
        if tag == 'a' or href: # 有 href，也视为 a 元素
            tag = 'a'
            group_id = kwargs.pop('group_id', None)
        else:
            group_id = None
        properties = ''
        if tag == 'a' and href:
            create_a_dom = True
        else:
            create_a_dom = False
        for key, value in kwargs.items():
            if key in ['title', 'content'] or '_' in key:
                continue
            elif create_a_dom and key in ['href', 'class']:
                continue
            else:
                properties += ' %s="%s" '%(key, value)
        if inner_html is None and caller:
            inner_html = caller()
        elif not inner_html:
            inner_html = ''
        if create_a_dom: # 调用 auto_a, 可以实现一些基本预览的处理
            html = Html.auto_a(inner_html, href, a_title=kwargs.get('title'), class_name=kwargs.get('class'), group_id=group_id)
            if properties:
                html = html.replace('<a ', '<a %s '% properties, 1)
            return html
        html = '<%s %s>%s</%s>'  % (tag, properties, inner_html, tag)
        return html
    return _func



@cache_result
def footer(): # 兼容 FarBox、Bitcron
    def _func(*args, **kwargs):
        caller = kwargs.pop('caller', None)
        if not caller or not hasattr(caller, '__call__'):
            return ''
        inner_html = caller()
        g.footer = inner_html
        return inner_html
    return _func


# 兼容
@cache_result
def font():
    # +font(path, **name, title_path, title_name,)
    def _func(font_filepath, *args, **kwargs):
        caller = kwargs.pop('caller', None)
        if not caller or not hasattr(caller, '__call__') or not g.site:
            return ''
        embed_html = caller()
        return embed_html
    return _func


@cache_result
def pure(): # 对 pure css 的处理
    def _func(*args, **kwargs):
        do_grid = True
        caller = kwargs.pop('caller', None)
        if not caller or not hasattr(caller, '__call__'):
            return ''
        inner_html = caller()

        factors_devices = ['pure-u', # 总是,  # 全填满的时候相当于phone
                           'pure-u-sm', # ≥ 568px  # phone 横
                           'pure-u-md', # ≥ 768px  # ipad
                           'pure-u-lg', # ≥ 1024px # ipad 横 & 普通桌面
                           'pure-u-xl', # ≥ 1280px # 大桌面
                           ]
        html_class = smart_unicode(kwargs.get('class') or '')
        html_class_list = html_class.split('.')
        html_class = ' '.join(html_class_list)
        if len(args):
            for i, raw_factor in enumerate(args):
                grid_factor = get_grid_factor(raw_factor)
                grid_value, grid_base = grid_factor
                try: prefix = factors_devices[i]
                except: break
                grid_class = '%s-%s-%s' % (prefix, grid_value, grid_base)
                html_class += ' %s'%grid_class
            do_grid = False
        if do_grid: # 外部的 grid 包裹
            return '%s\n<div class="pure-g">\n%s\n</div>' % (Html.load('pure'), inner_html)
        else: # 某个具体 grid
            html_class = html_class.replace('"', '') + ' pure_cell'
            return '\n<div class="%s">\n%s\n</div>' % (html_class, inner_html)

    return _func





####### refer starts

def re_sub_refer(re_obj, handler=None):
    prefix = re_obj.group(1)
    url = re_obj.group(2)
    suffix = re_obj.group(3)
    new_line = False
    if prefix and suffix:
        if prefix.startswith('<span ') and 'md_line' in prefix and suffix == '</span>':
            new_line = True
        elif re.match(r'<div[ >]', prefix) and suffix == '</div>':
            new_line = True
        elif re.match(r'<p[ >]', prefix) and suffix=='</p>':
            new_line = True
    original_html = re_obj.group(0)
    new_html = original_html

    # 三个变量，逐个试过去...
    try:
        new_html = handler(url, original_html, new_line)
    except TypeError:
        try: new_html = handler(url, original_html)
        except TypeError:
            try: new_html = handler(url)
            except: pass
    except:
        pass
    return new_html

@cache_result
def refer():
    def _func(handler=None, refer_type='link', **kwargs):
        caller = kwargs.pop('caller', None)
        if not caller or not hasattr(caller, '__call__'):
            return ''
        inner_html = caller()
        if not handler or not hasattr(handler, '__call__'):
            return inner_html
        if refer_type in ['image', 'images']:
            # 图片
            inner_html = re.sub(r"""(<[^<>]+>)?<img [^<>]*?src=['"](.*?)['"][^<>]*?/?>(</\w+>)?""", curry(re_sub_refer, handler=handler), inner_html)
        else:
            # 链接
            inner_html = re.sub(r"""(<[^<>]+>)?<a [^<>]*?href=['"](.*?)['"][^<>]*?>.*?</a>(</\w+>)?""", curry(re_sub_refer, handler=handler), inner_html)
        return inner_html
    return _func


####### refer ends
