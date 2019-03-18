#coding: utf8
from __future__ import absolute_import
import os
import unidecode
import re
import urllib
import datetime
from dateutil.parser import parse as parse_date
from farbox_markdown.compile_md import compile_markdown
from farbox_lite.utils import smart_unicode, smart_str, get_relative_path, string_to_list
from farbox_lite.compiler.utils import get_sort_and_name_from_filepath


def count_words(content):
    content = smart_unicode(content)
    total_words = len(re.findall(ur'[\w\-_/]+|[\u1100-\ufde8]', content))
    return total_words

def slugify(value, must_lower=True, auto=False):
    # auto=True 表示是自动生成的
    value= smart_unicode(value)
    value = unidecode.unidecode(value).strip()
    if must_lower:
        value = value.lower()
    value = re.sub(r'[ &~,"\':*+?#{}()<>\[\]]', '-', value).strip('-')  # 去掉非法的url字符
    value = re.sub(r'-+', '-', value)  # 替换连续的 --的或者-/
    value = value.replace('-/', '/')
    if auto: # 去掉可能的序号, 这样自动生成的 url 美观一点
        value = re.sub(r'^\d{1,2}(\.\d+)? ', '', value).strip() or value
        value = value.strip('-_')
    value = value.strip('/') # 头尾不能包含 /
    return value


def to_date(value):
    if not value:
        return None
    if isinstance(value, datetime.datetime):
        return value
    elif isinstance(getattr(value, 'core', None), datetime.datetime): # 被Date给wrap了
        return getattr(value, 'core', None)
    else:
        try:
            return parse_date(value)
        except:
            return None


def get_images_from_html(content, relative_to_site=False):
    raw_images = re.findall("""<\s*img.*?src=['"]([^'"]+).*?>""", content, flags=re.I)
    images = []
    for image_src in raw_images:
        if image_src in images:
            continue
        if relative_to_site and ('://' in image_src or image_src.startswith('//')):
            continue
        images.append(image_src)
    return images



def get_md_meta_value(compiled_content, key_name, default=None):
    metadata = getattr(compiled_content, 'metadata', {})
    if not isinstance(metadata, dict):
        metadata = {}
    if key_name in metadata:
        value = metadata.get(key_name)
        if value is None:
            value = default
    else:
        value = default
    if isinstance(value, (str, unicode)):
        value = value.strip()
    # 根据default的值，自动格式化得到的value
    if default is not None and not isinstance(value, basestring) and value is not None:
        value = type(default)(value)  # 变量格式化
    return value


def filepath_to_post_doc(filepath, root=None):
    if not os.path.isfile(filepath):
        return {}
    if not root:
        root = os.path.dirname(filepath)
    filepath = smart_unicode(filepath)
    relative_path = get_relative_path(filepath, root=root)
    relative_path = smart_unicode(relative_path)
    filename = os.path.split(filepath)[-1]
    just_name = os.path.splitext(filename)[0]
    slash_number = relative_path.count('/')

    with open(filepath, 'rb') as f:
        raw_content = f.read()
    raw_content = smart_unicode(raw_content)
    compiled_content = compile_markdown(raw_content)

    sort, name = get_sort_and_name_from_filepath(filepath)
    title = get_md_meta_value(compiled_content, 'title', '')
    #文中没有声明，看有没有唯一的H1作为title
    if not title and getattr(compiled_content, 'title', None) and getattr(compiled_content, 'title_from_post', False):
        title = compiled_content.title
    if not title: # 仍然没有title的，就取文件名
        title = just_name
        if title == 'index': # index doc, get parent folder's name
            parent_folder = os.path.dirname(filepath)
            title = os.path.split(parent_folder)[-1]
    title = smart_unicode(title.strip())

    tags = get_md_meta_value(compiled_content, 'tags') or get_md_meta_value(compiled_content, 'tag')
    tags = string_to_list(tags)
    if not isinstance(tags, (list, tuple)):
        tags = []

    if relative_path in ['robots.txt', 'robot.txt']:
        status = 'system'
    elif re.match(r'^_[a-z]{1,20}/', relative_path, re.I) and not re.match(r'_posts?/', relative_path)\
            and not get_md_meta_value(compiled_content,'status'):
        # 位于_xxx 目录下的，默认为status 为 xxx (如果没有声明的话)
        # 但是对_post/_posts下的目录不处理status，兼容Jekyll
        status = relative_path.split('/')[0].lower().strip('_')
    else:
        status = get_md_meta_value(compiled_content, 'status', 'public') or 'public'
    status = status.strip().lower()

    # url_path是全小写
    url_path = get_md_meta_value(compiled_content, 'url', '') or get_md_meta_value(compiled_content, 'url_path', '')
    if url_path and not isinstance(url_path, basestring):
        url_path = smart_unicode(url_path)
    if not url_path: # 如果是用户自己指定的url，则不管对错，都保存; 反之则是通过relative_path解析一个url
        url_path = relative_path.rsplit('.', 1)[0]
        url_path = slugify(url_path, auto=True).lower() # 不能以slash开头,并且确保小写
    else: # 用户自己声明的 url，不做大小写处理，保留原始状态
        url_path = slugify(url_path, must_lower=False) # 替代掉不适合做url的字符
    if '%' in url_path:
        # 被编码的url，特别是wordpress转过来的
        _url_path = urllib.unquote(smart_str(url_path))
        if url_path != _url_path:
            url_path = smart_unicode(_url_path)
    url_path = url_path.lstrip('/')
    url_path = re.sub(r'/{2,}', '/', url_path)
    url_path = url_path or '--' # 可能存在空的情况...


    # date
    # 文件，client属性中的最后修改时间
    updated_at = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
    try:
        updated_at_s = smart_str(get_md_meta_value(compiled_content, 'date', ''))
        if updated_at_s:
            updated_at_s = updated_at_s.strip()
        if updated_at_s and re.match('\d{4}\.\d+\.\d+$', updated_at_s):
            # # 2018.3.19  这种日期形式的 转为 xxxx-xx-xx
            updated_at_s = updated_at_s.replace('.', '-')
        if not updated_at_s:
            # 兼容 '2012-12-12 12-12 or 2012-12-12 12-12-12 这种格式'
            done = False
            if re.match(r'^\d+-\d+-\d+ \d+-\d+(-\d+)?$', just_name):
                part1, part2 = just_name.split(' ', 1)
                try:
                    updated_at = parse_date('%s %s' % (part1, part2.replace('-', ':')))
                    done = True
                except:
                    pass
            if not done:
                # 尝试从文件名中获取 2012-1?2-1?2, date模式
                date_search = re.search('/?(\d{4}-\d{1,2}-\d{1,2})[^/]*', relative_path)
                if date_search: # 可以从文件的路径中取， 兼容jekyll
                    updated_at_s = date_search.groups()[0]
        if updated_at_s:
            try:
                updated_at = parse_date(updated_at_s)
            except:
                pass
    except (ValueError, TypeError):
        pass


    metadata = compiled_content.metadata.copy()
    doc = dict(
        title = title,
        status = status,
        tags = tags,
        url_path = url_path,
        date = updated_at,

        cover = compiled_content.cover,
        toc = compiled_content.toc,
        metadata = metadata,
        images = get_images_from_html(compiled_content) or [],

        raw_content = raw_content,
        content = compiled_content,
        text_length = len(raw_content),
        text_words = count_words(raw_content),

        slash_number = slash_number,

        path = relative_path.lower(),
        filepath = filepath,
        md_filepath = filepath,
        mtime = os.path.getmtime(filepath),
        sort = sort,
        position = sort,

        type = 'post',

        id = filepath,

        url = '/post/%s' % url_path
    )

    return doc



